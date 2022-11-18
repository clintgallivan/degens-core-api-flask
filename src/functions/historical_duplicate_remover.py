import os
from pymongo import MongoClient, DeleteOne, UpdateOne
from pymongo.errors import BulkWriteError
from bson.objectid import ObjectId
from datetime import datetime

# cluster = MongoClient(os.getenv('MONGO_DB_SRV'))
cluster = MongoClient('mongodb+srv://cgallivan:P%40perless2020@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster["tokens"]
# collection = db["token-timeseries"]
collection = db["token-timeseries"]
# range 10/6 - 11/13


def historical_duplicate_remover(from_date=datetime(1975, 12, 12), to_date=datetime.now()):
    requests = []
    count = 0
    current_date = datetime(1975, 12, 12)
    existing_token = collection.find({}, {"historical": True}).skip(15000).limit(2000)
    # existing_token = collection.find({"_id": ObjectId('6335dfe50702837123958f9f')}, {"historical": True})
    print('moving to loop')
    for token_document in existing_token:
        new_historical = []
        document_id = token_document['_id']
        historical = token_document.get('historical')
        
        for ts in historical:
            ts_day = ts['timestamp'].date()
            if current_date == ts_day and ts['timestamp'] > from_date and ts['timestamp'] < to_date:
                
                continue
            else:
                new_historical.append(ts)
            current_date = ts_day

        requests.append(UpdateOne({"_id": token_document['_id']}, {'$set': {'historical': new_historical}}))
        # collection.find_one_and_update({"_id": token_document['_id']}, {'$set': {'historical': new_historical}})
        
    
    try:
        collection.bulk_write(requests, ordered=False)
    except BulkWriteError as bwe:
        print(bwe.details)
            
historical_duplicate_remover(from_date=datetime(2022,10,3))