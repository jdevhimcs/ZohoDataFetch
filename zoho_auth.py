import requests
import json
import os
from datetime import datetime, timedelta
from config import ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN

TOKEN_FILE = 'zoho_token.json'

def get_stored_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            expiry = datetime.strptime(data['expiry'], '%Y-%m-%dT%H:%M:%S')
            if datetime.now() < expiry:
                return data['access_token']
    return None

def save_token(token):
    expiry_time = datetime.now() + timedelta(hours=1)
    data = {
        'access_token': token,
        'expiry': expiry_time.strftime('%Y-%m-%dT%H:%M:%S')
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f)

def refresh_access_token():
    url = 'https://accounts.zoho.in/oauth/v2/token'
    params = {
        'refresh_token': ZOHO_REFRESH_TOKEN,
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_CLIENT_SECRET,
        'grant_type': 'refresh_token'
    }
    res = requests.post(url, params=params)
    res.raise_for_status()
    token = res.json()['access_token']
    save_token(token)
    return token

def get_access_token():
    token = get_stored_token()
    if token:
        return token
    return refresh_access_token()