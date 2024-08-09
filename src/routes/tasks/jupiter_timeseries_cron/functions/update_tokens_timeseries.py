import os
import time
import requests
import json
import concurrent.futures
from datetime import datetime

# Setting up the Tinybird API details
TINYBIRD_EVENTS_API_ENDPOINT = os.getenv('TINYBIRD_EVENTS_API_ENDPOINT')
TINYBIRD_API_TOKEN = os.getenv('TINYBIRD_API_TOKEN')
DATA_SOURCE_NAME = 'tokens_timeseries_5m_interval'

LOG_TAG = ['jupiter_timeseries_cron.update_tokens_timeseries']

def insert_documents_to_tinybird(documents, start_time):
    if documents:
        # Convert the list of documents to NDJSON format
        ndjson_data = "\n".join([json.dumps(doc) for doc in documents])

        # Define the schema with jsonpath
        schema = "mint_address String `json:$.mint_address`, created_at DateTime `json:$.created_at`, price Float32 `json:$.price`"

        response = requests.post(
            TINYBIRD_EVENTS_API_ENDPOINT,
            params={
                'name': DATA_SOURCE_NAME,
                'mode': 'create',  # or 'create' if creating a new Data Source
                'schema': schema,
                'format': 'ndjson',
                'token': TINYBIRD_API_TOKEN
            },
            headers={'Content-Type': 'application/x-ndjson'},
            data=ndjson_data
        )

        if response.status_code == 202:
            print(f"{LOG_TAG} Batch inserted successfully after: {time.time() - start_time:.2f} seconds")
        else:
            print(f"{LOG_TAG} Failed to insert batch after {time.time() - start_time:.2f} seconds: {response.status_code} - {response.text}")


def update_tokens_timeseries(jupiter_data, start_time):
    documents = []
    batch_size = 50000  # Adjust this based on the size of your data and API limits
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        count = 1
        for data in jupiter_data:
            if count == 1:
                count += 1
                continue
            mint_address = data['mint_address']
            created_at = data['created_at'].isoformat()  # Convert datetime to ISO 8601 string format
            price = data['price']

            document = {
                'mint_address': mint_address,
                'created_at': created_at,  # Use the converted ISO 8601 string
                'price': price
            }
            documents.append(document)

            if len(documents) == batch_size:
                futures.append(executor.submit(insert_documents_to_tinybird, documents, start_time))
                documents = []

        # Execute any remaining operations in the batch
        if documents:
            futures.append(executor.submit(insert_documents_to_tinybird, documents, start_time))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
