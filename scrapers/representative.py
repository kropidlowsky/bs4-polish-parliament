from selenium.webdriver import chrome

from scraper import Scraper
import bs4
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
        self.result['hrefs'] = dict()
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
        self.__get_dynamic_info()

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

    def __get_dynamic_info(self) -> None:
        if self._get_dynamic:
            self._get_selenium_driver()
            self.__click_div_hyperlinks()
            self.__click_div_hyperlinks('kontakt')
            self._make_soup(self._driver.page_source)
            self.__get_speeches()
            self.__get_actions()
            self.__get_votes()
            self.__get_email()

    def __click_div_hyperlinks(self, div_class: str = 'aktywnosc') -> None:
        """
        Click all div's hyperlinks.
        A representative website has two divs with dynamic elements:
            1) aktywnosc - standard case. New elements appear under 'content' ID.
            2) kontakt - complex case.
        :param div_class: div's class to click through
        """
        lis = self._driver.find_elements(By.CSS_SELECTOR, f'div.{div_class} ul.data li')
        for i, li in enumerate(lis):
            li.find_element(By.CSS_SELECTOR, 'a').click()
            if div_class == 'kontakt' and i >= 1:
                self.__wait_for_contact_loading(i, li)
            else:
                WebDriverWait(li, 10).until(ec.presence_of_element_located((By.ID, "content")))

    def __wait_for_contact_loading(self, i, li):
        if i == 1:
            WebDriverWait(li, 10).until(
                ec.presence_of_element_located((By.ID, "view:_id1:_id2:facetMain:_id191:holdWspInner")))
        elif i == 2:
            WebDriverWait(li, 10).until(
                ec.presence_of_element_located((By.ID, "view:_id1:_id2:facetMain:_id191:holdMajatekInner")))
        elif i == 3:
            WebDriverWait(li, 10).until(
                ec.presence_of_element_located(
                    (By.ID, "view:_id1:_id2:facetMain:_id191:holdKorzysciInner")))
        elif i == 4:
            WebDriverWait(li, 10).until(
                ec.presence_of_element_located((By.ID, "view:_id1:_id2:facetMain:_id191:_id280")))

    def __get_speeches(self):
        # Wystąpienia na posiedzeniach Sejmu
        self.result['Wypowiedzi href'] = self._soup.select_one('#content > table > tbody > tr > td > a').get('href')
        self.result['Wypowiedzi łącznie'] = self._soup.select_one('#content > table > tbody > tr > td').get_text()

    def __get_actions(self):
        # Interpelacje, zapytania, pytania w sprawach bieżących, oświadczenia
        action_div = self._soup.select_one('#view\:_id1\:_id2\:facetMain\:_id191\:holdInterpelacje')
        rows = action_div.select('tr')
        for row in rows:
            tds = row.select('td')
            if len(tds) == 3:
                left_td, right_td = tds[0], tds[1]
                left_a = left_td.select_one('a')
                self.result['hrefs'][left_a.get_text()] = left_a.get('href')
                self.result[left_a.get_text()] = right_td.get_text()

    def __get_votes(self):
        vote_div = self._soup.select_one('#view\:_id1\:_id2\:facetMain\:_id191\:holdGlosowania')
        vote_tds = vote_div.select('td')
        self.result['votes'] = dict()
        self.result['percentage'] = vote_tds[0].get_text()
        self.result['number'] = vote_tds[1].get_text()
        self.result['hrefs']['votes'] = vote_tds[2].select_one('a').get('href')

    def __get_email(self) -> None:
        self.result['email'] = self._soup.select_one('#view\:_id1\:_id2\:facetMain\:_id191\:_id280').get('href')


if __name__ == '__main__':
    # representative = Representative('https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id=001&type=A', True)
    representative = Representative('https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id=002&type=A', True)
    print(representative.result)
