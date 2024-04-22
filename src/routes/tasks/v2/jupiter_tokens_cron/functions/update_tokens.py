from pymongo import MongoClient, UpdateOne
from datetime import datetime, timezone
import os

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
timeseries_collection = db['tokens']

def update_tokens(jupiter_data):
    operations = []
    for data in jupiter_data:
        mint_address = data.get('address')
        created_at = int(datetime.now(timezone.utc).timestamp())

        # Keys we want to update if they exist, mapped to their database field names
        data_keys = {
            'name': 'name',
            'symbol': 'symbol',
            'decimals': 'decimals',
            'logoURI': 'image_url'  # Mapping logoURI to image_url in the database
        }
        network = 'solana'

        # Create the update document dynamically
        update_doc = {
            'updated_at': created_at,
            'network': network
        }
        
        # Add keys from data_keys if they exist in data and use their mapped names
        for key, db_key in data_keys.items():
            if key in data:
                update_doc[db_key] = data[key]

        # Handling nested data (e.g., extensions)
        if 'extensions' in data and 'coingeckoId' in data['extensions']:
            update_doc['coingecko_coin_id'] = data['extensions']['coingeckoId']

        # Set up the MongoDB update operation
        operation = UpdateOne(
            {'mint_address': mint_address},
            {'$set': update_doc, '$setOnInsert': {'created_at': created_at}},
            upsert=True
        )
        operations.append(operation)

        # Perform the batch update when we have accumulated enough operations
        if len(operations) == 1000:
            timeseries_collection.bulk_write(operations)
            operations = []

    # Perform the batch update for any remaining operations
    if operations:
        timeseries_collection.bulk_write(operations)

