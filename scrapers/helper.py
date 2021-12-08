import requests
from bs4 import BeautifulSoup


def get_response(url: str):
    return requests.get(url)


def get_soup(response: requests.Response):
    return BeautifulSoup(response.content, "html.parser")
