import urllib3
import datetime

from typing import List
from .models.stock import stock
from bs4 import (BeautifulSoup, ResultSet)

class stock_listing_crawler():
    companies_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                       'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    stock_list_url = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'

    def __init__(self):
        pass

    def get_stock_list(self) -> list:
        return_lst: list = []

        for index in self.companies_index:
            url = self.stock_list_url.format(index)
            req = urllib3.PoolManager()
            res = req.request('GET', url)
            soup = BeautifulSoup(res.data, 'html.parser')
            table_id_aux = str('id_{}').format(index)
            stock_table = soup.find('table', {'id': table_id_aux})

            if not (stock_table):
                continue

            stocks = stock_table.findAll('tr')

            # If not empty or null
            if not (stocks):
                continue

            # Removing header
            del stocks[0]

            for s in stocks:
                stockRow = s.findAll('td')

                if not stockRow:
                    continue

                stock_obj = stock()
                stock_obj.code = stockRow[1].text
                stock_obj.date_time_operation = datetime.datetime.utcnow().replace(
                    tzinfo=datetime.timezone.utc).isoformat()

                return_lst.append(stock_obj)
            pass

        return return_lst
    pass