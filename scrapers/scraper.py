import helper
import abc
from bs4 import BeautifulSoup


class Scraper(abc.ABC):
    """Abstract class used to represent a custom web scraper."""

    def __init__(self, url: str):
        """
        :param url: url to scrape
        """
        self.url: str = url
        self._soup: BeautifulSoup = helper.get_soup(helper.get_response(self.url))
        self.result = None

    @abc.abstractmethod
    def _scrape(self) -> None:
        """
        Scrape website to collect data.
        :return: None
        """
        pass
