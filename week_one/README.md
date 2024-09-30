# Snowflake Solution - Combine Two Tables

## Overview

This project demonstrates how to combine data from two tables (`Person` and `Address`) using Snowflake. The solution involves creating a dedicated database and schema, setting up the necessary tables, and then performing a `LEFT JOIN` to merge the data, ensuring that all records from the `Person` table are included in the final output, even if they do not have corresponding entries in the `Address` table.

## Prerequisites

- A Snowflake account with access to the `SYSADMIN` role.
- Basic knowledge of SQL.

## Steps to Implement

### 1. Create a Dedicated Database and Schema

First, connect to the `SYSADMIN` role and create a new database and schema.

```sql
-- Connect to the SYSADMIN role
USE ROLE SYSADMIN;

-- Create a new database
CREATE DATABASE person_address_db;

-- Create a new schema within the database
CREATE SCHEMA person_address_schema;

-- Switch to the newly created database and schema
USE DATABASE person_address_db;
USE SCHEMA person_address_schema;
```

### 2. Create the Tables

Create the `Person` and `Address` tables with the specified columns.

```sql
-- Create the Person table
CREATE TABLE Person (
    personId INT PRIMARY KEY,
    lastName VARCHAR,
    firstName VARCHAR
);

-- Create the Address table
CREATE TABLE Address (
    addressId INT PRIMARY KEY,
    personId INT,
    city VARCHAR,
    state VARCHAR,
    FOREIGN KEY (personId) REFERENCES Person(personId)
);
```

### 3. Insert Sample Data

Populate the tables with sample data.

```sql
-- Insert data into the Person table
INSERT INTO Person (personId, lastName, firstName) VALUES
(1, 'Wang', 'Allen'),
(2, 'Alice', 'Bob');

-- Insert data into the Address table
INSERT INTO Address (addressId, personId, city, state) VALUES
(1, 2, 'New York City', 'New York'),
(2, 3, 'Leetcode', 'California');
```

### 4. Query to Combine the Tables

Perform a `LEFT JOIN` to combine the data from the `Person` and `Address` tables.

```sql
-- Query to combine the Person and Address tables
SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM
    Person p
LEFT JOIN
    Address a
ON
    p.personId = a.personId;
```

### 5. Expected Output

The result of the query should look like this:

```sql
+-----------+----------+---------------+----------+
| firstName | lastName | city          | state    |
+-----------+----------+---------------+----------+
| Allen     | Wang     | Null          | Null     |
| Bob       | Alice    | New York City | New York |
+-----------+----------+---------------+----------+
```

### Explanation

- **Database and Schema**: We created a new database and schema to keep the solution isolated and organized.
- **Tables**: The `Person` table holds basic person information, and the `Address` table holds city and state information linked to persons.
- **LEFT JOIN**: This join ensures that all persons are included in the result, even if they do not have an address.
