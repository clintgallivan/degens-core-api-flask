from pymongo import MongoClient
import os

# Setting up the MongoDB connection
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=True)  # Utilizing connection pooling
db = cluster['prod']
timeseries_collection = db['tokens-timeseries-5m-interval-28h-expiry']

def update_tokens_timeseries(jupiter_data):
    documents = []
    for data in jupiter_data:
        # Assuming 'adx' needs to be calculated or is provided in 'data'
        mint_address = data['mint_address']
        created_at = data['created_at']
        price = data['price']

        document = {
            'mint_address': mint_address,
            'created_at': created_at,
            'price': price
        }
        documents.append(document)

        # Consider batching logic; for example, execute operations every 500 documents
        if len(documents) == 500:
            timeseries_collection.insert_many(documents, ordered=False)
            documents = []

    # Execute any remaining operations in the batch
    if documents:
        timeseries_collection.insert_many(documents, ordered=False)

# Example usage with data coming from somewhere (e.g., an API or another function)
# update_tokens_timeseries(jupiter_data)