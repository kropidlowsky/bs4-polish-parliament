from scraper import Scraper
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By


class Representative(Scraper):
    """
    Scraper class to represent a representative (deputy) profile.
    """

    def __init__(self, url: str, get_dynamic: bool = False):
        """
        :param url: representative (deputy) profile url
        """
        super().__init__(url)
        self._get_dynamic = get_dynamic
        self.result = dict()
        self._scrape()

    def _scrape(self) -> None:
        """
        Scrape representative (deputy) profile url.
        """
        self.__info_div = self.__get_info_div()
        self.result['name'] = self.__get_name()
        self.result['picture'] = self.__get_picture()
        data_uls = self.__get_data_uls()
        self.__get_static_info(data_uls)
        self.__get_email()

    def __get_info_div(self) -> bs4.BeautifulSoup:
        """
        Get information div.
        :return: information div
        """
        return self._soup.select_one('div', {'id': 'title_content'})

    def __get_name(self) -> str:
        return self.__info_div.select_one('H1').get_text()

    def __get_picture(self) -> str:
        return self.__info_div.select_one('img').get('src')

    def __get_data_uls(self) -> bs4.element.ResultSet:
        return self.__info_div.select('ul.data')

    def __get_static_info(self, uls: bs4.element.ResultSet):
        """
        Get information from static HTML elements.
        :param uls: HTML elements to loop through
        """
        for li in uls[0].select('li'):
            key = li.select_one('p.left').get_text()
            if key:
                self.result[key] = li.select_one('p.right').get_text()

    # def __get_dynamic_info(self):
    #     pass

    def __get_email(self):
        """
        Get email address from href value (must be parsed) to avoid using Selenium.
        """
        self.result['email'] = self.__info_div.select_one('#view\:_id1\:_id2\:facetMain\:_id191\:_id280').get('href')


if __name__ == '__main__':
    representative = Representative('https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id=001&type=A')
    print(representative.result)
