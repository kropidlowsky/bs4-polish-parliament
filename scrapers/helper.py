import requests
from bs4 import BeautifulSoup


def get_response(url: str) -> requests.models.Response:
    return requests.get(url)


def get_soup(response: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(response.content, "html.parser")


if __name__ == "__main__":
    resp = get_response("https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A")
    print(resp)
    soup = get_soup(resp)
    print(soup)
