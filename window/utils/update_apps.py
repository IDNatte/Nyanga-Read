from packaging.version import parse as ver_parse
from .resources import get_resources

import requests
import json
import sys
import re


class Updater:
    def __init__(self):
        self.metapath = get_resources("docs/app/version.json")
        self.release_ref = "https://api.github.com/repos/IDNatte/Nyanga-Read/releases"
        with open(self.metapath) as f:
            self.app_meta = json.load(f)

    def check_update(self):
        fetch_upload_meta = requests.get(f"{self.release_ref}")
        remote_version = ver_parse(
            re.sub(re.escape("v"), "", fetch_upload_meta.json()[0].get("tag_name"))
        )
        local_version = ver_parse(
            re.sub(re.escape("v"), "", self.app_meta.get("currentVersion"))
        )

        self.assets_meta_url = fetch_upload_meta.json()[0].get("assets_url")

        return {
            "update_available": remote_version > local_version,
            "update_info": {
                "local": str(local_version),
                "remote": str(remote_version),
            },
        }

    def download_update(self):
        fetch_assets_meta = requests.get(f"{self.assets_meta_url}")
        assets = fetch_assets_meta.json()
        assets_meta = [
            assets_meta
            for assets_meta in assets
            if str(sys.platform) in assets_meta.get("name")
            and not assets_meta.get("name").endswith(".json")
        ]

        requests.get(f"{assets}")


# def update_apps():
#     with open(get_resources("docs/app/version.json")) as f:
#         test = json.load(f)

#     fetch_upload = requests.get(f"{test.get('releaseRef')}")
#     assetst_url = fetch_upload.json()[0].get("assets_url")
#     asset_list_meta = requests.get(f"{assetst_url}")
#     asset_lists = [a.get("name") for a in asset_list_meta.json()]

#     remote_version = ver_parse(
#         re.sub(re.escape("v"), "", fetch_upload.json()[0].get("tag_name"))
#     )
#     local_version = ver_parse(re.sub(re.escape("v"), "", test.get("currentVersion")))

#     print(
#         f"local < remote {local_version < remote_version} local ver {local_version}, remote ver {remote_version}"
#     )

#     # print(test.get("releaseRef"))
