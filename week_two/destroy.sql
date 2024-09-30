-- Drop the temporary table temp_aggregated_data
DROP TABLE IF EXISTS finance_db.transactions.temp_aggregated_data;

-- Drop the transient table staging_transactions
DROP TABLE IF EXISTS finance_db.transactions.staging_transactions;

-- Drop the permanent table financial_transactions
DROP TABLE IF EXISTS finance_db.transactions.financial_transactions;

-- Drop the schema transactions
DROP SCHEMA IF EXISTS finance_db.transactions CASCADE;

-- Drop the database finance_db
DROP DATABASE IF EXISTS finance_db;

-- Drop the virtual warehouse transaction_warehouse
DROP WAREHOUSE IF EXISTS transaction_warehouse;
