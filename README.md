# 📊 ZohoDataFetch

A robust, extensible tool to **sync any Zoho CRM module** (e.g., Leads, Accounts, Sales Orders) into a **Microsoft SQL Server** database.

Supports automatic table creation, token refresh, incremental syncs, and error handling — fully configurable and database-driven.

---

## 🚀 Features

✅ **Zoho OAuth Token Management**

* Refresh token automatically handled
* Token info stored in DB (`ZohoAuth` table)
* Transparent retry on token expiry
  👉 [auth.py](https://github.com/jdevhimcs/ZohoDataFetch/blob/main/auth.py)

---

✅ **Dynamic Table Creation per Module**

* Fetches Zoho module metadata via API
* Automatically creates corresponding SQL Server table with proper data types
  👉 [db\_handler.py](https://github.com/jdevhimcs/ZohoDataFetch/blob/main/db_handler.py)

---

✅ **Incremental Sync Based on Last Sync Time**

* Syncs only new/updated records from last successful sync
* Maintains sync log in `LastSync` table
  👉 [db\_utils.py](https://github.com/jdevhimcs/ZohoDataFetch/blob/main/db_utils.py)

---

✅ **Modular and Reusable Structure**

* Add support for any Zoho CRM module
* Works across different tables/schemas
* Central config for credentials and database connection

---

✅ **Clean Error Logging**

* Logs failed insertions in a dedicated `InsertErrorLog` table
* Helps in debugging and reprocessing

---

## 📁 Project Structure

```
ZohoDataFetch/
├── __main__.py            # Main entry point
├── auth.py                # Token management
├── config.py              # Zoho + DB credentials
├── db_handler.py          # Table creation logic
├── db_utils.py            # Last sync tracking
├── global_data_save.py    # Common record insertion logic
├── sync_modules.py        # Sync logic by module
├── zoho_api.py            # API integration layer
├── basic_query.sql        # Sample queries
├── requirements.txt       # Dependencies
```

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/jdevhimcs/ZohoDataFetch.git
cd ZohoDataFetch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

Update `config.py` with:

* Zoho API credentials (client ID, secret, refresh token)
* SQL Server connection string

Ensure you have the following tables in your DB:

* `ZohoAuth` (for token)
* `LastSync` (for last sync timestamps)
* `InsertErrorLog` (for error records)

---

## 📦 How to Use

### ⏯️ Full Sync

Run the full sync from the main file:

```bash
python __main__.py
```

### 🔁 Add New Module

To sync a new module (e.g., Contacts, Invoices):

1. Add module name to the sync logic
2. The system:

   * Fetches module metadata
   * Creates SQL table
   * Pulls records since last sync
   * Inserts/updates DB

---

## 📌 Best Practices

* Use a scheduler (e.g., Windows Task Scheduler / cron) to automate daily/hourly sync
* Backup your DB regularly
* Monitor `InsertErrorLog` for failed records
* Avoid unnecessary full syncs on large modules

---

## 🧩 Example Modules You Can Sync

* Leads
* Accounts
* Contacts
* Sales Orders
* Invoices
* Deals

> Add any module with just one line — no schema hardcoding needed.

---

## 🛡️ Security Notes

* Do not commit real API keys or refresh tokens
* Use `.env` for secrets (can be added in a future enhancement)
* Ensure the database has proper access control

---

## 🧠 Contributions

Want to extend this for another CRM or DB?
PRs are welcome! Please follow the modular structure.

---

## 📬 Contact

Maintainer: [Gaurav Pandey](mailto:jdevhimcs@gmail.com)


