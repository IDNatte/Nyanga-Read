"""File Downloader"""

import requests
import os


class FileDownload:
    def __init__(self, link, file_name, dist):
        self.link = link
        self.filetarget = os.path.join(dist, file_name)

    def downloadFile(self):
        file = requests.get(self.link, stream=True)
        if file.status_code == 200:
            with open(self.filetarget, "wb") as download:
                download.write(file.content)
