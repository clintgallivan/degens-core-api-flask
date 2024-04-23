from .get_token_list import get_token_list
from .get_jupiter_data import get_jupiter_data
from .update_tokens_timeseries import update_tokens_timeseries
from .get_tokens_timeseries_list import get_tokens_timeseries_list
from .remove_unused_documents import remove_unused_documents

def handler():
    mongo_token_address_list = get_token_list()
    mongo_tokens_timeseries_address_list = get_tokens_timeseries_list()
    jupiter_data = get_jupiter_data(mongo_token_address_list)
    update_tokens_timeseries(jupiter_data)
    remove_unused_documents(mongo_token_address_list, mongo_tokens_timeseries_address_list)
    return