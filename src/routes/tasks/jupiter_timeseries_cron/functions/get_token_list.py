import os
from pymongo import MongoClient

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
collection = db['tokens']

def get_token_list(page=1, per_page=10000):
    output = []
    tokens = collection.find().skip((page - 1) * per_page).limit(per_page)
    for token in tokens:
        output.append(token['mint_address'])
    return output