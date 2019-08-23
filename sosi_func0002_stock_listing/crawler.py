import urllib3
import datetime

from typing import List
from sosi_func0002_stock_listing.models.stock import stock
from bs4 import BeautifulSoup

class stock_listing_crawler():
    companies_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    site_url = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'

    def __init__(self):
        pass
    
    def getStockList(self) -> dict:
        returnDict = dict()

        for index in self.companies_index:
            url = self.site_url.format(index)
            req = urllib3.PoolManager()
            res = req.request('GET', url)
            soup = BeautifulSoup(res.data, 'html.parser')
            table_id_aux = str('id_{}').format(index)
            stock_table = soup.find('table', {'id': table_id_aux})
            
            if not (stock_table):
                continue
                
            stocks = stock_table.findAll('tr')

            # If not empty or null
            if not (stocks): continue

            # Removing header
            del stocks[0]
            
            for s in stocks:
                stockRow = s.findAll('td')

                if not stockRow: 
                    continue

                utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
                stock_code = stockRow[1].text
                company = stockRow[0].text
                details = ''

                stockObj = stock(stock_code, company, details, utc_timestamp)

                returnDict[stockObj.code] = stockObj.__dict__
            pass

        return returnDict
    pass