import os
import sys

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))
_pretrained_dir = os.path.join(WORKSPACE_DIRECTORY, 'pretrained')
_rfdetr_dir = os.path.join(_pretrained_dir, 'transformer')
if 'RF_HOME' not in os.environ:
    try:
        os.makedirs(_rfdetr_dir, exist_ok=True)
        os.environ['RF_HOME'] = _rfdetr_dir
    except OSError:
        pass

from app.main_window import main

main()
