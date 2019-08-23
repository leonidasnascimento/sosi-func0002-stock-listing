import datetime
import logging
import azure.functions as func
import json

from typing import List
from configuration_manager.reader import reader
from sosi_func0002_stock_listing.crawler import stock_listing_crawler
from azure.storage.blob import (
    Blob,
    BlockBlobService,
    PublicAccess
)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    try:
        # Loading configurations
        configObj = reader('local.settings.json', 'Values')
        
        # Crawling
        crawlerObj = stock_listing_crawler()
        returnList = crawlerObj.getStockList()
        jsonObj = json.dumps(returnList)

        # Saving output and logging the operation
        # Create the BlockBlockService that is used to call the Blob service for the storage account.
        block_blob_service = BlockBlobService(
            account_name=configObj.get_value('AzureBlobAccountName'), 
            account_key=configObj.get_value('AzureBlobAccountKey')
        )

        # Create a container called 'quickstartblobs'.
        container_name = configObj.get_value('AzureContainerName')
        blob_name = configObj.get_value('AzureBlobName')
        block_blob_service.create_container(container_name, fail_on_exist=False)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(
            container_name, public_access=PublicAccess.Container)

        # Uploading list
        block_blob_service.create_blob_from_text(container_name, blob_name, str(jsonObj))

        # Commiting to a database

        # if mytimer.past_due:
        #     logging.info('The timer is past due!')

        # logging.info('Python timer trigger function ran at %s', utc_timestamp)

        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass