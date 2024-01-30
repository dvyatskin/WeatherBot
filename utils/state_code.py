import requests


def check(way):
    result = requests.get(way)
    if result.status_code == 200:
        return result.json()