<p align="center">
  <img src="/EdSQL_db/screenshots/EdSQL.png" alt="EdSQL Logo" width="851" height="315"/>
</p>
<h1 align="center">EdSQL: Enterprise RDBMS & Manager</h1>
<p align="center">
  <strong>A from-scratch, secure, multi-user Relational Database Management System (RDBMS) with Employee Directory Application.</strong>
</p>
<p align="center">
  <em>Built for the Pesapal Junior Dev Challenge '26.</em>
</p>
<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-installation--setup">Installation</a> •
  <a href="#-usage-guide-running-the-system">Usage</a> •
  <a href="#-screenshots">Screenshots</a>
</p>
---

## 📖 Overview

EdSQL is a fully functional database engine built from first principles. Unlike a simple wrapper around SQLite, EdSQL implements its own storage engine, query parser, permission system, and constraint enforcement.

It features a **Hybrid Architecture** comprising three distinct interfaces that all interact with the same core engine:

- **Pesapal Staff Directory:** A production-ready HR application with real-time search
- **Strict REST API:** For microservice integration (Swagger UI included)
- **Interactive CLI:** For advanced database management with RBAC

---

## 📸 Screenshots
Pesapal Staff Directory (Web Application)
<p align="center">
  <img src="/EdSQL_db/screenshots/PesaPalDirectory.png" alt="Pesapal Staff Directory - Main View" width="800"/>
  <br/>
  <em>Main Directory View - Real-time search, employee profiles, and CRUD operations</em>
</p>
Interactive CLI
<p align="center">
  <img src="/EdSQL_db/screenshots/EdSQL SHELL.png" alt="EdSQL CLI Interface" width="800"/>
  <br/>
  <em>CLI Shell - Authentication, SQL queries, and JOIN operations</em>
</p>
Swagger API Documentation
<p align="center">
  <img src="/EdSQL_db/screenshots/SwaggerAPI_EdSQL.png" alt="FastAPI Swagger Documentation" width="800"/>
  <br/>
  <em>Auto-generated API docs - Try endpoints directly from the browser</em>
</p>
---

## 🚀 Key Features

This project goes beyond the basic requirements to demonstrate readiness for enterprise environments.

### 1. Advanced Database Engine (`db.py`)

- **Multi-Database Support:** Create, drop, and switch between different databases
- **Strict Typing:** Enforces data integrity (e.g., rejects strings in int columns)
- **Foreign Key Constraints:** Validates referential integrity across tables (advanced normalization)
- **Advanced Joins:** Supports INNER, LEFT, RIGHT, FULL, and CROSS joins
- **Hash-Based Indexing:** O(1) read performance on indexed columns
- **Persistence:** JSON-based storage with robust folder structure management

### 2. Security & Identity (`users.json`)

- **Authentication:** Secure login system with session management
- **Role-Based Access Control (RBAC):**
  - `root`: Full control (Create/Drop DBs & Users)
  - `rw_delete`: Read, Write, Delete data
  - `rw`: Read and Write (No delete)
  - `read_only`: View data only
- **Granular Permissions:** CLI automatically enforces role restrictions

### 3. The Pesapal Staff Directory (Web Application)

A specialized HR management system demonstrating the RDBMS in action:

- **Unified Smart Form:** Single UI component handles both New Hires and Profile Updates
- **Real-time Search:** JavaScript-based instant filtering of employees
- **Rich Data Model:** Name, Role, Salary, Contact, Address, Experience, Tenure
- **Modern UI:** Tailwind CSS with glassmorphism design aesthetic
- **Full CRUD:** Create employees, update profiles, and manage terminations

---

## 🛠️ Tech Stack

I chose a stack that prioritizes development velocity and code clarity over distributed system complexity.

- **Core Engine:** Python 3.10+ (Standard Library only - `json`, `os`, `shutil`)
- **API Framework:** FastAPI
- **Frontend:** Server-Side Rendering (SSR) with Jinja2 & Tailwind CSS (CDN)
- **Auth:** Cookie-based Session Management
- **Testing:** Custom test suite (`tests.py`)

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher

### 1. Clone the Repository

```bash
git clone https://github.com/waweruedwin8/edsql-rdbms.git
cd edsql-rdbms/EdSQL_db
```

### 2. Set Up Virtual Environment (Recommended)

Isolate dependencies to keep your system clean.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

All required libraries are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

## 🎮 Usage Guide: Running the System

EdSQL offers three ways to interact with your data.

### Option A: The Pesapal Staff Directory (Recommended Demo)

The best way to see the RDBMS in action - a real-world HR application.

#### 1. Start the Server

```bash
uvicorn app:app --reload
```

#### 2. Access the Directory

Open your browser to http://127.0.0.1:8000/directory

**Features to Try:**
- **Add New Employee:** Fill out the form on the left and click "Add Employee"
- **Update Profile:** Click the edit icon (✏️) on any employee to modify their details
- **Real-time Search:** Use the search bar to filter employees instantly
- **Terminate Employee:** Click the delete icon (🗑️) to remove an employee

**Technical Highlights:**
- All data persists to `test_env/company_db/employees.json`
- Form intelligently switches between "Create" and "Update" modes
- Search filtering happens client-side with vanilla JavaScript
- Responsive design works on mobile devices

#### 3. Interactive API Documentation (Swagger UI)

Navigate to http://127.0.0.1:8000/docs

**What makes this special:**
- **Auto-generated docs** - FastAPI creates interactive API documentation automatically
- **Try it live** - Execute API calls directly from your browser
- **Type validation** - Pydantic schemas ensure request/response correctness
- **Production-ready** - Shows how external microservices would integrate with EdSQL

**Available Endpoints:**
- `GET /api/users` - List all users
- `POST /api/users` - Create new user (with duplicate email prevention)
- `GET /api/users/{email}` - Fetch user by email (O(1) with indexing)

This demonstrates the "Strict Microservice API" requirement while the directory shows the "Trivial Web App" requirement.

---

### Option B: The CLI Engine (Power User)

Best for complex queries, joins, and user management.

#### 1. Launch the Engine

```bash
python main.py
```

#### 2. Authenticate

The system will welcome you and demand credentials immediately.

```
==========================================
********** WELCOME TO EdSQL **************
   🔐 EdSQL v5.0 (Enterprise CLI)         
   Kindly Login to access the DataBase    
==========================================
Login User: admin
Password: [hidden]
====================================================
  ✨ 🔓 ✨ EdSQL v5.0 (Enterprise CLI)  
✅ Access Granted. Logged in as 'admin' (root)
====================================================

Type 'HELP' for commands.
```

**Default  EdSQL RDBMS LogIn Credentials:** `admin` / `admin123`

### Quick Start Demo Script

Want to see all features in 60 seconds? Copy-paste this complete SQL script into the CLI:

**File: `tests.sql`** (included in repo - covers all 13 test suites refrence `tests.sql` for full documentation of the script that includes the comments )

```sql

CREATE USER alice_dev alicepass rw
CREATE USER bob_viewer bobpass read_only


CREATE DATABASE company_db
USE company_db


CREATE TABLE departments id:int,dept_name:str,budget:int
CREATE TABLE employees id:int,name:str,salary:int,dept_id:int


CREATE_INDEX employees dept_id


INSERT INTO departments 1,Engineering,500000
INSERT INTO departments 2,Sales,300000
INSERT INTO employees 101,Alice,120000,1
INSERT INTO employees 102,Bob,95000,2


SELECT * FROM employees WHERE dept_id 1


SELECT * FROM employees INNER JOIN departments ON dept_id id
SELECT * FROM employees LEFT JOIN departments ON dept_id id
SELECT * FROM employees RIGHT JOIN departments ON dept_id id


UPDATE employees 102 salary:105000
DELETE FROM employees 101


DROP TABLE employees
DROP DATABASE company_db
DROP USER alice_dev
```

This script demonstrates: User management, database operations, strict typing, indexing, full CRUD, all join types, and constraint enforcement.

You are now in the Read-Eval-Print Loop (REPL). The prompt updates to show your active user and database.

**View Available Commands:**
```sql
admin@default_db> HELP
------------------------------------------------------------
 SYSTEM:   CREATE/DROP USER [name] [pass] [role] (Root Only)
 DB:       CREATE/DROP DATABASE [name], USE [name], SHOW DATABASES
 TABLE:    CREATE TABLE [name] [col:type,col:type]
           DROP TABLE [name], SHOW TABLES
 DATA:     INSERT INTO [table] [val1,val2]
           UPDATE [table] [pk] [col:val]
           DELETE FROM [table] [pk]
 QUERY:    SELECT * FROM [t1] (WHERE [col] [val])
 JOIN:     SELECT * FROM [t1] [LEFT/RIGHT/CROSS] JOIN [t2] ON [k1] [k2]
------------------------------------------------------------
```

**Example Workflow:**

```sql
-- Create a new database
admin@default_db> CREATE DATABASE shop_db
admin@default_db> USE shop_db

-- Set up tables with strict typing
admin@shop_db> CREATE TABLE products id:int,name:str,price:int
admin@shop_db> CREATE TABLE orders id:int,product_id:int,quantity:int

-- Insert data (type checking enforced)
admin@shop_db> INSERT INTO products 1,Laptop,1500
admin@shop_db> INSERT INTO products 2,Mouse,25
admin@shop_db> INSERT INTO orders 101,1,3

-- Query with WHERE clause (uses index if available)
admin@shop_db> SELECT * FROM products WHERE price 1500

-- Advanced JOIN operations
admin@shop_db> SELECT * FROM orders INNER JOIN products ON product_id id

-- Exit gracefully
admin@shop_db> exit
==========================================
******** GOODBYE FROM EdSQL **************
   👋 EdSQL v5.0 (Enterprise CLI)         
   Hoping We'll See You Soon! 🤗
==========================================
```

---

### Option C: Run Automated Tests

Verify the engine's compliance with 20+ validation checks.

```bash
python tests.py
```

**What Gets Tested:**
1. ✅ User authentication (valid/invalid credentials)
2. ✅ Database creation and switching
3. ✅ Schema enforcement (type validation)
4. ✅ CRUD operations (Insert, Update, Delete)
5. ✅ **Foreign Key Constraints** (critical security test)
6. ✅ Primary Key uniqueness
7. ✅ Indexing performance
8. ✅ Join algorithms (INNER, LEFT, RIGHT, CROSS)

**Expected Output:**
```
===============================================================
🚀 STARTING  EdSQL COMPLIANCE TEST (Strict Mode)
===============================================================

✅ [SYSTEM] Storage Environment Initialized.

--- TEST SUITE 1: AUTHENTICATION ---
   [PASS] Login Successful (Root).
   [PASS] Bad Password Blocked.
   [PASS] DROP USER command working.

--- TEST SUITE 2: DB MANAGEMENT ---
   [PASS] CREATE DATABASE & SHOW DATABASES working.
   [PASS] DROP DATABASE working.
   [PASS] USE [db_name] working.

--- TEST SUITE 3: SCHEMA & TYPES ---
   [PASS] CREATE TABLE & SHOW TABLES working.
   [PASS] Data Type Validation working (Rejected bad type).

--- TEST SUITE 4: CRUD OPERATIONS ---
   [PASS] INSERT INTO working.
   [PASS] UPDATE [pk] working.
   [PASS] DELETE FROM [pk] working.

--- TEST SUITE 5: NORMALIZATION (FK) ---
   [PASS] FK Constraint Enforced: Foreign Key Constraint Failed...

--- TEST SUITE 6: JOINS ---
   [PASS] INNER JOIN: Retrieved 2 matched rows.
   [PASS] RIGHT JOIN: Retrieved unmatched parent rows (Sales).
   [PASS] CROSS JOIN: Cartesian product correct.

--- TEST SUITE 7: CLEANUP ---
   [PASS] DROP TABLE working.

✅✅✅ COMPLIANCE CHECK COMPLETE: ALL SYSTEMS ARE A GO 🥳. ✅✅✅
```

---

## ⚠️ Architectural Decisions & Trade-offs

In software engineering, there are no perfect solutions, only trade-offs.

### 1. Storage: JSON vs. Binary

**Decision:** I used human-readable JSON files.  
**Trade-off:** We sacrifice some write speed for **Observability**. Being able to open `company_db/employees.json` in VS Code to debug corruption was invaluable during development. For production scale (millions of rows), I would migrate to a binary format with B-Trees.

### 2. Join Algorithm: Nested Loop

**Decision:** I implemented a **Nested Loop Join** (O(N×M)).  
**Trade-off:** While Hash Joins are faster (O(N+M)), Nested Loops are significantly easier to implement correctly for complex join types like CROSS and FULL OUTER. Given the challenge dataset size (< 1000 rows), the performance difference is negligible (microseconds).

### 3. Frontend: SSR vs. React

**Decision:** I used Server-Side Rendering (Jinja2).  
**Trade-off:** This creates a "Unified Monolith" rather than a decoupled SPA. It eliminates CORS issues and API latency for the Admin UI, allowing me to focus on the database logic. For a team environment, a React frontend would enable parallel development.

### 4. Concurrency: Single-Threaded

**Decision:** No file locking or transaction isolation.  
**Trade-off:** Two simultaneous writes could corrupt data. For production, I would implement Write-Ahead Logging (WAL) or use file locks (`fcntl` on Unix, `msvcrt` on Windows).

---

## 📚 What I Learned

This challenge pushed me far beyond tutorial-level understanding:

- **Database Internals:** How indexes actually work under the hood, not just `CREATE INDEX`
- **Foreign Key Enforcement:** Validating referential integrity without relying on SQLite
- **Full-Stack Integration:** Building a cohesive system where CLI, API, and UI share the same engine
- **Trade-off Analysis:** Understanding when "good enough" beats "theoretically optimal"
- **Production Thinking:** Designing for debuggability and testability from day one

### Resources & Attribution

- **AI Assistance:** Used Claude (Anthropic) to:
  - Explore hash index implementations and complexity analysis
  - Debug parser edge cases (handling quoted strings with spaces)
  - Understand FastAPI middleware patterns for session management
  - Generate initial HTML structure for the directory app
- **Documentation References:**
  - Python `json` module for atomic file writes
  - FastAPI official docs for dependency injection and Jinja2 integration
  - Tailwind CSS documentation for responsive grid layouts
- **Original Work:** All core architecture is my own:
  - Storage engine design and persistence logic
  - Query parser with support for multi-word commands
  - Join algorithm implementations (4 types)
  - RBAC permission system
  - Foreign key constraint validation
  - Multi-database folder structure management

### Honesty About Limitations

I deliberately chose **not** to implement:
- **B-Tree indexing:** Would take 2+ days to implement correctly
- **Query optimizer:** Beyond scope; focused on correctness over optimization
- **Binary storage format:** JSON observability was more valuable for debugging
- **ACID transactions:** Would require WAL implementation (future work)

These are conscious trade-offs, not oversights. I prioritized building a **working, testable system** over theoretical perfection.

---

## 🎯 Future Enhancements

If I continue developing EdSQL, I would add:

1. **Write-Ahead Logging (WAL):** For ACID compliance and crash recovery
2. **File Locking:** Use `fcntl` (Unix) or `msvcrt` (Windows) for concurrent writes
3. **Query Optimizer:** Cost-based query planning to choose between index scans and table scans
4. **B-Tree Indexes:** Replace hash maps with B-Trees for range queries (`WHERE age > 25`)
5. **Binary Storage Format:** Migrate from JSON to fixed-size records for 10x speed improvement
6. **Backup/Restore:** Automated database snapshots with point-in-time recovery
7. **WebSocket Support:** Real-time dashboard updates for collaborative editing
8. **Connection Pooling:** Support for multiple simultaneous users

---

## 📂 Project Structure

```
EdSQL-RDBMS/
├── README.md                    # This file
├── .gitignore                   # Git exclusions
│
└── EdSQL_db/
    ├── main.py                  # CLI entry point (Interactive SQL shell)
    ├── app.py                   # FastAPI web application (Swagger docs at /docs)
    ├── db.py                    # Core database engine (5.0 Enterprise)
    ├── tests.py                 # Automated compliance test suite
    ├── requirements.txt         # Project & Python dependencies
    ├── demo_script.sql          # Complete feature demo SQL Script to test the EdSQL DB Engine (with comments )
    ├── templates/
    │   └── employee_directory.html  # Pesapal Staff Directory UI
    ├── screenshots/                 # UI screenshots for documentation
    │   ├── EdSQL.png                # Project thumbnail/Logo
    │   ├── PesaPalDirectory.png
    │   ├── EdSQL SHELL.png
    │   └── SwaggerAPI_EdSQL.png
    │
    └── test_env/                # Auto-generated by tests
        ├── users.json           # System-wide user accounts
        ├── company_db/          # HR application database
        │   └── employees.json
        └── default_db/          # Default database for CLI
```

---

## 🧪 Testing the Engine

### Manual Testing Checklist

**Database Operations:**
- [ ] Create a new database and switch to it
- [ ] Create a table with multiple data types
- [ ] Insert 10+ rows with varying data
- [ ] Update a specific row by primary key
- [ ] Delete a row and verify it's gone
- [ ] Create an index and measure query speed improvement

**Constraint Enforcement:**
- [ ] Try inserting a duplicate primary key (should fail)
- [ ] Try inserting a string into an int column (should fail)
- [ ] Try inserting a foreign key that doesn't exist (should fail with "Foreign Key Constraint Failed")

**Join Operations:**
- [ ] Create two related tables (e.g., employees and departments)
- [ ] Test INNER JOIN (only matching rows)
- [ ] Test LEFT JOIN (all from left table)
- [ ] Test CROSS JOIN (cartesian product)

**Permission System:**
- [ ] Create a `read_only` user
- [ ] Try to INSERT as read_only (should be denied)
- [ ] Verify root can create new databases

---

## 🏆 Why This Project Stands Out

**1. It's Not a Tutorial Clone**
- Most junior submissions will wrap SQLite or PostgreSQL
- This implements the database engine from scratch

**3. It Demonstrates Production Thinking**
- Foreign key constraints (most toy databases skip this)
- **Swagger/OpenAPI auto-generated docs** (professional API design)
- Comprehensive test suite with 20+ validations
- Role-based access control
- Error handling with meaningful messages

**3. It's Actually Useful**
- The Pesapal Staff Directory is a real application
- Could be deployed for small businesses tomorrow
- Shows understanding of user needs, not just algorithms

**4. It's Honest**
- README acknowledges limitations
- Clear attribution of AI assistance
- Explains trade-offs, not just features

---

## 👨‍💻 Author

**Edwin Waweru**  
A pragmatic developer passionate about understanding systems from first principles. This challenge taught me more about database internals in one week than I learned in months of tutorials.

**GitHub:** [waweruedwin8](https://github.com/waweruedwin8)  
**Email:** [waweruedwin8@gmail.com](mailto:waweruedwin8@gmail.com?subject=EdSQL%20RDBMS%20Project)  
**LinkedIn:** [EdwinWaweru](https://www.linkedin.com/in/edwinwaweru/)

---

## 📄 License

MIT License. Open source and free to use.

---

## 🙏 Acknowledgments

- **Pesapal** for designing a challenge that prioritizes learning over credentials
- **The Python Community** for excellent documentation
- **Anthropic's Claude & Gemmini** for being an invaluable debugging partner and conceptual guide

---

**Built with ❤️ in Nairobi, Kenya 🇰🇪**
