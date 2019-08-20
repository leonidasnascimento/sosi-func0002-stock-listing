import urllib3

from typing import List
from sosi_func0002_stock_listing.models.stock import stock
from bs4 import BeautifulSoup

class stock_listing_crawler():
    companies_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    site_url = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'

    def __init__(self):
        pass
    
    def getStockList(self) -> []:
        returnObj = []

        for index in self.companies_index:
            url = self.site_url.format(index)
            req = urllib3.PoolManager()
            res = req.request('GET', url)
            soup = BeautifulSoup(res.data, 'html.parser')
            table_id_aux = str('id_{}').format(index)
            stocks = soup.find('table', {'id': table_id_aux}).findAll('tr')

            # If not empty or null
            if not (stocks): continue

            # Removing header
            del stocks[0]
            
            for s in stocks:
                stockRow = s.findAll('td')

                if not stockRow: continue

                stock_code = stockRow[0].text
                company = stockRow[1].text 
                returnObj.append(stock(stock_code, company, ''))
            pass

        return returnObj
    pass