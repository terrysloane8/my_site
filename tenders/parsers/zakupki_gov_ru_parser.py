import datetime

from tenders.parsers.abstractParser import AbstractParser, TenderIsExpired


class Parser(AbstractParser):
    def init_search_line(self, keyword):
        search_line1 = 'http://zakupki.gov.ru/epz/order/quicksearch/search_eis.html?searchString='
        search_line2 = '&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&ppRf615=on&af=on&currencyId=-1&regionDeleted=false&sortBy=PUBLISH_DATE'
        self.search_line = search_line1 + keyword + search_line2

    def go_to_next_page(self):
        texts = self.search_line.split('pageNumber=')
        page_number = int(texts[1][0])
        page_number += 1
        self.search_line = texts[0] + 'pageNumber=' + str(page_number) + texts[1][1:]

    def search_on_current_page(self, soup):
        objs = soup.findAll('div', attrs={'class': 'registerBox registerBoxBank margBtm20'})
        for obj in objs:
            self.parse_obj(obj)

    def parse_obj(self, obj):
        obj1 = obj.find('td', attrs={'class': 'descriptTenderTd'})
        obj1 = obj1.find('a', attrs={'target': '_blank'})
        url = obj1['href']
        if url.startswith('/'):
            url = 'http://zakupki.gov.ru' + url
        obj2 = obj.find('td', attrs={'class': 'tenderTd'})
        obj2 = obj2.findAll('dd')[1]
        obj2 = obj2.find('strong')
        try:
            text = obj2.text.strip()
            text1 = text.split(',')[0].strip().replace('\xa0', '')
            text2 = text.split(',')[1].strip()
            text = text1 + '.' + text2
            _sum = float(text)
        except AttributeError:
            _sum = 0.
        obj3 = obj.find('td', attrs={'class': 'descriptTenderTd'})
        obj3 = obj3.findAll('dd')[1]
        try:
            description = obj3.text.strip().replace('"', '\'')
        except AttributeError:
            description = ''
        obj4 = obj.find('td', attrs={'class': 'descriptTenderTd'})
        obj4 = obj4.findAll('dd')[0]
        try:
            customer = obj4.text.strip().split(':')[1].strip().replace('"', '\'')
        except AttributeError:
            customer = ''
        obj5 = obj.find('td', attrs={'class': 'amountTenderTd'})
        obj5 = obj5.find('li')
        try:
            text = obj5.text.strip().split(':')[1].strip()
            created = text.split('.')[2]+'-'+text.split('.')[1]+'-'+text.split('.')[0]
        except AttributeError:
            created = '2100-01-01'
        deadline = '2018-12-31'
        loaded = str(datetime.date.today())
        on_delete = False
        if created < '2018-11-28':
            raise TenderIsExpired()
        self.create_tender(url, description, customer, _sum, created, deadline, loaded, on_delete)

