import lmdb
import json
import os
import time
import uuid
from . import keys

# LMDB map_size 上限。注意 Windows 上这是真实预分配(非稀疏文件):
# 设为 N 则 data.mdb 立即占用约 N 磁盘空间, 与实际数据量无关, 故不宜盲目取大。
# 128MB 约可容纳数百条完整训练记录(train_history 含每 epoch metrics 序列,
# 单条约数十 KB), 远大于旧值 10MB——旧值在训练记录累积后会 MapFullError 硬崩。
# 已存在的库用更大的 map_size 重新 open 是安全的, 已有数据不受影响。
DEFAULT_MAP_SIZE = 128 * 1024 * 1024


def _rename_item(item, old_name, new_name):
    """数据集项("项目/数据集"或纯名)中匹配 old_name 的数据集部分替换为新名。"""
    if "/" in item:
        proj, ds = item.rsplit("/", 1)
        return "{}/{}".format(proj, new_name) if ds == old_name else item
    return new_name if item == old_name else item


def _ds_of(item):
    """数据集项("项目/数据集"或纯名)取数据集名部分。"""
    return item.rsplit("/", 1)[-1] if "/" in item else item


class DataBase:
    def __init__(self, db_path, db_size=DEFAULT_MAP_SIZE):
        self.db_path = db_path
        self.db_size = db_size
        self.mdb = None
        # 进程内缓存: project_info_list 读多写少, 标注/标签/视图多处高频
        # get_project_info() 全量 json.loads, 缓存后仅首次反序列化;
        # 所有写方法(update/add/delete_project_info)写后置 None 失效。
        self._project_info_cache = None
        self.create_db()

    def create_db(self):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path, exist_ok=True)
        db_file = os.path.join(self.db_path, 'app.mdb')
        self.mdb = lmdb.open(db_file, map_size=self.db_size)

    def add_project(self, name):
        key = keys.project_list
        txn = self.mdb.begin(write=True)
        project_list = txn.get(key)
        if project_list is None:
            project_list = [name]
        else:
            project_list = json.loads(project_list.decode())
            project_list.append(name)
        txn.put(key, json.dumps(project_list).encode())
        txn.commit()

    def rename_project(self, old_name, new_name):
        project_list = self.get_projects()
        if project_list:
            for idx, project_name in enumerate(project_list):
                if project_name == old_name:
                    project_list[idx] = new_name
            key = keys.project_list
            txn = self.mdb.begin(write=True)
            txn.put(key, json.dumps(project_list).encode())
            txn.commit()
        info_list = self.get_project_info()
        changed = False
        for info in info_list:
            if info.get('project_name') == old_name:
                info['project_name'] = new_name
                changed = True
        if changed:
            self.update_project_info(info_list)
        self._rename_records_project(old_name, new_name)

    def _rename_records_project(self, old_name, new_name):
        """训练/模型记录中项目名替换(含 dataset/val_dataset/dataset_info 的"项目/"前缀)。"""
        txn = self.mdb.begin(write=True)
        for key in (keys.train_history, keys.model_history):
            data = txn.get(key)
            recs = json.loads(data.decode()) if data else []
            changed = False
            for r in recs:
                if r.get("project") != old_name:
                    continue
                r["project"] = new_name
                for field in ("dataset", "val_dataset", "dataset_info"):
                    items = [x.strip() for x in str(r.get(field, "")).split(",") if x.strip()]
                    new_items = []
                    for it in items:
                        if "/" in it:
                            proj, ds = it.rsplit("/", 1)
                            new_items.append("{}/{}".format(
                                new_name if proj == old_name else proj, ds))
                        else:
                            new_items.append(it)
                    if new_items != items:
                        r[field] = ", ".join(new_items)
                changed = True
            if changed:
                txn.put(key, json.dumps(recs, ensure_ascii=False).encode())
        txn.commit()

    def delete_project(self, name):
        project_list = self.get_projects()
        if len(project_list) == 0:
            return
        for project_name in project_list:
            if project_name == name:
                project_list.remove(name)
        key = keys.project_list
        txn = self.mdb.begin(write=True)
        txn.put(key, json.dumps(project_list).encode())
        txn.commit()

    def get_projects(self):
        key = keys.project_list
        txn = self.mdb.begin(write=False)
        project_list = txn.get(key)
        if project_list is None:
            project_list = []
        else:
            project_list = json.loads(project_list.decode())
        return project_list

    def add_project_info(self, info):
        # 保存项目的详细信息(列表存储,每条 = 一个项目下的数据集记录)
        # 字段：project_name / dataset_name / dataset_type / image_path /
        #       label_path / label_fmt / labeled / total / labels
        key = keys.project_info_list
        txn = self.mdb.begin(write=True)
        info_list = txn.get(key)
        if info_list is None:
            info_list = [info]
        else:
            info_list = json.loads(info_list.decode())
            info_list.append(info)
        txn.put(key, json.dumps(info_list).encode())
        txn.commit()
        self._project_info_cache = None

    def get_project_info(self):
        if self._project_info_cache is not None:
            return self._project_info_cache
        key = keys.project_info_list
        txn = self.mdb.begin(write=False)
        info_list = txn.get(key)
        if info_list is None:
            info_list = []
        else:
            info_list = json.loads(info_list.decode())
        self._project_info_cache = info_list
        return info_list

    def update_project_info(self, info):
        key = keys.project_info_list
        txn = self.mdb.begin(write=True)
        txn.put(key, json.dumps(info).encode())
        txn.commit()
        self._project_info_cache = None

    def delete_project_info(self, name):
        project_list = self.get_project_info()
        keep_info = []
        for info in project_list:
            project_name = info['project_name']
            if project_name != name:
                keep_info.append(info)
        key = keys.project_info_list
        txn = self.mdb.begin(write=True)
        txn.put(key, json.dumps(keep_info).encode())
        txn.commit()
        self._project_info_cache = None

    def _get_deleted_maps(self):
        key = keys.deleted_images
        txn = self.mdb.begin(write=False)
        data = txn.get(key)
        if data is None:
            return {}
        try:
            return json.loads(data.decode())
        except Exception:
            return {}

    def add_deleted_image(self, project_name, dataset_name, image_path):
        """记录一张被删除/不加载的图像。"""
        key = keys.deleted_images
        txn = self.mdb.begin(write=True)
        maps = txn.get(key)
        if maps is None:
            maps = {}
        else:
            maps = json.loads(maps.decode())
        project_data = maps.setdefault(project_name, {})
        path_set = project_data.setdefault(dataset_name, [])
        norm = os.path.normcase(os.path.normpath(image_path))
        if norm not in path_set:
            path_set.append(norm)
        txn.put(key, json.dumps(maps).encode())
        txn.commit()

    def get_deleted_images(self, project_name, dataset_name):
        """返回该数据集的已删除/不加载图像路径集合（归一化）。"""
        maps = self._get_deleted_maps()
        project_data = maps.get(project_name, {})
        return set(project_data.get(dataset_name, []))

    def get_datasets(self, project_name):
        """返回某项目的数据集列表 [{'dataset_name','dataset_type','labeled','total'}, ...]。"""
        result = []
        for info in self.get_project_info():
            if info.get('project_name') == project_name:
                result.append({
                    'dataset_name': info.get('dataset_name', ''),
                    'dataset_type': info.get('dataset_type', ''),
                    'labeled': info.get('labeled', 0),
                    'total': info.get('total', 0),
                })
        return result

    def add_dataset(self, project_name, dataset_name, dataset_type=''):
        """在项目下新增一个数据集记录。返回 True 成功 / False 名称已存在。"""
        if not project_name or not dataset_name:
            return False
        for info in self.get_project_info():
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                return False  # 项目下数据集重名
        self.add_project_info({
            'project_name': project_name,
            'dataset_name': dataset_name,
            'dataset_type': dataset_type,
        })
        return True

    def rename_dataset(self, project_name, old_name, new_name, dataset_type=None):
        """修改数据集名称/类型。返回 True 成功 / False 重名或不存在。"""
        if not new_name:
            return False
        info_list = self.get_project_info()
        target = None
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == old_name):
                target = info
                break
        if target is None:
            return False
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == new_name
                    and info is not target):
                return False
        target['dataset_name'] = new_name
        if dataset_type is not None:
            target['dataset_type'] = dataset_type
        self.update_project_info(info_list)
        self._rename_records_dataset(project_name, old_name, new_name)
        return True

    def _rename_records_dataset(self, project_name, old_name, new_name):
        """
        训练/模型记录中该数据集名替换(训练集/验证集/dataset_info)。
        dataset 字段为 "项目/数据集" 格式,匹配后半段数据集名。
        """
        txn = self.mdb.begin(write=True)
        for key in (keys.train_history, keys.model_history):
            data = txn.get(key)
            recs = json.loads(data.decode()) if data else []
            changed = False
            for r in recs:
                if r.get("project") != project_name:
                    continue
                replaced = False
                for field in ("dataset", "val_dataset"):
                    names = [x.strip() for x in str(r.get(field, "")).split(",") if x.strip()]
                    new_names = [_rename_item(n, old_name, new_name) for n in names]
                    if new_names != names:
                        r[field] = ", ".join(new_names)
                        replaced = True
                if replaced:
                    info = str(r.get("dataset_info", ""))
                    items = [x.strip() for x in info.split(",") if x.strip()]
                    new_items = [_rename_item(n, old_name, new_name) for n in items]
                    r["dataset_info"] = ", ".join(new_items)
                    changed = True
            if changed:
                txn.put(key, json.dumps(recs, ensure_ascii=False).encode())
        txn.commit()

    def delete_dataset(self, project_name, dataset_name):
        """删除项目下的一个数据集记录。"""
        info_list = self.get_project_info()
        keep = []
        for info in info_list:
            if not (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                keep.append(info)
        self.update_project_info(keep)
        # 同步清理该数据集的自定义标签 / 已删除图像记录
        self.delete_dataset_deleted(project_name, dataset_name)

    def delete_dataset_deleted(self, project_name, dataset_name):
        """删除数据集时清理其已删除图像记录。"""
        key = keys.deleted_images
        txn = self.mdb.begin(write=True)
        maps = txn.get(key)
        if maps is not None:
            maps = json.loads(maps.decode())
            project_data = maps.get(project_name)
            if project_data is not None:
                project_data.pop(dataset_name, None)
                if not project_data:
                    maps.pop(project_name, None)
                txn.put(key, json.dumps(maps).encode())
        txn.commit()

    def update_dataset_import(self, project_name, dataset_name, image_path, label_path='',
                              label_fmt='', labeled=None, total=None, append=False):
        """
        保存（或更新）某数据集的导入路径绑定；labeled/total 为标注/总数统计。
        支持多次导入：image_paths / label_paths 为历史路径列表（去重保留），
        单值字段 image_path/label_path 保持最新（向后兼容）。
        参数兼容 str 或 list（多路径合并导入）
        append=False（默认）: labeled/total 直接覆盖（适合全量重算）
        append=True: labeled/total 累加到原值（适合追加新图, 不覆盖已有统计）
        """
        img_list = ([image_path] if isinstance(image_path, str) else list(image_path or []))
        lbl_list = ([label_path] if isinstance(label_path, str) else list(label_path or []))
        img_list = [p for p in img_list if p]
        lbl_list = [p for p in lbl_list if p]
        single_img = img_list[-1] if img_list else ''
        single_lbl = lbl_list[-1] if lbl_list else ''
        info_list = self.get_project_info()
        target = None
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                target = info
                break
        if target is None:
            self.add_project_info({
                'project_name': project_name,
                'dataset_name': dataset_name,
                'image_path': single_img,
                'label_path': single_lbl,
                'label_fmt': label_fmt,
                'image_paths': img_list,
                'label_paths': lbl_list,
                'labeled': labeled if labeled is not None else 0,
                'total': total if total is not None else 0,
            })
            return True
        target['image_path'] = single_img
        target['label_path'] = single_lbl
        target['label_fmt'] = label_fmt
        img_paths = list(target.get('image_paths') or [])
        for p in img_list:
            if p not in img_paths:
                img_paths.append(p)
        target['image_paths'] = img_paths
        lbl_paths = list(target.get('label_paths') or [])
        for p in lbl_list:
            if p not in lbl_paths:
                lbl_paths.append(p)
        target['label_paths'] = lbl_paths
        if labeled is not None:
            target['labeled'] = ((target.get('labeled') or 0) + labeled) if append else labeled
        if total is not None:
            target['total'] = ((target.get('total') or 0) + total) if append else total
        self.update_project_info(info_list)
        return True

    def clear_dataset_import(self, project_name, dataset_name):
        """清空数据集的导入绑定与统计（数据集移动后源数据集无数据）。"""
        info_list = self.get_project_info()
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                info['image_path'] = ''
                info['label_path'] = ''
                info['label_fmt'] = ''
                info['image_paths'] = []
                info['label_paths'] = []
                info['labeled'] = 0
                info['total'] = 0
                self.update_project_info(info_list)
                return True
        return False

    def move_deleted_images(self, src_project, src_dataset,
                            dst_project, dst_dataset):
        """迁移"已删除/不加载"图像记录：src → dst（dst 追加，src 清空）。"""
        key = keys.deleted_images
        txn = self.mdb.begin(write=True)
        maps = txn.get(key)
        if maps is None:
            maps = {}
        else:
            maps = json.loads(maps.decode())
        src_set = list(maps.get(src_project, {}).get(src_dataset, []))
        if src_set:
            dst_set = maps.setdefault(dst_project, {}).setdefault(dst_dataset, [])
            for p in src_set:
                if p not in dst_set:
                    dst_set.append(p)
        maps.get(src_project, {}).pop(src_dataset, None)
        if not maps.get(src_project, {}):
            maps.pop(src_project, None)
        txn.put(key, json.dumps(maps).encode())
        txn.commit()

    def get_dataset_import(self, project_name, dataset_name):
        """
        返回该数据集导入绑定：
        {'image_path','label_path','label_fmt','labeled','total',
         'image_paths': [...], 'label_paths': [...]}
         """
        for info in self.get_project_info():
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                return {
                    'image_path': info.get('image_path', ''),
                    'label_path': info.get('label_path', ''),
                    'label_fmt': info.get('label_fmt', ''),
                    'labeled': info.get('labeled', 0),
                    'total': info.get('total', 0),
                    'image_paths': list(info.get('image_paths') or [])
                                   or ([info.get('image_path', '')] if info.get('image_path') else []),
                    'label_paths': list(info.get('label_paths') or [])
                                   or ([info.get('label_path', '')] if info.get('label_path') else []),
                }
        return {}

    def get_dataset_labels(self, project_name, dataset_name):
        """返回该数据集标签映射 {标签名: 颜色#hex}。"""
        for info in self.get_project_info():
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                return dict(info.get('labels') or {})
        return {}

    def save_dataset_label_counts(self, project_name, dataset_name, counts):
        """持久化数据集标签数量统计 {标签名: 数量},供属性页无缓存时展示。"""
        info_list = self.get_project_info()
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                info['label_counts'] = dict(counts)
                self.update_project_info(info_list)
                return True
        return False

    def get_dataset_label_counts(self, project_name, dataset_name):
        """返回该数据集标签数量统计 {标签名: 数量},无则 {}。"""
        for info in self.get_project_info():
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                return dict(info.get('label_counts') or {})
        return {}

    def save_dataset_labels(self, project_name, dataset_name, labels):
        """整体保存该数据集标签映射 {标签名: 颜色#hex}。"""
        info_list = self.get_project_info()
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                info['labels'] = dict(labels)
                self.update_project_info(info_list)
                return True
        return False

    def get_dataset_label_ids(self, project_name, dataset_name):
        """返回该数据集 class_id→标签名 映射 {str_id: 标签名}(YOLO txt 数字 id 的显示名)。"""
        for info in self.get_project_info():
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                return dict(info.get('label_ids') or {})
        return {}

    def save_dataset_label_ids(self, project_name, dataset_name, ids):
        """整体保存 {str_id: 标签名}。"""
        info_list = self.get_project_info()
        for info in info_list:
            if (info.get('project_name') == project_name
                    and info.get('dataset_name') == dataset_name):
                info['label_ids'] = dict(ids)
                self.update_project_info(info_list)
                return True
        return False

    def add_dataset_label(self, project_name, dataset_name, label_name, color):
        """添加/更新单个标签及其颜色。"""
        labels = self.get_dataset_labels(project_name, dataset_name)
        labels[label_name] = color
        return self.save_dataset_labels(project_name, dataset_name, labels)

    def remove_dataset_label(self, project_name, dataset_name, label_name):
        """删除该数据集的单个标签（不存在返回 False）。"""
        labels = self.get_dataset_labels(project_name, dataset_name)
        if label_name in labels:
            del labels[label_name]
            return self.save_dataset_labels(project_name, dataset_name, labels)
        return False

    # ---------- 训练记录 ----------
    def add_train_record(self, record):
        """追加一条训练记录（record 为 dict，见 main 训练启动处）。"""
        key = keys.train_history
        txn = self.mdb.begin(write=True)
        recs = txn.get(key)
        recs = json.loads(recs.decode()) if recs else []
        recs.append(record)
        txn.put(key, json.dumps(recs).encode())
        txn.commit()

    def get_train_records(self):
        key = keys.train_history
        txn = self.mdb.begin(write=False)
        recs = txn.get(key)
        if recs is None:
            return []
        try:
            return json.loads(recs.decode())
        except Exception:
            return []

    def delete_train_record(self, record_id):
        """按 id 删除一条训练记录。"""
        key = keys.train_history
        txn = self.mdb.begin(write=True)
        data = txn.get(key)
        recs = json.loads(data.decode()) if data else []
        new_recs = [r for r in recs if r.get("id") != record_id]
        if len(new_recs) != len(recs):
            txn.put(key, json.dumps(new_recs, ensure_ascii=False).encode())
        txn.commit()

    def update_train_record(self, record):
        """按 id 覆盖一条训练记录（训练中实时更新 metrics 等字段）。"""
        key = keys.train_history
        txn = self.mdb.begin(write=True)
        data = txn.get(key)
        recs = json.loads(data.decode()) if data else []
        rid = record.get("id")
        for i, r in enumerate(recs):
            if r.get("id") == rid:
                recs[i] = record
                break
        else:
            recs.append(record)
        txn.put(key, json.dumps(recs).encode())
        txn.commit()

    # ---------- 模型记录(独立于训练记录存储) ----------
    def add_model_record(self, record):
        """追加一条模型记录(有模型文件的训练)。"""
        key = keys.model_history
        txn = self.mdb.begin(write=True)
        recs = txn.get(key)
        recs = json.loads(recs.decode()) if recs else []
        recs.append(record)
        txn.put(key, json.dumps(recs, ensure_ascii=False).encode())
        txn.commit()

    def get_model_records(self):
        key = keys.model_history
        txn = self.mdb.begin(write=False)
        recs = txn.get(key)
        if recs is None:
            return []
        try:
            return json.loads(recs.decode())
        except Exception:
            return []

    def delete_model_record(self, record_id):
        """按 id 删除一条模型记录(不影响训练记录)。"""
        key = keys.model_history
        txn = self.mdb.begin(write=True)
        data = txn.get(key)
        recs = json.loads(data.decode()) if data else []
        new_recs = [r for r in recs if r.get("id") != record_id]
        if len(new_recs) != len(recs):
            txn.put(key, json.dumps(new_recs, ensure_ascii=False).encode())
        txn.commit()

    def update_model_record(self, record):
        """按 id 覆盖一条模型记录。"""
        key = keys.model_history
        txn = self.mdb.begin(write=True)
        data = txn.get(key)
        recs = json.loads(data.decode()) if data else []
        rid = record.get("id")
        for i, r in enumerate(recs):
            if r.get("id") == rid:
                recs[i] = record
                break
        else:
            recs.append(record)
        txn.put(key, json.dumps(recs, ensure_ascii=False).encode())
        txn.commit()

    # ---------- 训练/模型记录级联删除 ----------
    def migrate_model_records(self):
        """一次性迁移:train_history 中带模型的历史记录补录到 model_history(幂等)。"""
        txn = self.mdb.begin(write=True)
        existing = txn.get(keys.model_history)
        existing = json.loads(existing.decode()) if existing else []
        if existing:
            txn.commit()
            return
        data = txn.get(keys.train_history)
        recs = json.loads(data.decode()) if data else []
        added = False
        for r in recs:
            if r.get("model_path") and r.get("end_time"):
                m = dict(r)
                m["id"] = "{}-{}".format(uuid.uuid4().hex[:12], int(time.time() * 1000) % 100000)
                m["train_id"] = r.get("id")
                existing.append(m)
                added = True
        if added:
            txn.put(keys.model_history, json.dumps(existing, ensure_ascii=False).encode())
        txn.commit()

    def delete_project_records(self, project_name):
        """删除项目下所有训练记录与模型记录。"""
        txn = self.mdb.begin(write=True)
        for key in (keys.train_history, keys.model_history):
            data = txn.get(key)
            recs = json.loads(data.decode()) if data else []
            new_recs = [r for r in recs if r.get("project") != project_name]
            if len(new_recs) != len(recs):
                txn.put(key, json.dumps(new_recs, ensure_ascii=False).encode())
        txn.commit()

    def dataset_in_records(self, project_name, dataset_name):
        """该数据集是否被训练记录引用(训练集或验证集任一出现)。

        model_history 是 train_history 的子集(训练完成时浅拷贝),无需重复检查。
        """
        key = keys.train_history
        txn = self.mdb.begin(write=False)
        data = txn.get(key)
        recs = json.loads(data.decode()) if data else []
        for r in recs:
            if r.get("project") != project_name:
                continue
            for field in ("dataset", "val_dataset"):
                names = [x.strip() for x in str(r.get(field, "")).split(",") if x.strip()]
                if any(_ds_of(n) == dataset_name for n in names):
                    return True
        return False

    def _strip_dataset_from_record(self, record, ds_name):
        """从记录中移除 ds_name,返回 (record, 是否仍被其他数据集引用)。"""
        def _strip(field):
            names = [x.strip() for x in str(record.get(field, "")).split(",") if x.strip()]
            return [n for n in names if _ds_of(n) != ds_name]

        train = _strip("dataset")
        val = _strip("val_dataset")
        record["dataset"] = ", ".join(train)
        record["val_dataset"] = ", ".join(val)
        if train or val:
            info = str(record.get("dataset_info", ""))
            if info:
                items = [x.strip() for x in info.split(",") if x.strip()]
                items = [n for n in items if _ds_of(n) != ds_name]
                record["dataset_info"] = ", ".join(items)
        return record, bool(train or val)

    def remove_dataset_from_records(self, project_name, ds_name):
        """数据集删除时从训练/模型记录中移除该数据集;记录无任何引用则删除。"""
        txn = self.mdb.begin(write=True)
        for key in (keys.train_history, keys.model_history):
            data = txn.get(key)
            recs = json.loads(data.decode()) if data else []
            new_recs = []
            changed = False
            for r in recs:
                if r.get("project") != project_name:
                    new_recs.append(r)
                    continue
                # 元素可能带空格("A/2, A/4"),须 strip 后再比
                train_names = [x.strip() for x in str(r.get("dataset", "")).split(",") if x.strip()]
                val_names = [x.strip() for x in str(r.get("val_dataset", "")).split(",") if x.strip()]
                if not any(_ds_of(n) == ds_name for n in train_names + val_names):
                    new_recs.append(r)
                    continue
                r, still_used = self._strip_dataset_from_record(r, ds_name)
                changed = True
                if still_used:
                    new_recs.append(r)
            if changed:
                txn.put(key, json.dumps(new_recs, ensure_ascii=False).encode())
        txn.commit()


if __name__ == '__main__':
    db = DataBase(r'C:/Users/admin/.easy2yolo')
    print(db.get_project_info())

