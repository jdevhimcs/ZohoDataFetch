# US zoho module
ZOHO_CLIENT_ID = ''
ZOHO_CLIENT_SECRET = ''
ZOHO_REFRESH_TOKEN = ''
#ZOHO_REDIRECT_URI = 'your_redirect_uri'
ZOHO_URI = 'https://www.zohoapis.in/crm/v2.1/'

# Define the connection details
DB_SERVER = ''  # or '127.0.0.1' or 'localhost\SQLEXPRESS'
DB_NAME = ''  # Database name
DB_USER = 'localuser'  # SQL Server login username (e.g., 'sa' for system administrator)
DB_PASSWORD = 'Pass@1234'  # SQL Server login password

DB_SCHEMA = 'ZohoUS'
ZOHO_MODULE = 'Leads'
MIN_PAGE_LIMIT = 1
MAX_PAGE_LIMIT = 3



SQL_CONNECTION_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}'