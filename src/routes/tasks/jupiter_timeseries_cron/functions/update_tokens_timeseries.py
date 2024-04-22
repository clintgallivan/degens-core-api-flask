from pymongo import MongoClient, UpdateOne
import os

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
timeseries_collection = db['tokens-timeseries']

def update_tokens_timeseries(jupiter_data):
    operations = []
    for data in jupiter_data:
        mint_address = data['mint_address']
        price = data['price']
        created_at = data['created_at']

        operation = UpdateOne(
            {'mint_address': mint_address}, 
            {
                '$set': {'updated_at': created_at},
                '$setOnInsert': {'created_at': created_at},
                '$push': {'historical': {
                    '$each': [{'price': price, 'created_at': created_at}],
                    '$position': 0
                }},
            }, 
            upsert=True
        )
        operations.append(operation)

        # If the number of operations reaches 1000, perform the batch update and clear the list of operations
        if len(operations) == 1000:
            timeseries_collection.bulk_write(operations)
            operations = []

    # Perform the batch update for any remaining operations
    if operations:
        timeseries_collection.bulk_write(operations)