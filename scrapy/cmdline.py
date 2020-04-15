import sys

from utils.project import get_project_settings

def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv
        
    if settings is None:
        settings = get_project_settings()
    print('cmdline.execute')