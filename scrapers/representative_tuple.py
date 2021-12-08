from scraper import Scraper
from bs4 import BeautifulSoup
import bs4


# extract a (HTML hyperlink) from provided list of HTML elements
def _extract_a(elements: bs4.element.ResultSet) -> list:
    return [e.select_one('a') for e in elements]


class RepresentativeTuple(Scraper):

    def __init__(self, url: str = "https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A"):
        super().__init__(url)
        self._scrape()

    def _scrape(self):
        uls = self.__get_deputies_uls()
        representative_hyperlinks = _extract_a(uls)
        self.__make_tuple(representative_hyperlinks)

    # get list of ul (HTML unordered list) elements containing deputies (representatives) class
    def __get_deputies_uls(self) -> bs4.element.ResultSet:
        return self._soup.select('ul.deputies')

    def __make_tuple(self, hyperlinks: list) -> None:
        self.generator = (a['href'] for a in hyperlinks)


if __name__ == '__main__':
    rl = RepresentativeTuple()
    for r in rl.generator:
        print(r)
