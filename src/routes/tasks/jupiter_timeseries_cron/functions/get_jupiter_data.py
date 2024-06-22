from datetime import datetime, timezone
import json
import os
import requests

jupiter_price_base_url = os.getenv('JUPITER_PRICE_BASE_URL')
jupiter_tokens_base_url = os.getenv('JUPITER_TOKENS_BASE_URL')

def get_jupiter_data():
    # Fetch token addresses from jupiter tokens api
    response = requests.get(f'{jupiter_tokens_base_url}/all')

    if response.status_code == 200:
        data = response.json()
        # Use a set to store addresses to automatically handle duplicates
        token_addresses = {token['address'] for token in data if 'address' in token}
    else:
        print(f"Error with API call: {response.status_code}")
        return []

    # Function to divide token addresses into chunks of 100
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Convert the set back to a list and split the addresses into chunks of 100
    address_chunks = list(chunks(list(token_addresses), 100))
    
    # Accumulator for the results from all API calls
    all_data = []
    
    # Loop through each chunk, make API calls and collect data
    for chunk in address_chunks:
        # Join addresses in the chunk with commas
        ids = ','.join(chunk)
        
        # Make the API call
        response = requests.get(f'{jupiter_price_base_url}/v6/price?ids={ids}')
        
        # Check if the response was successful
        if response.status_code == 200:
            # Extract data from the response
            data = response.json().get('data', {})
            # Parse each token data
            for key, value in data.items():
                unix_timestamp = int(datetime.now(timezone.utc).timestamp())
                if value:  # Check if the value is not empty
                    all_data.append({
                        'mint_address': value['id'],
                        'price': value.get('price', 0),  # Use .get() to handle missing 'price'
                        'created_at': datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
                    })
        else:
            print(f"Error with API call: {response.status_code}")
    return all_data

# Example usage
# token_addresses = ['So11111111111111111111111111111111111111112', 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', ...]
# data = get_jupiter_data(token_addresses)
