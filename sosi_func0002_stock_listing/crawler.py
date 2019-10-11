import urllib3
import datetime

from typing import List
from .models.stock import stock
from bs4 import (BeautifulSoup, ResultSet)

class stock_listing_crawler():
    companies_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    stock_list_url = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'

    def __init__(self):
        pass
    
    def get_stock_list(self) -> dict:
        returnDict = dict()

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
            if not (stocks): continue

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

                if not stock_code_details_crawler().enrich(stock_obj):
                    continue

                if not stock_available_volume_cvm_code_crawler().enrich(stock_obj):
                    continue

                returnDict[stock_obj.code] = stock_obj.__dict__

                #Remove this
                return returnDict
            pass

        return returnDict
    pass

class stock_code_details_crawler():
    stock_det_url = "https://br.advfn.com/bolsa-de-valores/bovespa/{}/cotacao"
      
    def __init__(self):
        pass

    def enrich(self, stock_ref: stock) -> bool:
        url_det = str(self.stock_det_url).format(stock_ref.code)
        req = urllib3.PoolManager()
        res = req.request('GET', url_det)
        soup = BeautifulSoup(res.data, 'html.parser')
        divs_details = soup.find_all('div', {'class': 'TableElement'})

        if (not (divs_details is None)) and len(divs_details) > 0:
            div_1_det = divs_details[0].find('table').findAll('td')
            div_2_det = divs_details[2].find('table').findAll('td')
            
            stock_ref.detail = div_1_det[len(div_1_det) - 1].text
            stock_ref.stock_name = div_1_det[0].text
            stock_ref.isin_code = div_1_det[4].text
            stock_ref.stock_type = self.__set_stock_type(div_1_det[3].text)
            stock_ref.currency = 'BRL' # div_2_det[len(div_2_det) - 1].text

            return True

        return False
    
    def __set_stock_type(self, stock_type: str):
        if stock_type.lower() == 'preferencial':
            return 'PN'
        else:
            if stock_type.lower() == 'ordinária':
                return 'ON'
            else:
                return stock_type
        pass
    pass

class stock_available_volume_cvm_code_crawler():
    url = "https://br.advfn.com/bolsa-de-valores/bovespa/{}/empresa"
    
    def __init__(self):
        pass

    def enrich(self, stock_ref: stock) -> bool:
        url_det = str(self.url).format(stock_ref.code)
        req = urllib3.PoolManager()
        res = req.request('GET', url_det)
        soup = BeautifulSoup(res.data, 'html.parser')
        res_url = res.geturl()

        if str(res_url).__contains__('cotacao'):
            return False

        # CVM code
        cvm_row = soup.find("td", text=" Código CVM ")

        if cvm_row is not None:
            cvm_code_aux = cvm_row.find_next("td").text
            stock_ref.cvm_code = str(cvm_code_aux).strip()
        else:
            return False

        # Stock volume
        
        on_share_row = soup.find("td", text="Ações Ordinárias")
        pn_share_row = soup.find("td", text="Ações Preferenciais")

        if on_share_row is not None and pn_share_row is not None:
            on_share = on_share_row.find_next("td").text.strip().replace('.', '')
            pn_share = pn_share_row.find_next("td").text.strip().replace('.', '')

            if(stock_ref.stock_type.upper() == 'PN'):
                stock_ref.available_volume = int(pn_share)
            else:
                stock_ref.available_volume = int(on_share)
            pass
        else:
            return False
        
        return True
    pass