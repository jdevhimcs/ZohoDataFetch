import requests
from auth import get_access_token
from db_handler import create_table, insert_records
import time

def get_modules(token):
    print(token)
    url = 'https://www.zohoapis.com/crm/v2.1/settings/modules'
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    #print("Status Code:", res.status_code)
    #print("Response:", res.text)    

    return [m['api_name'] for m in res.json()['modules'] if m['api_supported']]

def get_module_fields(token, module_name):
    url = f"https://www.zohoapis.com/crm/v2.1/settings/fields?module={module_name}"
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('fields', [])
    elif response.status_code == 401:
        time.sleep(2)
    else:
        time.sleep(2)
    return []
        