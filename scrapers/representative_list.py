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
        # as_ = self._soup.select('ul.deputies > li > div > a')
        # print(as_)

    def scrape(self) -> None:
        """Scrape deputies (representatives) links from a term of office."""
        self.__get_a_href()

    def __get_a_href(self):
        """
        Get list of href (link's destination) attributes from a (HTML hyperlink).
        :param elements: list of HTML elements
        """
        for a in self._soup.select('ul.deputies > li > div > a'):
            # update part href to the full URL
            self.result.append(urljoin(self.url, a.get('href'))) if a.get('href') else None

    def scrape_representatives(self, get_dynamic=False):
        for url in self.result:
            representative = Representative(url, get_dynamic)
            representative.scrape()
            self.representatives_result.append(representative.result)


if __name__ == '__main__':
    rl = RepresentativeList()
    # get representative links
    rl.scrape()

    # get info from representatives
    rl.scrape_representatives(True)
    # save to json
    rl.save_data_to_json(rl.representatives_result)
