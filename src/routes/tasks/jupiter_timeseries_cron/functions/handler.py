from .get_token_list import get_token_list
from .get_jupiter_data import get_jupiter_data
from .update_tokens_timeseries import update_tokens_timeseries

def handler():
    token_addresses = get_token_list()
    jupiter_data = get_jupiter_data(token_addresses)
    update_tokens_timeseries(jupiter_data)
    return token_addresses