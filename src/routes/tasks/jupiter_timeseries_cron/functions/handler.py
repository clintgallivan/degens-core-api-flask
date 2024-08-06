import time
import json
import os
from .get_jupiter_data import get_jupiter_data
from .update_tokens_timeseries import update_tokens_timeseries
from datetime import datetime

LOG_TAG = ['jupiter_timeseries_cron.handler']

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# * [FOR LOCAL DEBUG] 1. Set use_local_data to True to use local data file in root of repo called "example_jupiter_data.json"
def handler(use_local_data=False, local_data_file='example_jupiter_data.json'):
    start_time = time.time()
    
    if use_local_data and os.path.exists(local_data_file):
        with open(local_data_file, 'r') as f:
            jupiter_data = json.load(f)
        
        # Convert created_at fields back to datetime objects
        for item in jupiter_data:
            if 'created_at' in item:
                item['created_at'] = datetime.fromisoformat(item['created_at'])
        
        print(f"{LOG_TAG} Loaded jupiter data from {local_data_file}")
    else:
        jupiter_data = get_jupiter_data()
        print(f"{LOG_TAG} Fetching jupiter data took: {time.time() - start_time:.2f} seconds")
    
    update_tokens_timeseries(jupiter_data, start_time)
    
    print(f"{LOG_TAG} Handler execution time: {time.time() - start_time:.2f} seconds")
    
    return

def save_jupiter_data_to_file(data, filename='example_jupiter_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, cls=DateTimeEncoder)
    print(f"Data saved to {filename}")