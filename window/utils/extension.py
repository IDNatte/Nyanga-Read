from server.helper.constant.constant import EXTENSION_CLIENT

import requests
import time


# def get_csrf():
#     """
#     get csrf from nyanga, delay for server thread start is .5 seconds
#     """

#     print(EXTENSION_CLIENT)

#     time.sleep(0.5)
#     get = requests.get(
#         "http://localhost:5000/extension/my_manga",
#         headers={"User-Agent": EXTENSION_CLIENT},
#     )
#     return get.json()


def get_manga():
    """
    get local manga lists
    """
    time.sleep(0.5)
    manga = requests.get(
        "http://localhost:5000/extension/my_manga",
        headers={"User-Agent": EXTENSION_CLIENT},
    )
    return manga.json()


def search_manga(manga_name):
    """
    get local manga lists
    """
    time.sleep(0.5)
    manga = requests.get(
        f"http://localhost:5000/extension/search_manga?title={manga_name}",
        headers={"User-Agent": EXTENSION_CLIENT},
    )
    return manga.json()
