import requests
import time
from auth import get_access_token

def fetch_data_from_zoho(module, filter_type, filter_value, page=1, retry_count=3):
    for attempt in range(retry_count):
        url = f"https://www.zohoapis.com/crm/v2.1/{module}?page={page}&per_page=200"
        headers = {'Authorization': f'Zoho-oauthtoken {get_access_token()}', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', [])
        elif response.status_code == 401:
            time.sleep(2)
        else:
            time.sleep(2)
    return []