-- Set the role
USE ROLE SYSADMIN;

-- Create a virtual warehouse with x-small size to handle the compute layer
CREATE OR REPLACE WAREHOUSE transaction_warehouse
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;

-- Create a database named finance_db
CREATE OR REPLACE DATABASE finance_db;

-- Create a schema named transactions within the finance_db
CREATE OR REPLACE SCHEMA finance_db.transactions;

-- Create a permanent table named financial_transactions
CREATE OR REPLACE TABLE finance_db.transactions.financial_transactions (
  transaction_id STRING,
  account_id STRING,
  amount NUMBER,
  transaction_date DATE,
  transaction_type STRING
);

-- Modify the data retention period to 60 days
ALTER TABLE finance_db.transactions.financial_transactions SET DATA_RETENTION_TIME_IN_DAYS = 60;

-- Verify the data retention period
SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' IN TABLE finance_db.transactions.financial_transactions;

-- Create a transient table named staging_transactions
CREATE OR REPLACE TRANSIENT TABLE finance_db.transactions.staging_transactions (
  transaction_id STRING,
  account_id STRING,
  amount NUMBER,
  transaction_date DATE,
  transaction_type STRING
);

-- Check metadata to confirm the table is transient
SHOW TABLES LIKE 'staging_transactions' IN SCHEMA finance_db.transactions;

-- Create a temporary table named temp_aggregated_data for short-term calculations
CREATE OR REPLACE TEMPORARY TABLE finance_db.transactions.temp_aggregated_data (
  account_id STRING,
  total_amount NUMBER,
  average_amount NUMBER
);

-- Retrieve and display all different types of tables
SHOW TABLES IN SCHEMA finance_db.transactions;

-- Insert initial transaction data into the financial_transactions table
INSERT INTO finance_db.transactions.financial_transactions (transaction_id, account_id, amount, transaction_date, transaction_type) VALUES
('TXN1001', 'ACCT123', 150.00, '2024-09-10', 'credit'),
('TXN1002', 'ACCT124', -75.00, '2024-09-10', 'debit'),
('TXN1003', 'ACCT125', 200.00, '2024-09-10', 'credit'),
('TXN1004', 'ACCT126', -100.00, '2024-09-10', 'debit'),
('TXN1005', 'ACCT127', 120.00, '2024-09-10', 'credit'),
('TXN1006', 'ACCT128', -105.00, '2024-09-10', 'debit'),
('TXN1007', 'ACCT129', 200.00, '2024-09-10', 'credit'),
('TXN1008', 'ACCT130', -180.00, '2024-09-10', 'debit');

-- Simulate additional transactions (after waiting for 2+ minutes)
INSERT INTO finance_db.transactions.financial_transactions (transaction_id, account_id, amount, transaction_date, transaction_type) VALUES
('TXN1009', 'ACCT131', 300.00, '2024-09-10', 'credit'),
('TXN1010', 'ACCT132', -50.00, '2024-09-10', 'debit');

-- Query data as it exists now
SELECT * FROM finance_db.transactions.financial_transactions;

-- Query data as it existed 2 minutes ago
SELECT * FROM finance_db.transactions.financial_transactions 
  AT (OFFSET => -120);

-- Query data as it existed 10 minutes ago
SELECT * FROM finance_db.transactions.financial_transactions 
  AT (OFFSET => -600);
