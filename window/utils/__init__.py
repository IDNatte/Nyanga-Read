"""Get Resources files"""
import sys
import os


def get_resources(relative_path):
    dev_mode = os.environ.get("APP_DEV", default=None)
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if dev_mode:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "../../", relative_path)
    else:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
