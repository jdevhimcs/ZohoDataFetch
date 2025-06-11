import pyodbc
from config import SQL_CONNECTION_STRING

def get_db_connection():
    return pyodbc.connect(SQL_CONNECTION_STRING)

def create_table(table_name, columns):
    conn = get_db_connection()
    cursor = conn.cursor()

    col_defs = []
    for col in columns:
        name = col['api_name']
        datatype = 'NVARCHAR(MAX)'
        col_defs.append(f"[{name}] {datatype}")

    col_defs_str = ', '.join(col_defs)
    sql = f"IF OBJECT_ID('{table_name}', 'U') IS NULL CREATE TABLE {table_name} ({col_defs_str})"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def insert_records(table_name, records):
    if not records:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for record in records:
        keys = ', '.join(f"[{k}]" for k in record)
        values = ', '.join(['?' for _ in record])
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
        cursor.execute(sql, list(record.values()))

    conn.commit()
    cursor.close()
    conn.close()