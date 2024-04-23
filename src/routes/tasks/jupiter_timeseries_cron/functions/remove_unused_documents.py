import os
from pymongo import MongoClient, DeleteOne

LOG_TAG = ['jupiter_timeseries_cron.remove_unused_documents']

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
collection = db['tokens-timeseries']

def remove_unused_documents(mongo_token_address_list, mongo_tokens_timeseries_address_list):
    # Prepare bulk operations
    operations = []
    
    for address in mongo_tokens_timeseries_address_list:
        if address not in mongo_token_address_list:
            operations.append(DeleteOne({'mint_address': address}))

    # Execute bulk operations if there are any deletions to make
    if operations:
        result = collection.bulk_write(operations)
        print(f'{LOG_TAG} Old tokens removed. Count: {result.deleted_count}')
    else:
        print(f'{LOG_TAG} No tokens to remove')

