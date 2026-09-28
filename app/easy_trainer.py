import os
import sys

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIRECTORY = os.path.dirname(CURRENT_DIRECTORY)
sys.path.append(WORKSPACE_DIRECTORY)
sys.path.append(os.path.join(WORKSPACE_DIRECTORY, 'ui'))

from app.main_window import main

main()
