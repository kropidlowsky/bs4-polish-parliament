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
        self._make_soup()
        self.result = None

    @abc.abstractmethod
    def _scrape(self) -> None:
        """
        Scrape website to collect data.
        :return: None
        """
        pass

    def _make_soup(self, html=None) -> None:
        if not html:
            html = helper.get_response(self.url)
            self._soup: BeautifulSoup = helper.get_soup(html)
        else:
            # selenium
            self._soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
