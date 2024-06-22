from .get_jupiter_data import get_jupiter_data
from .update_tokens_timeseries import update_tokens_timeseries

def handler():
    jupiter_data = get_jupiter_data()
    update_tokens_timeseries(jupiter_data)
    return