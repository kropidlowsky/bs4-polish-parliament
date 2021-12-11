import helper
import abc
from bs4 import BeautifulSoup


class Scraper(abc.ABC):
    def __init__(self, url: str):
        self.url: str = url
        self._soup: BeautifulSoup = helper.get_soup(helper.get_response(self.url))

    @abc.abstractmethod
    # scrape website to collect data
    def _scrape(self) -> None:
        pass

    @abc.abstractmethod
    # prepare desired result
    def _prepare_result(self, data) -> None:
        pass
