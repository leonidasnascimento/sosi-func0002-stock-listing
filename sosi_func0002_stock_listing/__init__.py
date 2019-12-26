import datetime
import logging
import azure.functions as func
import json
import requests
import pathlib
import threading

from typing import List
from configuration_manager.reader import reader
from .crawler import stock_listing_crawler
from .models.stock import stock
from azure.storage.blob import (
    Blob,
    BlockBlobService,
    PublicAccess
)

SETTINGS_FILE_PATH = pathlib.Path(
    __file__).parent.parent.__str__() + "//local.settings.json"

def main(TimerJobSosiMs0002StockListing: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:
        logging.info("'TimerJobSosiMs0002StockListing' has begun")

        config_obj: reader = reader(SETTINGS_FILE_PATH, 'Values')
        next_service_url: str = config_obj.get_value("NEXT_SERVICE_URL")
        func_key_header: str = config_obj.get_value("X_FUNCTION_KEY")
        service_upd_cache_server: str = config_obj.get_value("SERVICE_UPD_CACHE_SERVER")
        
        # Crawling
        logging.info("Getting stock list. It may take a while...")
        stock_list: list = stock_listing_crawler().get_stock_list()

        if not stock_list or len(stock_list) == 0:
            logging.warning("No stock code was found to process...")
        else:
            for s in stock_list:
                obj: stock = s 

                logging.info("Sending '{}' for next processing step...".format(obj.code))
                json_obj = json.dumps(obj.__dict__)

                # Ain't gonna wait for any response. At first, we will not care about this. Just going forward
                threading.Thread(target=next_step, args=(next_service_url, json_obj, func_key_header)).start()

            # In the end of all processing, ask for MS to update cache server... We are not caring whether all data was processed or not here.
            threading.Thread(target=update_cache_server, args=(service_upd_cache_server)).start()
        
        logging.info("Timer job is done. Waiting for the next execution time")

        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass

def next_step(url, json, func_key_header):
    headers = {
        'content-type': "application/json",
        'x-functions-key': func_key_header,
        'cache-control': "no-cache"
    }

    requests.request("POST", url, data=json, headers=headers)
    pass

def update_cache_server(url: str):
    if (url != ""):    
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        requests.request("PUT", url, headers=headers)
        pass
    pass