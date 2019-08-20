from typing import List
from sosi_func0002_stock_listing.models.stock import stock

class stock_listing_crawler():
    companies_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    site_url = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'

    def __init__(self):
        pass
    
    def getStockList(self) -> List[stock]:
        returnObj = []

        for index in self.companies_index:
            full_url = self.site_url.format(index)
            returnObj.append(stock('', '', ''))
            pass

        return returnObj
    pass