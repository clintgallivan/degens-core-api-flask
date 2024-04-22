from .get_jupiter_data import get_jupiter_data
from .update_tokens import update_tokens
from .get_tokens_list import get_tokens_list
from .remove_old_tokens import remove_old_tokens

def handler():
    [jupiter_data, jupiter_tokens_list] = get_jupiter_data()
    mongo_tokens_list = get_tokens_list()
    remove_old_tokens(mongo_tokens_list, jupiter_tokens_list)
    update_tokens(jupiter_data)
    return 'Jupiter Tokens handler successful'