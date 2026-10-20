# -*- coding: utf-8 -*-
"""tests/ 不装包: 把仓库根目录加进 sys.path, import app.* / ui.* 直接走源码."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
