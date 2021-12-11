from scraper import Scraper
import bs4


# extract a (HTML hyperlink) from provided list of HTML elements
def _extract_a(elements: bs4.element.ResultSet) -> list:
    return [e.select_one('a') for e in elements]


class RepresentativeList(Scraper):

    def __init__(self, url: str = "https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A"):
        super().__init__(url)
        self._scrape()

    def _scrape(self) -> None:
        uls = self.__get_deputies_uls()
        representative_hyperlinks = _extract_a(uls)
        self._prepare_result(representative_hyperlinks)

    # get list of ul (HTML unordered list) elements containing deputies (representatives) class
    def __get_deputies_uls(self) -> bs4.element.ResultSet:
        return self._soup.select('ul.deputies')

    # get result (generator) with deputies (representatives) hyperlinks
    def _prepare_result(self, data) -> None:
        self.result = (a['href'] for a in data)


if __name__ == '__main__':
    rl = RepresentativeList()
    for r in rl.result:
        print(r)
