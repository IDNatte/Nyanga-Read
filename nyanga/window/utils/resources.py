import os
import sys


def get_resources(relative_path):
    dev_mode = os.environ.get("APP_ENV", default=None)
    ui_dev_mode = os.environ.get("UI_APP_DEV", default=None)
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if dev_mode or ui_dev_mode:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "../../", relative_path)
    else:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
