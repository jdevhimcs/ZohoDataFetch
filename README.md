# Zoho Sales Sync Project

This project syncs **Sales Orders** and their **line items** from the Zoho CRM API to a Microsoft SQL Server database. It supports both fresh daily imports and incremental updates.

---

## 📁 Project Structure

```
zoho_sales_sync/
├── __main__.py                  # Main entry point to run data sync
├── config.py                    # Contains API and DB credentials
├── db_utils.py                  # DB connection & sync time functions
├── auth.py                      # Zoho access token management
├── zoho_api.py                  # Handles Zoho API communication
├── sales_orders.py              # Sync logic for Sales Orders
├── sales_order_items.py         # Sync logic for related line items
├── utils.py                     # Helper utilities (e.g., date formatting)
└── requirements.txt             # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Update `config.py` with your:

- Zoho API credentials
- SQL Server connection details

### 3. Run the Sync

```bash
python -m zoho_sales_sync
```

By default, it runs the **daily sync** of newly created Sales Orders.

To run **incremental sync** (e.g., modified in last 1 hour), change the `main()` function in `__main__.py` to call:

```python
from sales_orders import fetch_incremental_data
fetch_incremental_data(ZOHO_MODULE)
```

---

## 🛠 Features

- Auto-refresh Zoho access token
- Pull paginated data from Zoho CRM
- Insert/Update records in MS SQL Server
- Flatten nested JSON from Zoho API
- Line item sync via separate endpoint

---

## 🔐 Note

Ensure your SQL Server schema has the necessary tables:

- `ZohoIntl.Sales_Orders`
- `ZohoIntl.Sales_Ordered_Items`
- `ZohoIntl.LastSync`
- `ZohoIntl.ZohoAuth`
- `ZohoIntl.InsertErrorLog`

---

## 📄 License

Internal project for EC-Council integration. No external distribution permitted.