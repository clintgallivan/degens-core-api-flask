import os
import time
from pymongo import MongoClient
import concurrent.futures

# Setting up the MongoDB connection
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=True)  # Utilizing connection pooling
db = cluster['prod']
timeseries_collection = db['tokens-timeseries-5m-interval-28h-expiry']

def insert_documents(documents):
    if documents:
        timeseries_collection.insert_many(documents, ordered=False)

def update_tokens_timeseries(jupiter_data):
    documents = []
    batch_size = 500
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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
                futures.append(executor.submit(insert_documents, documents))
                documents = []

        # Execute any remaining operations in the batch
        if documents:
            futures.append(executor.submit(insert_documents, documents))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)