import pyodbc
from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA
from datetime import datetime, timedelta

def get_sql_server_connection():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}'
    )

def getLastSyncTime(module, sync_type):
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT last_sync_time FROM {DB_SCHEMA}.LastSync WHERE module = ? AND sync_type = ?", (module, sync_type))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')

def setLastSyncTime(module, sync_type):
    sync_time = datetime.now()
    conn = get_sql_server_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        MERGE INTO {DB_SCHEMA}.LastSync AS target
        USING (VALUES (?, ?, ?)) AS source (module, sync_type, last_sync_time)
        ON target.module = source.module AND target.sync_type = source.sync_type
        WHEN MATCHED THEN
            UPDATE SET last_sync_time = source.last_sync_time
        WHEN NOT MATCHED THEN
            INSERT (module, sync_type, last_sync_time) VALUES (source.module, source.sync_type, source.last_sync_time);
    """, (module, sync_type, sync_time))
    conn.commit()
    cursor.close()
    conn.close()