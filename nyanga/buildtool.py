import subprocess
from pathlib import Path

import PyInstaller.__main__


def start_ui():
    try:
        subprocess.run(
            ["yarn", "run", "svelte:dev"], cwd=Path(__file__).parent.absolute()
        )
    except KeyboardInterrupt:
        pass


def install_ui_dep():
    try:
        subprocess.run(["yarn", "install"], cwd=Path(__file__).parent.absolute())
    except KeyboardInterrupt:
        pass


def build_ui():
    try:
        subprocess.run(["yarn", "install"], cwd=Path(__file__).parent.absolute())
        subprocess.run(
            ["yarn", "run", "svelte:build"], cwd=Path(__file__).parent.absolute()
        )
    except KeyboardInterrupt:
        pass


def build_linux():
    PyInstaller.__main__.run(
        [
            f"{Path(__file__).parent.absolute()}/buildtools/specfile/Nyanga-Read-linux.spec",
            "--distpath",
            "nyanga",
        ]
    )


def build_windows():
    PyInstaller.__main__.run(
        [
            f"{Path(__file__).parent.absolute()}/buildtools/specfile/Nyanga-Read-linux.spec",
            "--distpath",
            "nyanga",
        ]
    )
