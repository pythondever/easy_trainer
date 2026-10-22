# -*- coding: utf-8 -*-
"""项目备份/恢复 UI 交互: 对话框装配 + 进度框 + 右键菜单入口.

核心逻辑在 app/core/backup.py(无 Qt 依赖, 有单测); 这里只负责选路径/
显示摘要/用 ProgressDialog 包裹 core 调用, 不碰记录过滤与路径重写.
"""

import os
import traceback

from PySide6.QtCore import QCoreApplication as QC
from PySide6.QtWidgets import QDialog, QFileDialog

from app.core import backup as bk
from app.widgets.dialog_buttons import apply_icon
from app.widgets.message_box import MessageBox, ProgressDialog
from ui.backup_restore import Ui_Dialog


class BackupMixin:

    def _on_backup_restore(self, project=None, mode="backup"):
        """项目右键菜单入口: 备份/恢复对话框. mode 决定打开时停在哪一页."""
        dlg = QDialog(self)
        ui = Ui_Dialog()
        ui.setupUi(dlg)
        ui.bk_mode_restore.setChecked(mode == "restore")

        def on_mode():
            backing = ui.bk_mode_backup.isChecked()
            ui.bk_stack.setCurrentIndex(0 if backing else 1)
            ui.bk_ok_btn.setText(
                QC.translate("BackupMixin", "开始备份") if backing
                else QC.translate("BackupMixin", "开始恢复"))
            # 项目来自右键菜单, 标题栏直接显示, 不再放下拉框
            if backing and project:
                dlg.setWindowTitle(
                    QC.translate("BackupMixin", "备份项目: {}").format(project))
            elif project:
                dlg.setWindowTitle(
                    QC.translate("BackupMixin", "恢复项目到: {}").format(project))
            else:
                dlg.setWindowTitle(
                    QC.translate("BackupMixin", "恢复项目"))

        ui.bk_mode_backup.toggled.connect(on_mode)
        on_mode()
        ui.bk_browse_btn.clicked.connect(
            lambda: self._bk_pick_dir(ui.bk_save_path,
                                      QC.translate("BackupMixin", "选择备份保存位置")))
        ui.bk_pkg_btn.clicked.connect(lambda: self._bk_pick_pkg(ui, project))
        apply_icon(ui.bk_ok_btn, QC.translate("BackupMixin", "确定"))
        ui.bk_ok_btn.clicked.connect(dlg.accept)
        ui.bk_cancel_btn.clicked.connect(dlg.reject)
        if dlg.exec() != QDialog.Accepted:
            return
        if ui.bk_mode_backup.isChecked():
            self._do_backup_project(ui, project)
        else:
            self._do_restore_project(ui, project)

    def _bk_pick_dir(self, line_edit, title):
        path = QFileDialog.getExistingDirectory(self, title)
        if path:
            line_edit.setText(path)

    def _bk_pick_pkg(self, ui, project=None):
        """选备份包并回填摘要(只读 manifest, 不解包).

        project 为右键项目: 恢复内容将归属到它(与包内项目名可以不同)."""
        path, _ = QFileDialog.getOpenFileName(
            self, QC.translate("BackupMixin", "选择备份包"),
            "", QC.translate("BackupMixin", "备份包 (*.etbak)"))
        if not path:
            return
        try:
            manifest = bk.read_backup(path)[0]
        except bk.RestoreError as e:
            MessageBox.warning(self, QC.translate("BackupMixin", "恢复"), str(e))
            return
        ui.bk_pkg_path.setText(path)
        # 恢复目标: 右键项目(内容进这个项目); 没传则按包内项目名
        target = (project or "").strip() or manifest["project"]
        lines = [
            QC.translate("BackupMixin", "项目: {}").format(manifest["project"]),
            QC.translate("BackupMixin", "备份时间: {}").format(
                manifest.get("created_at", "")),
            QC.translate("BackupMixin", "数据集: {} 个(共 {} 张, 已标注 {} 张)").format(
                len(manifest["datasets"]),
                sum(d.get("total", 0) for d in manifest["datasets"]),
                sum(d.get("labeled", 0) for d in manifest["datasets"])),
            QC.translate("BackupMixin", "训练记录: {} 条 | 未开始队列: {} 项").format(
                manifest.get("train_records", 0), manifest.get("queue_items", 0)),
        ]
        if target != manifest["project"]:
            lines.append(QC.translate(
                "BackupMixin", "恢复到: {}(当前项目)").format(target))
        # 解包位置固定为包同目录的 restore_<目标项目>, 摘要里告诉用户数据落在哪
        dest = os.path.join(
            os.path.dirname(os.path.abspath(path)), "restore_" + target)
        lines.append(QC.translate("BackupMixin", "解包位置: {}").format(dest))
        # 目标项目仅空项目可恢复, 摘要提前给出结论, 别等走完流程才报错
        # 结论必须说清是"目标项目"(右键项目或包内项目), 两者不同名时
        # 用户站在右键项目上操作, 不说清会误读成右键项目本身冲突
        if target in self.db.get_projects():
            clash = bk.project_content(self.db, target)
            if clash:
                lines.append(QC.translate(
                    "BackupMixin",
                    "目标项目\"{}\"在库中已存在且包含 {} 项内容, "
                    "无法恢复(需先删除)").format(target, len(clash)))
            else:
                lines.append(QC.translate(
                    "BackupMixin",
                    "目标项目\"{}\"在库中已存在(空项目), 可直接恢复").format(
                        target))
        ui.bk_summary.setText("\n".join(lines))

    def _bk_progress_cb(self, prog):
        def cb(done, total, text):
            prog.set_progress(int(done * 100 / max(1, total)), text)
        return cb

    def _do_backup_project(self, ui, project):
        project = (project or "").strip()
        save_dir = ui.bk_save_path.text().strip()
        if not project:
            MessageBox.warning(self, QC.translate("BackupMixin", "备份"),
                               QC.translate("BackupMixin", "未指定项目"))
            return
        if not save_dir:
            MessageBox.warning(self, QC.translate("BackupMixin", "备份"),
                               QC.translate("BackupMixin", "请选择备份保存位置"))
            return
        zip_path = os.path.join(save_dir, project + ".etbak")
        if os.path.exists(zip_path):
            if not MessageBox.question(
                    self, QC.translate("BackupMixin", "备份"),
                    QC.translate("BackupMixin", "备份包已存在, 覆盖吗?\n{}").format(
                        zip_path), default_yes=True):
                return
        prog = ProgressDialog(
            QC.translate("BackupMixin", "备份"),
            QC.translate("BackupMixin", "正在备份项目..."), self,
            maximum=100, cancellable=False)
        try:
            manifest = bk.write_backup(
                self.db, project, zip_path,
                include_data=ui.bk_inc_data.isChecked(),
                include_models=ui.bk_inc_models.isChecked(),
                progress=self._bk_progress_cb(prog))
        except Exception as e:
            self._log(QC.translate("BackupMixin", "备份失败: {} | {}").format(
                project, traceback.format_exc()))
            MessageBox.critical(self, QC.translate("BackupMixin", "备份失败"), str(e))
            return
        finally:
            prog.close()
        size_mb = os.path.getsize(zip_path) / (1024.0 * 1024.0)
        MessageBox.information(
            self, QC.translate("BackupMixin", "备份"),
            QC.translate("BackupMixin", "项目\"{}\"备份完成\n数据集 {} 个 | 训练记录 {} 条 | 包大小 {:.1f} MB\n位置: {}").format(
                project, len(manifest["datasets"]),
                manifest["train_records"], size_mb, zip_path))
        self._log(QC.translate("BackupMixin", "备份项目完成: {} | {} 个数据集 | {} 条训练记录 | → {}").format(
            project, len(manifest["datasets"]), manifest["train_records"], zip_path))

    def _do_restore_project(self, ui, project=None):
        pkg = ui.bk_pkg_path.text().strip()
        if not pkg:
            MessageBox.warning(self, QC.translate("BackupMixin", "恢复"),
                               QC.translate("BackupMixin", "请选择备份包"))
            return
        # 恢复目标: 右键项目(内容进这个项目, 不按包内项目名新建)
        target = (project or "").strip() or None
        # 冲突提前报: 目标项目仅空项目可恢复, 非空带内容清单弹同款警示框
        try:
            manifest = bk.check_restorable(self.db, pkg, target)
        except bk.RestoreError as e:
            items = getattr(e, "items", None)
            if items:
                # 沿用"路径失效"那套弹窗: 警示图标+正文+清单+知道了
                MessageBox.missing_paths(
                    self, QC.translate("BackupMixin", "恢复失败"), str(e),
                    QC.translate("BackupMixin", "项目内容 · {} 项").format(
                        len(items)), items)
            else:
                MessageBox.warning(
                    self, QC.translate("BackupMixin", "恢复"), str(e))
            return
        # 固定解包到 .etbak 同目录的 restore_<目标项目>: 数据要留着给绑定
        # 路径用, 位置固定才找得到
        dest = os.path.join(
            os.path.dirname(os.path.abspath(pkg)),
            "restore_" + (target or manifest["project"]))
        prog = ProgressDialog(
            QC.translate("BackupMixin", "恢复"),
            QC.translate("BackupMixin", "正在恢复项目..."), self,
            maximum=100, cancellable=False)
        try:
            manifest = bk.restore_backup(
                self.db, pkg, dest, include_data=True, target_project=target,
                progress=self._bk_progress_cb(prog))
        except bk.RestoreError as e:
            MessageBox.critical(self, QC.translate("BackupMixin", "恢复失败"), str(e))
            return
        except Exception as e:
            self._log(QC.translate("BackupMixin", "恢复失败: {} | {}").format(
                pkg, traceback.format_exc()))
            MessageBox.critical(self, QC.translate("BackupMixin", "恢复失败"), str(e))
            return
        finally:
            prog.close()
        self.refresh_project_list()
        done_text = ("项目\"{}\"已恢复到\"{}\"".format(
            manifest["project"], target) if target
            else "项目\"{}\"恢复完成".format(manifest["project"]))
        MessageBox.information(
            self, QC.translate("BackupMixin", "恢复"),
            QC.translate("BackupMixin", "{}\n数据集 {} 个 | 训练记录 {} 条\n数据位置: {}").format(
                done_text, len(manifest["datasets"]),
                manifest["train_records"], dest))
        self._log(QC.translate("BackupMixin", "恢复项目完成: {} → {} | {} 个数据集 | {} 条训练记录 | → {}").format(
            manifest["project"], target or manifest["project"],
            len(manifest["datasets"]), manifest["train_records"], dest))
