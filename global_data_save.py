from zoho_api import fetch_data_from_zoho
from db_utils import get_sql_server_connection, setLastSyncTime
from config import ZOHO_REFRESH_TOKEN, ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, MIN_PAGE_LIMIT, MAX_PAGE_LIMIT, DB_SCHEMA
import pyodbc

def store_data_into_sql(module, data):
    insert_data = []
    for record in data:
        flat = {k: str(v) for k, v in record.items()}
        # Ensure Zoho ID is present
        if 'id' in record:
            flat['zoho_id'] = record['id']

        insert_data.append(flat)

    insert_records(module, insert_data)

def fetch_fresh_data(module):
    page = MIN_PAGE_LIMIT
    while True:
        from datetime import datetime, timedelta
        last_sync_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S%z')
        print(f"Module {module} -> fetching data for page no {page}")
        data = fetch_data_from_zoho(module, "Created_Time", last_sync_time, page)
        if not data or page == MAX_PAGE_LIMIT:
            print(f"Module {module} → Page {page}: This Message was reached either because the maximum page limit set by the configuration file was exceeded or no records were found on this page.")
            break
        
        store_data_into_sql(module, data)
        page += 1
    setLastSyncTime(module, "daily")

# =====================
# Insert Records (Default Type NVARCHAR)
# =====================
from datetime import datetime

def insert_records(table_name, records):
    if not records:
        return

    conn = get_sql_server_connection()
    cursor = conn.cursor()

    # Fetch actual column names and their types from DB
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}'
    """)
    columns_info = {row[0]: row[1] for row in cursor.fetchall()}

    # Define datetime fields
    datetime_fields = {'Created_Time', 'Modified_Time', 'Call_Start_Time', 'Last_Activity_Time', 'Lead_Status_updated_time', 'Assign_owner_Date_time', 'Last_Visited_Time', 'eventbrite__Order_Date',
                       'First_Activity_Time', 'Lead_Creation_Date', 'Estimated_Training_Dates', 'Membership_Expiration_Date', 'Membership_Activated_Date', 'First_Visited_Time',
                       'Unsubscribed_Time', 'Change_Log_Time__s', 'Lead_Owner_assignement_time', 'Last_Enriched_Time__s'}
    
    bigint_fields = {column for column, dtype in columns_info.items() if dtype == 'bigint'}

    for record in records:
        print(f"🔍 Process data for Zoho ID: {record.get('id')}")
        cleaned_record = {}

        for k, v in record.items():
            
            if k.startswith('$'):
                continue

            # Flatten dict (e.g. Layout)
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    new_key = f"{k}_{sub_k}"
                    if new_key in columns_info:
                        cleaned_record[new_key] = str(sub_v).strip() if sub_v is not None else None
                continue

            if k not in columns_info:
                continue

            # Convert list to string
            if isinstance(v, list):
                v = str(v)

            # Clean strings
            elif isinstance(v, str):
                v = v.strip()
                if v.lower() in ['none', 'null', '']:
                    v = None

            # Handle datetime fields
            if k in datetime_fields and v:
                try:
                    # Attempt to convert the date to a datetime object
                    dt = datetime.fromisoformat(v)  # This works for 'YYYY-MM-DDTHH:MM:SS+HH:MM' or 'YYYY-MM-DD HH:MM:SS'
                    v = dt.strftime('%Y-%m-%d %H:%M:%S')  # Format for SQL Server
                except ValueError:
                    print(f"❌ Invalid datetime format for {k}: {v}")
                    v = None  # Fallback if conversion fails

            # Handle bigint fields (convert to integer)
            if k in bigint_fields and v is not None:
                try:
                    v = int(v)  # Convert to integer if possible
                except ValueError:
                    print(f"❌ Invalid value for bigint field '{k}': {v}. Setting it to NULL.")
                    v = None  # Set invalid values to None

            # Final clean
            cleaned_record[k] = str(v).strip() if v is not None else None

        if not cleaned_record:
            continue

        keys = ', '.join(f"[{k}]" for k in cleaned_record)
        values = ', '.join(['?' for _ in cleaned_record])
        sql = f"INSERT INTO {DB_SCHEMA}.{table_name} ({keys}) VALUES ({values})"

        try:
            cursor.execute(sql, list(cleaned_record.values()))
            print(f"✅ Data inserted successfully!")
        except pyodbc.IntegrityError as e:                
            print(f"❌ Skipping duplicate record:")   
        except Exception as e:
            print("❌ Error inserting record:")
            print("Original record:", record)
            print("Prepared record:", cleaned_record)
            print("Error message:", e)

    conn.commit()
    cursor.close()
    conn.close()
