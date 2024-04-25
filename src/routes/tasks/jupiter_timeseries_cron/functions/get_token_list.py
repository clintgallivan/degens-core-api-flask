import os
from pymongo import MongoClient

# Set up MongoDB connection
cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster['prod']
collection = db['tokens']

def get_token_list(per_page=10000):
    all_tokens = []
    page = 1
    while True:
        # Fetch a page of tokens
        tokens = collection.find().skip((page - 1) * per_page).limit(per_page)
        current_batch = [token['mint_address'] for token in tokens]
        if not current_batch:
            break  # If no tokens are found, stop the loop
        all_tokens.extend(current_batch)
        page += 1
    print(f"Total tokens retrieved: {len(all_tokens)}")
    return all_tokens
