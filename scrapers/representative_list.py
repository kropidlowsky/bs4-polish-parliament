from scraper import Scraper
import bs4


def _extract_a_href(elements: bs4.element.ResultSet) -> list:
    """
    extract href (link's destination) attributes from a (HTML hyperlink) from provided list of HTML elements
    :param elements: list of HTML elements
    :return: list of links
    """
    generator_of_a_lists = (e.select("a", href=True) for e in elements)
    extract_result = []
    for a_list in generator_of_a_lists:
        for a in a_list:
            extract_result.append(a.get('href')) if a.get('href') else None
    return extract_result


class RepresentativeList(Scraper):
    """
    Scraper class to represent a representative (deputies) hyperlinks list in Polish parliament per a term of office.
    """

    def __init__(self, url: str = "https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A"):
        """
        :param url: representatives (deputies) list in Polish parliament in a term of office.
        """
        super().__init__(url)
        self._scrape()

    def _scrape(self) -> None:
        """Scrape deputies (representatives) links form a term of office."""
        uls = self.__get_deputies_uls()
        self._prepare_result(uls)

    def __get_deputies_uls(self) -> bs4.element.ResultSet:
        """Get list of ul (HTML unordered list) elements containing deputies (representatives) class."""
        return self._soup.select('ul.deputies')

    def _prepare_result(self, data) -> None:
        """
        Get result (list) with deputies (representatives) URLs.
        :param data: list of ul (HTML unordered list) elements containing deputies (representatives) class
        :return: None
        """
        self.result = _extract_a_href(data)


if __name__ == '__main__':
    rl = RepresentativeList()
    for r in rl.result:
        print(r)
    print(len(rl.result))
