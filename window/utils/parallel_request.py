import requests


def parallelize_req(url):
    parallel_executor = requests.get(url)
    return parallel_executor.json()
