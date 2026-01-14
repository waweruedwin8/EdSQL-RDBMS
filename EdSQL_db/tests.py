import os
import shutil
from db import Database

def run_tests():
    print("===============================================================")
    print("🚀 STARTING  EdSQL COMPLIANCE TEST (Strict Mode)")
    print("===============================================================\n")
    
    # --- 1. SETUP & CLEANUP ---
    if os.path.exists("test_env"):
        shutil.rmtree("test_env")
    db = Database(root_folder="test_env")
    print("✅ [SYSTEM] Storage Environment Initialized.")

    #  TEST SUITE 1: USER AUTHENTICATION & MANAGEMENT
    #  Requirement: CREATE/DROP USER, Auth Login
    print("\n--- TEST SUITE 1: AUTHENTICATION ---")
    
    # 1.1 Create User
    db.create_user("admin_user", "securePass", "root")
    db.create_user("guest_user", "guestPass", "read_only")
    
    # 1.2 Authenticate (Success)
    role = db.authenticate("admin_user", "securePass")
    assert role == "root"
    print("   [PASS] Login Successful (Root).")
    
    # 1.3 Authenticate (Failure)
    bad_role = db.authenticate("admin_user", "wrongPass")
    assert bad_role is None
    print("   [PASS] Bad Password Blocked.")
    
    # 1.4 Drop User
    db.drop_user("guest_user")
    deleted_role = db.authenticate("guest_user", "guestPass")
    assert deleted_role is None
    print("   [PASS] DROP USER command working.")


  
    #  TEST SUITE 2: DATABASE MANAGEMENT
    #  Requirement: CREATE/DROP DB, SHOW DBs, USE
    
    print("\n--- TEST SUITE 2: DB MANAGEMENT ---")
    
    # 2.1 Create & Show
    db.create_database("company_db")
    db.create_database("temp_db")
    all_dbs = db.show_databases()
    assert "company_db" in all_dbs
    assert "temp_db" in all_dbs
    print("   [PASS] CREATE DATABASE & SHOW DATABASES working.")
    
    # 2.2 Drop DB
    db.drop_database("temp_db")
    all_dbs_after = db.show_databases()
    assert "temp_db" not in all_dbs_after
    print("   [PASS] DROP DATABASE working.")
    
    # 2.3 Use DB
    db.use_database("company_db")
    assert db.current_db == "company_db"
    print("   [PASS] USE [db_name] working.")


   
    #  TEST SUITE 3: SCHEMA & TYPES
    #  Requirement: CREATE TABLE [col:type], DROP TABLE
    print("\n--- TEST SUITE 3: SCHEMA & TYPES ---")
    
    # 3.1 Create Table with Types (Departments)
    t_dept = db.create_table(
        "departments", 
        ["id", "dept_name"], 
        {"id": "int", "dept_name": "str"}, 
        primary_key="id"
    )
    
    # 3.2 Create Table with FK (Employees)
    t_emp = db.create_table(
        "employees", 
        ["id", "name", "salary", "dept_id"], 
        {"id": "int", "name": "str", "salary": "int", "dept_id": "int"}, 
        primary_key="id"
    )
    # Manually attach FK (Simulating the CLI parser's job)
    t_emp.foreign_keys = {"dept_id": "departments"}
    t_emp.save()
    
    # 3.3 Show Tables
    tables = db.show_tables()
    assert "employees" in tables
    assert "departments" in tables
    print("   [PASS] CREATE TABLE & SHOW TABLES working.")

    # 3.4 Type Validation (Try inserting string into int column)
    try:
        t_dept.insert(["one", "Bad Data"]) 
        print("   [FAIL] Type Validation Failed (Allowed string in int col).")
    except ValueError:
        print("   [PASS] Data Type Validation working (Rejected bad type).")


    #  TEST SUITE 4: CRUD OPERATIONS
    #  Requirement: INSERT, UPDATE, DELETE, SELECT
    print("\n--- TEST SUITE 4: CRUD OPERATIONS ---")
    
    # 4.1 INSERT (Populate Departments)
    t_dept.insert([1, "Engineering"])
    t_dept.insert([2, "HR"])
    t_dept.insert([3, "Sales"])
    print("   [PASS] INSERT INTO working.")

    # 4.2 INSERT (Populate Employees)
    t_emp.insert([101, "Alice", 80000, 1])
    t_emp.insert([102, "Bob", 60000, 2])
    
    # 4.3 UPDATE
    # Update Bob's Salary from 60000 to 65000
    t_emp.update(102, {"salary": 65000})
    bob = t_emp.select_where("id", 102)[0]
    assert int(bob['salary']) == 65000
    print("   [PASS] UPDATE [pk] working.")
    
    # 4.4 DELETE
    # Insert temporary guy then delete him
    t_emp.insert([999, "Temp Guy", 20000, 3])
    t_emp.delete(999)
    check = t_emp.select_where("id", 999)
    assert len(check) == 0
    print("   [PASS] DELETE FROM [pk] working.")


    #  TEST SUITE 5: ADVANCED NORMALIZATION
    #  Requirement: Foreign Key Constraints
    print("\n--- TEST SUITE 5: NORMALIZATION (FK) ---")
    
    try:
        # Try to add employee to Dept ID 99 (Does not exist)
        t_emp.insert([103, "Hacker", 70000, 99])
        print("   [FAIL] FK Constraint Broken (Accepted invalid parent ID).")
    except ValueError as e:
        print(f"   [PASS] FK Constraint Enforced: {e}")


    #  TEST SUITE 6: JOINS
    #  Requirement: INNER, LEFT, RIGHT, CROSS
    print("\n--- TEST SUITE 6: JOINS ---")
    
    # Setup for Joins:
    # Employees: Alice(1), Bob(2)
    # Departments: Eng(1), HR(2), Sales(3)
    
    # 6.1 INNER JOIN (Should match Alice and Bob)
    inner = db.join("employees", "departments", "dept_id", "id", "INNER")
    assert len(inner) == 2
    print(f"   [PASS] INNER JOIN: Retrieved {len(inner)} matched rows.")

    # 6.2 RIGHT JOIN (Should show Sales dept, even though no employee is there)
    right = db.join("employees", "departments", "dept_id", "id", "RIGHT")
    
    # Check if we found the row where dept_name is Sales and name is None
    sales_found = any(r.get('dept_name') == 'Sales' and r.get('name') is None for r in right)
    assert sales_found
    print("   [PASS] RIGHT JOIN: Retrieved unmatched parent rows (Sales).")
    
    # 6.3 CROSS JOIN (Cartesian Product)
    # 2 Employees * 3 Departments = 6 Rows
    cross = db.join("employees", "departments", "dept_id", "id", "CROSS")
    assert len(cross) == 6
    print("   [PASS] CROSS JOIN: Cartesian product correct.")

    
    #  TEST SUITE 7: DESTRUCTIVE CLEANUP
    #  Requirement: DROP TABLE
    print("\n--- TEST SUITE 7: CLEANUP ---")
    
    db.drop_table("employees")
    tables_after = db.show_tables()
    assert "employees" not in tables_after
    print("   [PASS] DROP TABLE working.")

    print("\n✅✅✅ COMPLIANCE CHECK COMPLETE: ALL SYSTEMS ARE A GO 🥳. ✅✅✅")

if __name__ == "__main__":
    run_tests()
