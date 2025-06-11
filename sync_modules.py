import requests
from zoho_auth import get_access_token
from db_handler import create_table, insert_records

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
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()['fields']

def fetch_module_data(token, module_name, from_time=None):
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    url = f'https://www.zohoapis.com/crm/v2.1/{module_name}?per_page=200'

    criteria = []
    if from_time:
        criteria.append(f"(Modified_Time:after:{from_time})")

    if criteria:
        url += '&criteria=' + '%20and%20'.join(criteria)

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get('data', [])