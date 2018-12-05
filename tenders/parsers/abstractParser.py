import requests
import sqlite3

from abc import ABCMeta, abstractmethod
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from threading import Thread


class TenderIsExpired(Exception):
    def __init__(self):
        super().__init__()


class AbstractParser(Thread):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()
        self.setDaemon(True)
        self.keywords = []
        self.search_line = ''
        self.results = 0

    def init_keywords(self, keywords):
        self.keywords = keywords

    def run(self):
        for keyword in self.keywords:
            self.init_search_line(keyword)
            while True:
                try:
                    html = self.get_response_content()
                    soup = self.make_soup(html)
                    self.search_on_current_page(soup)
                    self.go_to_next_page()
                except TenderIsExpired:
                    break
            print(keyword+' finished')
            print(str(self.results)+' found')
        print('search finished')

    @abstractmethod
    def init_search_line(self, keyword):
        pass

    def get_response_content(self) -> str:
        response = requests.get(self.search_line, headers={'User-Agent': UserAgent().chrome})
        return response.content.decode('UTF-8')

    @abstractmethod
    def go_to_next_page(self):
        pass

    def make_soup(self, response_content) -> BeautifulSoup:
        soup = BeautifulSoup(response_content, 'html.parser')
        return soup

    @abstractmethod
    def search_on_current_page(self, soup):
        pass

    def create_tender(self, url, description, customer, bid_sum, created, deadline, loaded, on_delete):
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('select id from tenders_tender order by id desc')
        result = cursor.fetchall()
        if len(result) == 0:
            _id = 1
        else:
            _id = int(result[0][0]) + 1
        text = 'insert into tenders_tender values(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        text = text % (str(_id), url, description, customer, str(bid_sum), created, deadline, loaded, str(on_delete))
        cursor.execute(text)
        conn.commit()
