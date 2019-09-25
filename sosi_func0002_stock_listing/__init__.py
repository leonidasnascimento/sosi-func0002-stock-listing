import datetime
import logging
import azure.functions as func
import json
import requests
import os

from typing import List
from .configuration_manager.reader import reader
from .crawler import stock_listing_crawler
from azure.storage.blob import (
    Blob,
    BlockBlobService,
    PublicAccess
)

SETTINGS_FILE_PATH = os.path.realpath("local.settings.json")

def upload_blob(blob_name: str, data: str):
    configObj = reader(SETTINGS_FILE_PATH, 'Values')

    # Saving output and logging the operation
    # Create the BlockBlockService that is used to call the Blob service for the storage account.
    block_blob_service = BlockBlobService(
        account_name=configObj.get_value('AzureBlobAccountName'),
        account_key=configObj.get_value('AzureBlobAccountKey')
    )

    # Create a container called 'quickstartblobs'.
    container_name = configObj.get_value('AzureContainerName')
    block_blob_service.create_container(container_name, fail_on_exist=False)

    # Set the permission so the blobs are public.
    block_blob_service.set_container_acl(
        container_name, public_access=PublicAccess.Container)

    # Uploading list
    block_blob_service.create_blob_from_text(container_name, blob_name, data)
    pass


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:
        configObj = reader(SETTINGS_FILE_PATH, 'Values')

        # Crawling
        crawlerObj = stock_listing_crawler()
        stockList = crawlerObj.getStockList()

        for s in stockList:
            jsonAux = json.dumps(stockList.get(s))

            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "652ec406-7b16-40ca-8436-5baf1d36b793"
            }

            response: requests.Response = requests.request("POST", configObj.get_value(
                "StockListingServiceEndPoint"), data=jsonAux, headers=headers)

            blob_data = ('STATUS => ' + str(response.status_code) +
                         '\nREASON => ' + str(response.reason) +
                         '\nMESSAGE => ' + str(response.text) +
                         '\n\n' + jsonAux)
            upload_blob(s, blob_data)
        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass
