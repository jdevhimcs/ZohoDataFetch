import requests
from datetime import datetime, timedelta
from db_utils import get_sql_server_connection
from config import ZOHO_REFRESH_TOKEN, ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, DB_SCHEMA

def get_access_token():
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT TOP 1 access_token, refresh_token, expires_in, created_at FROM {DB_SCHEMA}.ZohoAuth ORDER BY id DESC;")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        access_token, refresh_token, expires_in, created_at = result
        if datetime.now() < created_at + timedelta(seconds=expires_in):
            return access_token
        return refresh_access_token(refresh_token)
    return refresh_access_token(ZOHO_REFRESH_TOKEN)

def refresh_access_token(refresh_token):
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": refresh_token,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        token_data = response.json()
        save_access_token(token_data['access_token'], refresh_token, token_data['expires_in'])
        return token_data['access_token']
    return None

def save_access_token(access_token, refresh_token, expires_in):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {DB_SCHEMA}.ZohoAuth (access_token, refresh_token, expires_in, created_at) VALUES (?, ?, ?, ?)",
                   (access_token, refresh_token, expires_in, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()