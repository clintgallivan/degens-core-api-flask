import time
from .get_jupiter_data import get_jupiter_data
from .update_tokens_timeseries import update_tokens_timeseries

LOG_TAG = ['jupiter_timeseries_cron.handler']

def handler():
    start_time = time.time()
    
    jupiter_data = get_jupiter_data()
    print(f"{LOG_TAG} Fetching jupiter data took: {time.time() - start_time:.2f} seconds")
    update_tokens_timeseries(jupiter_data)
    
    print(f"{LOG_TAG} Handler execution time: {time.time() - start_time:.2f} seconds")
    
    return