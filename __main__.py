from config import ZOHO_MODULE, DB_SCHEMA
from global_data_save import fetch_fresh_data  # or fetch_incremental_data
from auth import get_access_token
from sync_modules import get_modules, get_module_fields
from db_handler import create_table

# Get data from module wise with page limit from min to max
def module_data(module_name):
    print(f"Process module name {module_name}")
    fetch_fresh_data(module_name)

def create_table_for_all_module():
    token = get_access_token()

    # Create tables for all module
    modules = get_modules(token)
    for module in modules:
        if(module == 'Activities' or module == 'Approvals'):
            continue
        if(module == 'Leads'):
            print(f"Processing {module}...")

            fields = get_module_fields(token, module)
            create_table(module, fields, DB_SCHEMA)

def main():
    create_table_for_all_module()
    module_data(ZOHO_MODULE)

if __name__ == "__main__":
    main()

