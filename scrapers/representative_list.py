from scraper import Scraper
from urllib.parse import urljoin
import bs4
from representative import Representative


class RepresentativeList(Scraper):
    """
    Scraper class to represent a representative (deputy) hyperlinks list in Polish parliament per a term of office.
    """

    def __init__(self, url: str = "https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A"):
        """
        :param url: representatives (deputies) list in Polish parliament in a term of office.
        """
        super().__init__(url)
        self.representatives_result = list()
        self.result = list()

    def scrape(self) -> None:
        """Scrape deputies (representatives) links form a term of office."""
        uls = self.__get_deputies_uls()
        self.__extract_a_href(uls)

    def __get_deputies_uls(self) -> bs4.element.ResultSet:
        """Get list of ul (HTML unordered list) elements containing deputies (representatives) class."""
        return self._soup.select('ul.deputies')

    def __extract_a_href(self, elements: bs4.element.ResultSet) -> list:
        """
        Extract href (link's destination) attributes from a (HTML hyperlink) from provided list of HTML elements.
        :param elements: list of HTML elements
        :return: list of links
        """
        for a_list in (e.select("a", href=True) for e in elements):
            for a in a_list:
                # update part href to the full URL
                self.result.append(urljoin(self.url, a.get('href'))) if a.get('href') else None

    def scrape_representatives(self, get_dynamic=False):
        for url in self.result:
            representative = Representative(url, get_dynamic)
            representative.scrape()
            self.representatives_result.append(representative.result)


if __name__ == '__main__':
    rl = RepresentativeList()
    rl.scrape()
    for r in rl.result:
        print(r)
    rl.scrape_representatives(True)
    rl.save_data_to_json(rl.representatives_result)
    # print(rl.representatives_result)
    print(len(rl.result))
