import os
import sys

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))
_pretrained_dir = os.path.join(WORKSPACE_DIRECTORY, 'pretrained')
if 'RF_HOME' not in os.environ and os.path.isdir(_pretrained_dir):
    os.environ['RF_HOME'] = _pretrained_dir

from app.main_window import main

main()
