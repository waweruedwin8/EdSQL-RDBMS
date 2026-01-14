-- EdSQL v5.0 - Complete Feature Demonstration Script
-- Covers ALL commands from HELP menu + tests.py validation
-- SUITE 1: USER MANAGEMENT (Root Only)
CREATE USER alice_dev alicepass rw
CREATE USER bob_viewer bobpass read_only
-- Note: Try logging out and back in as bob_viewer to see restricted permissions
-- SUITE 2: DATABASE MANAGEMENT
CREATE DATABASE company_db
CREATE DATABASE test_db
SHOW DATABASES
USE company_db
-- Note: Prompt should now show "admin@company_db>"
-- SUITE 3: TABLE CREATION WITH STRICT TYPING
-- Syntax: CREATE TABLE [name] [col:type,col:type,...]
CREATE TABLE departments id:int,dept_name:str,budget:int
CREATE TABLE employees id:int,name:str,salary:int,dept_id:int

-- Show all tables in current database
SHOW TABLES

-- SUITE 4: INDEXING FOR O(1) LOOKUPS
-- Syntax: CREATE_INDEX [table] [column]
CREATE_INDEX employees dept_id
CREATE_INDEX departments id

-- SUITE 5: DATA INSERTION (CRUD - Create)
-- Syntax: INSERT INTO [table] [val1,val2,val3,...]
-- Note: Values must match column order exactly
-- Insert Departments (Parent Table First for FK)
INSERT INTO departments 1,Engineering,500000
INSERT INTO departments 2,Sales,300000
INSERT INTO departments 3,HR,200000
INSERT INTO departments 4,Marketing,250000

-- Insert Employees (Child Table - References dept_id)
INSERT INTO employees 101,Alice Engineer,120000,1
INSERT INTO employees 102,Bob Sales Lead,95000,2
INSERT INTO employees 103,Carol Dev,115000,1
INSERT INTO employees 104,David HR Manager,85000,3

-- SUITE 6: QUERYING (CRUD - Read)
-- Syntax: SELECT * FROM [table] (WHERE [col] [val])
-- Simple SELECT (All rows)
SELECT * FROM departments

-- WHERE Clause (Uses Index if available)
SELECT * FROM employees WHERE dept_id 1

-- SUITE 7: DATA UPDATES (CRUD - Update)
-- Syntax: UPDATE [table] [pk_value] [col:new_value]
-- Give Bob a raise
UPDATE employees 102 salary:105000

-- Promote Alice to different department
UPDATE employees 101 dept_id:2

-- Verify the changes
SELECT * FROM employees WHERE id 102
SELECT * FROM employees WHERE id 101

-- SUITE 8: ADVANCED JOINS
-- Syntax: SELECT * FROM [t1] [TYPE] JOIN [t2] ON [key1] [key2]
-- INNER JOIN (Only matching records)
SELECT * FROM employees INNER JOIN departments ON dept_id id

-- LEFT JOIN (All employees + their departments)
SELECT * FROM employees LEFT JOIN departments ON dept_id id

-- RIGHT JOIN (All departments, even without employees)
SELECT * FROM employees RIGHT JOIN departments ON dept_id id

-- CROSS JOIN (Cartesian Product - every combination)
SELECT * FROM employees CROSS JOIN departments ON dept_id id

-- SUITE 9: DATA DELETION (CRUD - Delete)
-- Syntax: DELETE FROM [table] [pk_value]

-- Remove an employee
DELETE FROM employees 104

-- Verify deletion
SELECT * FROM employees

-- SUITE 10: CONSTRAINT VALIDATION TESTS
-- These commands SHOULD FAIL - Uncomment to test error handling
-- Test 1: Foreign Key Constraint (Should FAIL)
 INSERT INTO employees 999,Hacker,70000,99
-- Expected: "Foreign Key Constraint Failed: Value '99' not found in 'departments'"

-- Test 2: Duplicate Primary Key (Should FAIL)
 INSERT INTO employees 101,Duplicate Person,50000,1
-- Expected: "Duplicate PK: 101"

-- Test 3: Type Validation (Should FAIL)
 INSERT INTO employees NotANumber,Bad Data,InvalidSalary,1
-- Expected: "Column 'id' expects INT"

-- Test 4: Type Validation on Negative Numbers (Should PASS)
INSERT INTO employees 105,Intern,-5000,2
-- Note: System correctly handles negative integers
-- SUITE 11: TABLE MANAGEMENT
-- Drop a table
DROP TABLE employees

-- Verify it's gone
SHOW TABLES

-- Recreate it (demonstrating schema flexibility)
CREATE TABLE employees id:int,name:str,dept_id:int
-- SUITE 12: DATABASE CLEANUP
-- Switch back to default
USE default_db

-- Drop the test database
DROP DATABASE test_db

-- Verify
SHOW DATABASES

-- SUITE 13: USER CLEANUP (Root Only)
DROP USER alice_dev
DROP USER bob_viewer

-- 🎉 DEMONSTRATION COMPLETE!
-- Summary of Features Tested:
--  User Management (CREATE/DROP USER)
--  Database Management (CREATE/DROP/USE/SHOW)
--  Table Management (CREATE/DROP/SHOW with strict typing)
--  Indexing (CREATE_INDEX for O(1) lookups)
--  Full CRUD (INSERT/SELECT/UPDATE/DELETE)
--  Advanced Queries (WHERE clauses with index usage)
--  All 4 Join Types (INNER/LEFT/RIGHT/CROSS)
--  Constraint Enforcement (FK, PK, Type Validation)
--  Negative Number Handling
-- Type 'exit' to close the CLI
