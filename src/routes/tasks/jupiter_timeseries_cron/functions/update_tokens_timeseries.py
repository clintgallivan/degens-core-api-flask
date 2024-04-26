from pymongo import MongoClient, UpdateOne
import os

# Setting up the MongoDB connection
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=True)  # Utilizing connection pooling
db = cluster['prod']
timeseries_collection = db['tokens-timeseries']

# Create an index on 'mint_address' to optimize queries and updates
index_creation_result = timeseries_collection.create_index([('mint_address', 1)], unique=False)

def update_tokens_timeseries(jupiter_data):
    operations = []
    for data in jupiter_data:
        mint_address = data['mint_address']
        price = data['price']
        created_at = data['created_at']

        operation = UpdateOne(
            {'mint_address': mint_address},
            {
                '$setOnInsert': {
                    'created_at': created_at,
                },
                '$set': {'updated_at': created_at},
                '$push': {
                    'historical': {
                        '$each': [{'price': price, 'created_at': created_at}],
                        '$position': 0  # Insert at the start of the array
                    }
                }
            },
            upsert=True
        )
        operations.append(operation)

        # Consider batching logic; for example, execute operations every 500 documents
        if len(operations) == 500:
            timeseries_collection.bulk_write(operations, ordered=False)
            operations = []

    # Execute any remaining operations in the batch
    if operations:
        timeseries_collection.bulk_write(operations, ordered=False)

# Example usage with data coming from somewhere (e.g., an API or another function)
# update_tokens_timeseries(jupiter_data)
