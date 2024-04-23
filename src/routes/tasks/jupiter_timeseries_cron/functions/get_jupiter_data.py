import os
import requests
from datetime import datetime, timezone
import json

jupiter_price_base_url = os.getenv('JUPITER_PRICE_BASE_URL')

def get_jupiter_data(token_addresses):
    # Function to divide token addresses into chunks of 100
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Splitting the addresses into chunks of 100
    address_chunks = list(chunks(token_addresses, 100))
    
    # Accumulator for the results from all API calls
    all_data = []
    
    # Loop through each chunk, make API calls and collect data
    for chunk in address_chunks:
        # Join addresses in the chunk with commas
        ids = ','.join(chunk)
        
        # Make the API call
        response = requests.get(f'{jupiter_price_base_url}/v4/price?ids={ids}')
        
        # Check if the response was successful
        if response.status_code == 200:
            # Extract data from the response
            data = response.json().get('data', {})
            # Parse each token data
            for key, value in data.items():
                all_data.append({
                    'mint_address': value['id'],
                    'price': value['price'],
                    'created_at':  int(datetime.now(timezone.utc).timestamp())
                })
        else:
            print(f"Error with API call: {response.status_code}")
    return all_data

# Example usage
# token_addresses = ['So11111111111111111111111111111111111111112', 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', ...]
# data = get_jupiter_data(token_addresses)
