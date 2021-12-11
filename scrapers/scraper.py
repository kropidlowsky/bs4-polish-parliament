import helper
import abc
from bs4 import BeautifulSoup


class Scraper(abc.ABC):
    """A class used to represent a custom web scraper"""

    def __init__(self, url: str):
        """
        :param url: url to scrape
        """
        self.url: str = url
        self._soup: BeautifulSoup = helper.get_soup(helper.get_response(self.url))

    @abc.abstractmethod
    def _scrape(self) -> None:
        """
        scrape website to collect data
        :return: None
        """
        pass

    @abc.abstractmethod
    def _prepare_result(self, data) -> None:
        """
        prepare desired result
        :param data: bs4 data to process
        :return: None
        """
        pass
