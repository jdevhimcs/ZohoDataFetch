import pyodbc
from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={DB_SERVER};'
        f'DATABASE={DB_NAME};'
        f'UID={DB_USER};'
        f'PWD={DB_PASSWORD}'
    )

def is_valid_sql_field(field_name):
    return not field_name.startswith('$') and field_name.lower() != 'id'

# Dynamic Table Creation method
def create_table(table_name, columns):
    conn = get_db_connection()
    cursor = conn.cursor()

    col_defs = []
    for col in columns:
        api_name = col['api_name']
        if is_valid_sql_field(api_name):
            datatype = 'NVARCHAR(MAX)'
            col_defs.append(f"[{api_name}] {datatype}")

    col_defs_str = ', '.join(col_defs)
    sql = f"IF OBJECT_ID('{table_name}', 'U') IS NULL CREATE TABLE {table_name} ({col_defs_str})"

    print(f"Creating table with SQL:\n{sql}")  # Optional debug log
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# Inset records into the Table as per Module
def insert_records(table_name, records):
    if not records:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for record in records:
        # Filter out invalid fields
        filtered_record = {
            k: v for k, v in record.items() if is_valid_sql_field(k)
        }

        if not filtered_record:
            print(f"Skipping empty or invalid record: {record}")
            continue

        keys = ', '.join(f"[{k}]" for k in filtered_record)
        values = ', '.join(['?' for _ in filtered_record])
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"

        try:
            cursor.execute(sql, list(filtered_record.values()))
        except Exception as e:
            print(f"Error inserting record: {record}\nError: {e}")

    conn.commit()
    cursor.close()
    conn.close()

