import os
import time
import requests
from datetime import datetime, timezone
import concurrent.futures

jupiter_price_base_url = os.getenv('JUPITER_PRICE_BASE_URL')
jupiter_tokens_base_url = os.getenv('JUPITER_TOKENS_BASE_URL')

def fetch_prices(chunk):
    ids = ','.join(chunk)
    response = requests.get(f'{jupiter_price_base_url}/v6/price?ids={ids}')
    if response.status_code == 200:
        data = response.json().get('data', {})
        result = []
        for key, value in data.items():
            unix_timestamp = int(datetime.now(timezone.utc).timestamp())
            if value:
                result.append({
                    'mint_address': value['id'],
                    'price': value.get('price', 0),
                    'created_at': datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
                })
        return result
    else:
        return []

def get_jupiter_data():
    # Fetch token addresses from jupiter tokens api
    response = requests.get(f'{jupiter_tokens_base_url}/all')

    if response.status_code == 200:
        data = response.json()
        token_addresses = {token['address'] for token in data if 'address' in token}
    else:
        return []

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    address_chunks = list(chunks(list(token_addresses), 100))
    all_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        futures = []
        for chunk in address_chunks:
            futures.append(executor.submit(fetch_prices, chunk))
            time.sleep(0.1)  # Add a delay to avoid rate limiting
        for future in concurrent.futures.as_completed(futures):
            all_data.extend(future.result())

    return all_data