import os
import time
from pymongo import MongoClient
import concurrent.futures

# Setting up the MongoDB connection
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=True)  # Utilizing connection pooling
db = cluster['prod']
timeseries_collection = db['tokens-timeseries-5m-interval-28h-expiry']

LOG_TAG = ['jupiter_timeseries_cron.update_tokens_timeseries']
def insert_documents(documents, start_time):
    if documents:
        timeseries_collection.insert_many(documents, ordered=False)
        print(f"{LOG_TAG} Batch inserted after: {time.time() - start_time:.2f} seconds")

def update_tokens_timeseries(jupiter_data, start_time):
    documents = []
    batch_size = 30000
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for data in jupiter_data:
            mint_address = data['mint_address']
            created_at = data['created_at']
            price = data['price']

            document = {
                'mint_address': mint_address,
                'created_at': created_at,
                'price': price
            }
            documents.append(document)

            if len(documents) == batch_size:
                futures.append(executor.submit(insert_documents, documents, start_time))
                documents = []

        # Execute any remaining operations in the batch
        if documents:
            futures.append(executor.submit(insert_documents, documents, start_time))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)