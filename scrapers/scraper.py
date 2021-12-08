import helper
import abc


class Scraper(abc.ABC):
    def __init__(self, url: str):
        self.url = url
        self._soup = helper.get_soup(helper.get_response(self.url))

    @abc.abstractmethod
    def _scrape(self):
        pass
