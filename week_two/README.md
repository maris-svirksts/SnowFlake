# Snowflake Database Setup and Teardown Scripts

This repository contains two SQL files to set up and tear down a simple database structure in Snowflake. The `create.sql` file handles the creation of a virtual warehouse, database, schema, and tables, while the `destroy.sql` file is used to clean up the resources created.

## Table of Contents
- [Overview](#overview)
- [Create Script](#create-script)
- [Destroy Script](#destroy-script)

## Overview
These scripts are designed to simplify the creation and management of resources in Snowflake. The `create.sql` script provisions a virtual warehouse, a database (`finance_db`), a schema (`transactions`), and several tables that represent financial transactions. The `destroy.sql` script safely deletes these resources when they are no longer needed.

## Create Script

### File: [create.sql](./create.sql)

The `create.sql` script performs the following actions:
1. **Create a virtual warehouse**: A virtual warehouse named `transaction_warehouse` of size `XSMALL` is created to handle the compute layer.
2. **Create a database**: The database `finance_db` is created to store the transaction data.
3. **Create a schema**: The `transactions` schema is created within the `finance_db`.
4. **Create a permanent table**: The table `financial_transactions` is created to store detailed transaction data. A data retention period of 60 days is also set.
5. **Create a transient table**: A transient table `staging_transactions` is created for intermediate data staging.
6. **Create a temporary table**: A temporary table `temp_aggregated_data` is created for short-term data calculations.
7. **Insert sample data**: Initial transaction data is inserted into the `financial_transactions` table for testing purposes.
8. **Time travel queries**: The script includes queries to fetch historical data using Snowflake's Time Travel feature.

### Key SQL Statements:
- **Virtual Warehouse**: `CREATE OR REPLACE WAREHOUSE transaction_warehouse`
- **Permanent Table**: `CREATE OR REPLACE TABLE finance_db.transactions.financial_transactions`
- **Transient Table**: `CREATE OR REPLACE TRANSIENT TABLE finance_db.transactions.staging_transactions`
- **Time Travel Query**: `SELECT * FROM finance_db.transactions.financial_transactions AT (OFFSET => -120)`

## Destroy Script

### File: [destroy.sql](./destroy.sql)

The `destroy.sql` script removes the following resources:
1. **Drop the temporary table**: The `temp_aggregated_data` table is dropped.
2. **Drop the transient table**: The `staging_transactions` table is dropped.
3. **Drop the permanent table**: The `financial_transactions` table is dropped.
4. **Drop the schema**: The `transactions` schema is removed from the `finance_db`.
5. **Drop the database**: The `finance_db` is dropped.
6. **Drop the virtual warehouse**: The `transaction_warehouse` is deleted.

### Key SQL Statements:
- **Drop Table**: `DROP TABLE IF EXISTS finance_db.transactions.financial_transactions`
- **Drop Schema**: `DROP SCHEMA IF EXISTS finance_db.transactions CASCADE`
- **Drop Database**: `DROP DATABASE IF EXISTS finance_db`
- **Drop Warehouse**: `DROP WAREHOUSE IF EXISTS transaction_warehouse`
