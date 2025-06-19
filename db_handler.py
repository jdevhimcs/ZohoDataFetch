import pyodbc
from datetime import datetime
from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

# =====================
# Database Connection
# =====================
def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={DB_SERVER};'
        f'DATABASE={DB_NAME};'
        f'UID={DB_USER};'
        f'PWD={DB_PASSWORD}'
    )

# =====================
# SQL Field Validator
# =====================
def is_valid_sql_field(field_name):
    return (
        field_name 
        and isinstance(field_name, str) 
        and not field_name.startswith('$') 
        and field_name.lower() != 'id'
    )

# =====================
# Create Table Dynamically
# =====================
def create_table(table_name, columns, schema_name='ZohoUS'):
    conn = get_db_connection()
    cursor = conn.cursor()

    col_defs = []

    for col in columns:
        api_name = col['api_name']
        if is_valid_sql_field(api_name):
            datatype = map_zoho_to_sql_datatype(col.get('data_type', 'text'))
            col_defs.append(f"[{api_name}] {datatype}")

    # Always add zoho_id for traceability
    col_defs.append("[zoho_id] NVARCHAR(255) UNIQUE NOT NULL")

    # Compose the full table name with schema
    full_table_name = f"[{schema_name}].[{table_name}]"
    col_defs_str = ', '.join(col_defs)

    sql = f"""
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'
    )
    BEGIN
        CREATE TABLE {full_table_name} ({col_defs_str})
    END
    """

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# =====================
# Parse Dates (fallback)
# =====================
def parse_date(value):
    if not value or value in ['None', '']:
        return None
    for fmt in ("%b %d, %Y %I:%M %p", "%b %d, %Y", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return value  # Return original if not parsable

# =====================
# Insert Records (Default Type NVARCHAR)
# =====================
def insert_records(table_name, records):
    if not records:
        return

    # Define known nested fields
    nested_fields = {
        "Owner": ["Name", "Email", "Id"],
        "Modified_By": ["Name", "Email", "Id"],
        "Layout": ["display_label", "name", "id"]
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch actual column names from DB
    cursor.execute(f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}'
    """)
    column_names = {row[0] for row in cursor.fetchall()}

    for record in records:
        cleaned_record = {}

        for k, v in record.items():
            if k.startswith('$'):
                continue

            for main_field, sub_fields in nested_fields.items():
                if main_field in record and isinstance(record[main_field], dict):
                    for sub_key in sub_fields:
                        combined_key = f"{main_field}_{sub_key}"
                        value = record[main_field].get(sub_key)
                        cleaned_record[combined_key] = str(value).strip() if value is not None else None
                        
            # Flatten dict (e.g. Layout)            
            if isinstance(v, dict):
                print(v)
                for sub_k, sub_v in v.items():
                    new_key = f"{k}_{sub_k}"
                    print(new_key);
                    if new_key in column_names:
                        cleaned_record[new_key] = str(sub_v).strip() if sub_v is not None else None
                continue

            if k not in column_names:
                continue

            # Convert list to string
            if isinstance(v, list):
                v = str(v)

            # Clean strings
            elif isinstance(v, str):
                v = v.strip()
                if v.lower() in ['none', 'null', '']:
                    v = None

            # Final clean
            cleaned_record[k] = str(v).strip() if v is not None else None

        if not cleaned_record:
            continue

        keys = ', '.join(f"[{k}]" for k in cleaned_record)
        values = ', '.join(['?' for _ in cleaned_record])
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
        #print(sql);

        try:
            cursor.execute(sql, list(cleaned_record.values()))
        except Exception as e:
            print("❌ Error inserting record:")
            print("Original record:", record)
            print("Prepared record:", cleaned_record)
            print("Error message:", e)

    conn.commit()
    cursor.close()
    conn.close()

# =====================
# Optional: Zoho-to-SQL Type Mapping (used only in create_table)
# =====================
def map_zoho_to_sql_datatype(zoho_type):
    mapping = {
        "text": "NVARCHAR(MAX)",
        "textarea": "NVARCHAR(MAX)",
        "email": "NVARCHAR(255)",
        "phone": "NVARCHAR(50)",
        "integer": "INT",
        "bigint": "NVARCHAR(MAX)",
        "boolean": "NVARCHAR(10)",
        "double": "FLOAT",
        "currency": "FLOAT",
        "percent": "FLOAT",
        "datetime": "DATETIME",
        "date": "DATE",
        "lookup": "NVARCHAR(MAX)",
        "ownerlookup": "NVARCHAR(MAX)",
        "picklist": "NVARCHAR(255)",
        "multiselectpicklist": "NVARCHAR(MAX)",
        "jsonobject": "NVARCHAR(MAX)",
        "profilelookup": "NVARCHAR(MAX)",
        "userlookup": "NVARCHAR(MAX)",
        "autonumber": "NVARCHAR(100)",
        "website": "NVARCHAR(255)",
        "richtext": "NVARCHAR(MAX)"
    }

    return mapping.get(zoho_type.lower(), "NVARCHAR(MAX)")

