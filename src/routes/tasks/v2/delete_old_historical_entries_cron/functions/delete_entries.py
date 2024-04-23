import os
from pymongo import MongoClient
import time

# Connect to MongoDB
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
collection = db['tokens-timeseries']

LOGTAG = ['delete_old_historical_entries.delete_entries']

def delete_entries():
    # Calculate the cutoff time (24 hours ago)
    current_time = int(time.time())
    cutoff_time = current_time - 28 * 3600
    
    # Update documents to remove historical entries older than 24 hours
    result = collection.update_many(
        {},
        {
            '$pull': {
                'historical': {
                    'created_at': {'$lt': cutoff_time}
                }
            }
        }
    )
    
    print(f"{LOGTAG} Documents updated: {result.modified_count}")