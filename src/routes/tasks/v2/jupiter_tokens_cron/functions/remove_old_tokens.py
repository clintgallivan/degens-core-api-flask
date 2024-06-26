import os
from pymongo import MongoClient, DeleteOne

LOG_TAG = ['jupiter_tokens_cron.remove_old_tokens']

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
collection = db['tokens']

def remove_old_tokens(mongo_tokens_list, jupiter_tokens_list):
    # Prepare bulk operations
    operations = []
    
    for address in mongo_tokens_list:
        if address not in jupiter_tokens_list:
            operations.append(DeleteOne({'mint_address': address}))

    # Execute bulk operations if there are any deletions to make
    if operations:
        result = collection.bulk_write(operations)
        print(f'{LOG_TAG} Old tokens removed. Count: {result.deleted_count}')
    else:
        print(f'{LOG_TAG} No tokens to remove')


