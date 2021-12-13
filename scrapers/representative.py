from scraper import Scraper
import bs4


class Representative(Scraper):
    """
    Scraper class to represent a representative (deputy) profile.
    """

    def __init__(self, url: str):
        """
        :param url: representative (deputy) profile url
        """
        super().__init__(url)
        self._scrape()
        self._prepare_result(None)

    def _scrape(self) -> None:
        """
        Scrape representative (deputy) profile url.
        """
        self.__info_div = self.__get_info_div()

    def __get_info_div(self) -> bs4.BeautifulSoup:
        """
        Get information div.
        :return: information div
        """
        return self._soup.select_one('div', {'id': 'title_content'})

    def _prepare_result(self, data) -> None:
        """
        Prepare result dict with representative (deputy) information
        :param data: None
        """
        data_uls = self.__get_data_uls()
        self.result = {
            'name': self.__get_name(),
            'picture': self.__get_picture()
        }
        self.__get_static_info(data_uls)

    def __get_name(self) -> str:
        return self.__info_div.select_one('H1').get_text()

    def __get_picture(self) -> str:
        return self.__info_div.select_one('img').get('src')

    def __get_data_uls(self) -> bs4.element.ResultSet:
        return self.__info_div.select('ul.data')

    def __get_static_info(self, elements: bs4.element.ResultSet):
        """
        Get information from static HTML elements.
        :param elements: HTML elements to loop through
        """
        for i, element in enumerate(elements):
            # avoid dynamic elements
            if i > 1:
                break
            for li in element.select('li'):
                key = li.select_one('p.left').get_text()
                if key:
                    self.result[key] = li.select_one('p.right').get_text()


if __name__ == '__main__':
    representative = Representative('https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id=001&type=A')
    print(representative.result)
