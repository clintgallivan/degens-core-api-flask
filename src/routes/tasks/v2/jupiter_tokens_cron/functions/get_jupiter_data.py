import os
import requests
from datetime import datetime, timezone
import json

jupiter_price_base_url = os.getenv('JUPITER_TOKENS_BASE_URL')

def get_jupiter_data():
    # r = requests.get(f'{jupiter_price_base_url}/strict')
    r = requests.get(f'{jupiter_price_base_url}/all')
    all_data = r.json()

    jupiter_tokens_list = []
    def get_jupiter_tokens_list(data):
        for token in data:
            jupiter_tokens_list.append(token['address'])
    get_jupiter_tokens_list(all_data)
    
    return [all_data, jupiter_tokens_list]

# Example usage
# [{'address': '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr', 'chainId': 101, 'decimals': 9, 'name': 'Popcat', 'symbol': 'POPCAT', 'logoURI': 'https://bafkreidvkvuzyslw5jh5z242lgzwzhbi2kxxnpkic5wsvyno5ikvpr7reu.ipfs.nftstorage.link', 'tags': ['community'], 'extensions': {'coingeckoId': 'popcat'}}]
# [jupiter_data, jupiter_tokens_list] = get_jupiter_data()
