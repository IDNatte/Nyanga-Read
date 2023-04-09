import requests
import sys
import os

from utils.file_download import FileDownload


class Api:
    def __init__(self):
        self.mangaBaseLink = "https://api.mangadex.org"
        self.coverBaseLink = "https://uploads.mangadex.org/covers"
        self.chapteBaseLink = "https://api.mangadex.org/at-home/server"

        self.localEntry = os.path.join(os.path.expanduser("~"), ".nyanga-debug")
        self.localEntryData = os.path.join(
            os.path.expanduser("~"), ".nyanga-debug/data"
        )
        self.localEntryCacheImage = os.path.join(
            os.path.expanduser("~"), ".nyanga-debug/cache/image"
        )

        if not os.path.isdir(self.localEntry):
            os.makedirs(self.localEntry, exist_ok=True)
            os.makedirs(self.localEntryData, exist_ok=True)
            os.makedirs(self.localEntryCacheImage, exist_ok=True)

    def initManga(self, lang):
        mangaUrl = f"{self.mangaBaseLink}/manga?&originalLanguage[]=ja&excludedTags[]=5920b825-4181-4a17-beeb-9918b0ff7a30&includes[]=cover_art&availableTranslatedLanguage[]={lang}&limit=3&offset=0"
        try:
            manga = requests.get(mangaUrl)

            if manga.status_code == 200:
                mangaData = manga.json()

                MANGA_DATA = []

                for content in mangaData.get("data"):
                    for cover in content.get("relationships"):
                        if cover.get("type") == "cover_art":
                            FileDownload(
                                f"{self.coverBaseLink}/{content.get('id')}/{cover.get('attributes').get('fileName')}",
                                cover.get("attributes").get("fileName"),
                                self.localEntryCacheImage,
                            ).downloadFile()

                            MANGA_DATA.append(
                                {
                                    "manga": {
                                        "title": (
                                            content.get("attributes")
                                            .get("title")
                                            .get("en", None)
                                            if content.get("attributes")
                                            .get("title")
                                            .get("en", None)
                                            != None
                                            else content.get("attributes")
                                            .get("title")
                                            .get("ja", None)
                                        ),
                                        "id": content.get("id"),
                                        "description": str(
                                            content.get("attributes")
                                            .get("description")
                                            .get("en", None)
                                            if content.get("attributes")
                                            .get("description")
                                            .get("en", None)
                                            != None
                                            else content.get("attributes")
                                            .get("description")
                                            .get("ja", None)
                                        ),
                                    },
                                    "cover": {
                                        "localUrl": os.path.join(
                                            self.localEntryCacheImage,
                                            cover.get("attributes").get("fileName"),
                                        )
                                    },
                                }
                            )

                return MANGA_DATA

        except Exception as Error:
            print(f"some error : {Error}")
            return []

    def ready(self):
        return {"message": f"Hello from python {sys.version_info}"}

    def getSvelteVersion(self, svelte_version):
        print(f"using svelte version {svelte_version}")
