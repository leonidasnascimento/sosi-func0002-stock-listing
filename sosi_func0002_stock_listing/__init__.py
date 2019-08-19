import datetime
import logging
import azure.functions as func

from typing import List
from configuration_manager.reader import reader
from crawler import stock_listing_crawler

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # Loading configurations
    configObj = reader('', '')
    
    # Crawling
    crawlerObj = stock_listing_crawler()
    returnList = crawlerObj.getStockList()

    # Saving output and logging the operation
    # Commiting to a database

    # if mytimer.past_due:
    #     logging.info('The timer is past due!')

    # logging.info('Python timer trigger function ran at %s', utc_timestamp)
    pass