# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from app.core.utils import project_root

WORKSPACE_DIRECTORY = project_root()
LOG_FILE = os.path.join(WORKSPACE_DIRECTORY, "logs", "app.log")

MAX_LINES = 1000   # 日志界面最多保留行数(超过删除最老)
MAX_LINE_CHARS = 4000   # 单条日志上限: 进度条整段攒成一条能到几百 KB

_logger = None
_log_dialog = None


def get_logger():
    global _logger
    if _logger is None:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        logger = logging.getLogger("easy_trainer")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            # 按天分割
            fh = TimedRotatingFileHandler(
                LOG_FILE, when="midnight", encoding="utf-8", backupCount=0)
            fh.setFormatter(logging.Formatter(
                "[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
            logger.addHandler(fh)
        _logger = logger
    return _logger


def register_log_dialog(dlg):
    """注册常驻日志对话框(app 启动时创建, 隐藏也接收日志)."""
    global _log_dialog
    _log_dialog = dlg


def _shrink(msg):
    """进度条用 \r 原地刷新, 一整段攒成一条能有几百 KB; 每行只留最后一次刷新的状态."""
    if "\r" in msg:
        kept = []
        for ln in msg.split("\n"):
            segs = [s for s in ln.split("\r") if s.strip()]
            kept.append(segs[-1] if segs else "")
        msg = "\n".join(kept)
    if len(msg) > MAX_LINE_CHARS:
        msg = msg[:MAX_LINE_CHARS] + " …(截断 {} 字符)".format(
            len(msg) - MAX_LINE_CHARS)
    return msg


def write_log(msg):
    """写文件 + 写入常驻日志界面(无论是否显示)."""
    msg = _shrink(msg)
    line = "[{}] {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    get_logger().info(msg)
    dlg = _log_dialog
    if dlg is not None:
        dlg.append(line)
