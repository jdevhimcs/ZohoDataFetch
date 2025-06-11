from zoho_auth import get_access_token
from sync_modules import get_modules, get_module_fields, fetch_module_data
from db_handler import create_table, insert_records
from utils import get_iso_time

def main():
    token = get_access_token()
    modules = get_modules(token)

    for module in modules:
        print(f"Processing {module}...")

        fields = get_module_fields(token, module)
        create_table(module, fields)

        from_time = get_iso_time(hours_ago=24)
        records = fetch_module_data(token, module, from_time)

        insert_data = []
        for record in records:
            flat = {k: str(v) for k, v in record.items()}
            insert_data.append(flat)

        insert_records(module, insert_data)

if __name__ == "__main__":
    main()