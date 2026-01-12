import sys
import getpass
import time
from db import Database

# --- PERMISSIONS CONFIG ---
# Define what commands each role can execute
PERMS = {
    "root": ["ALL"],
    "rw_delete": ["SELECT", "INSERT", "UPDATE", "DELETE", "USE", "SHOW", "HELP", "EXIT"],
    "rw": ["SELECT", "INSERT", "UPDATE", "USE", "SHOW", "HELP", "EXIT"],
    "read_only": ["SELECT", "USE", "SHOW", "HELP", "EXIT"]
}

def check(role, cmd):
    """Checks if the current user's role allows the command"""
    allowed = PERMS.get(role, [])
    if "ALL" in allowed: return True
    return cmd in allowed

def print_table(rows):
    """Prints a nicely formatted ASCII table"""
    if not rows:
        print("(No results)")
        return
    
    # Get headers
    headers = list(rows[0].keys())
    
    # Calculate widths
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            val = str(row.get(h, "NULL"))
            widths[h] = max(widths[h], len(val))
            
    # Print Header
    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    sep_line = "-" * len(header_line)
    
    print(sep_line)
    print(header_line)
    print(sep_line)
    
    # Print Rows
    for row in rows:
        vals = [str(row.get(h, "NULL")).ljust(widths[h]) for h in headers]
        print(" | ".join(vals))
    print(f"\n({len(rows)} row(s) returned)")

def main():
    print("==========================================")
    print("********** WELCOME TO EdSQL **************")
    print("   🔐 EdSQL v5.0 (Enterprise CLI)         ")
    print("   Kindly Login to access the DataBase    ")
    print("==========================================")
    
    db = Database()
    
    # --- 1. LOGIN LOOP ---
    current_user = None
    current_role = None
    
    while not current_user:
        u = input("Login User: ").strip()
        if not u: continue
        p = getpass.getpass("Password: ")
        
        role = db.authenticate(u, p)
        if role:
            current_user = u
            current_role = role
            print("====================================================")
            print("   ✨ 🔓 ✨ EdSQL v5.0 (Enterprise CLI)  ")
            print(f"✅ Access Granted. Logged in as '{u}' ({role})")
            print("====================================================")
        else:
            print("❌ Login Failed. HINT: Default is admin / admin123")

    # --- 2. COMMAND LOOP ---
    print("\nType 'HELP' for commands.")
    
    while True:
        try:
            # Context-aware prompt: admin@company_db>
            prompt = f"\n{current_user}@{db.current_db}> "
            line = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
            
        if not line: continue
        parts = line.split()
        cmd = parts[0].upper()
        
        # --- EXIT ---
        if cmd == "EXIT":
            print("=" * 42)
            print("******** GOODBYE FROM EdSQL **************")
            print("   👋 EdSQL v5.0 (Enterprise CLI)         ")
            print("   Hoping We'll See You Soon! 🤗")
            print("=" * 42)
            break
            
        # --- HELP ---
        elif cmd == "HELP":
            print("-" * 60)
            print(" SYSTEM:   CREATE/DROP USER [name] [pass] [role] (Root Only)")
            print(" DB:       CREATE/DROP DATABASE [name], USE [name], SHOW DATABASES")
            print(" TABLE:    CREATE TABLE [name] [col:type,col:type]")
            print("           DROP TABLE [name], SHOW TABLES")
            print(" DATA:     INSERT INTO [table] [val1,val2]")
            print("           UPDATE [table] [pk] [col:val]")
            print("           DELETE FROM [table] [pk]")
            print(" QUERY:    SELECT * FROM [t1] (WHERE [col] [val])")
            print(" JOIN:     SELECT * FROM [t1] [LEFT/RIGHT/CROSS] JOIN [t2] ON [k1] [k2]")
            print("-" * 60)
            continue

        # --- PERMISSION CHECK ---
        # Some commands are Root-only regardless of the PERMS list
        root_only_cmds = ["CREATE_USER", "DROP_USER", "CREATE_DATABASE", "DROP_DATABASE"]
        
        # Construct specific action key for granular checks
        action_key = cmd
        if len(parts) > 1:
            if cmd == "CREATE" and parts[1].upper() == "USER": action_key = "CREATE_USER"
            if cmd == "DROP" and parts[1].upper() == "USER": action_key = "DROP_USER"
            if cmd == "CREATE" and parts[1].upper() == "DATABASE": action_key = "CREATE_DATABASE"
            if cmd == "DROP" and parts[1].upper() == "DATABASE": action_key = "DROP_DATABASE"

        if action_key in root_only_cmds and current_role != "root":
            print("❌ Permission Denied: Root access required.")
            continue
            
        if not check(current_role, cmd):
            print(f"❌ Permission Denied: Role '{current_role}' cannot perform '{cmd}'.")
            continue

        # --- EXECUTE COMMANDS ---

        # 1. USER MANAGEMENT
        if action_key == "CREATE_USER":
            # CREATE USER bob pass123 read_only
            try:
                db.create_user(parts[2], parts[3], parts[4])
                print(f"User '{parts[2]}' created.")
            except IndexError: print("Usage: CREATE USER [name] [pass] [role]")
            except ValueError as e: print(f"Error: {e}")

        elif action_key == "DROP_USER":
            try:
                db.drop_user(parts[2])
                print(f"User '{parts[2]}' deleted.")
            except ValueError as e: print(f"Error: {e}")

        # 2. DATABASE MANAGEMENT
        elif action_key == "CREATE_DATABASE":
            db.create_database(parts[2])
            print(f"Database '{parts[2]}' created.")

        elif action_key == "DROP_DATABASE":
            db.drop_database(parts[2])
            print(f"Database '{parts[2]}' dropped.")

        elif cmd == "USE":
            db.use_database(parts[1])

        elif cmd == "SHOW" and len(parts) > 1:
            if parts[1].upper() == "DATABASES":
                dbs = db.show_databases()
                print("\nDatabases:")
                for d in dbs: print(f" - {d}")
            elif parts[1].upper() == "TABLES":
                tbls = db.show_tables()
                print(f"\nTables in {db.current_db}:")
                if not tbls: print(" (empty)")
                for t in tbls: print(f" - {t}")

        # 3. TABLE MANAGEMENT
        elif cmd == "CREATE" and parts[1].upper() == "TABLE":
            # CREATE TABLE users id:int,name:str
            if len(parts) < 4:
                print("Usage: CREATE TABLE [name] [col:type,...]")
                continue
            name = parts[2]
            col_defs = parts[3].split(",")
            cols = []
            types = {}
            for c in col_defs:
                if ":" in c:
                    cn, ct = c.split(":")
                    cols.append(cn)
                    types[cn] = ct
                else:
                    cols.append(c)
            db.create_table(name, cols, types, primary_key=cols[0])
            print(f"Table '{name}' created.")

        elif cmd == "DROP" and parts[1].upper() == "TABLE":
            if db.drop_table(parts[2]):
                print("Table dropped.")
            else:
                print("Table not found.")

        # 4. DATA MANIPULATION
        elif cmd == "INSERT" and parts[1].upper() == "INTO":
            # INSERT INTO users 1,Bob
            if len(parts) < 4:
                print("Usage: INSERT INTO [table] [val,val]")
                continue
            t = db.get_table(parts[2])
            if t:
                vals = [v.strip() for v in parts[3].split(",")]
                try:
                    t.insert(vals)
                    print("Row inserted.")
                except Exception as e:
                    print(f"❌ Insert Error: {e}")
            else:
                print("Table not found.")

        elif cmd == "UPDATE":
            # UPDATE users 1 role:admin
            if len(parts) < 4:
                print("Usage: UPDATE [table] [pk] [col:val]")
                continue
            t = db.get_table(parts[1])
            pk = parts[2]
            try:
                col, val = parts[3].split(":", 1)
                if t and t.update(pk, {col: val}):
                    print("Row updated.")
                else:
                    print("Update failed (ID not found).")
            except ValueError:
                print("Error: Use col:val format")

        elif cmd == "DELETE" and parts[1].upper() == "FROM":
            # DELETE FROM users 1
            t = db.get_table(parts[2])
            if t and t.delete(parts[3]):
                print("Row deleted.")
            else:
                print("Delete failed.")

        # 5. QUERYING & JOINS
        elif cmd == "SELECT":
            start_time = time.time()
            
            # --- JOIN LOGIC ---
            if "JOIN" in parts:
                try:
                    # Syntax: SELECT * FROM t1 LEFT JOIN t2 ON k1 k2
                    join_idx = parts.index("JOIN")
                    on_idx = parts.index("ON")
                    
                    t1 = parts[3]
                    t2 = parts[join_idx + 1]
                    k1 = parts[on_idx + 1]
                    k2 = parts[on_idx + 2]
                    
                    # Detect Join Type
                    j_type = "INNER"
                    prev = parts[join_idx - 1].upper()
                    if prev in ["LEFT", "RIGHT", "FULL", "CROSS"]:
                        j_type = prev
                    elif parts[join_idx - 2].upper() == "FULL" and prev == "OUTER":
                         j_type = "FULL"

                    results = db.join(t1, t2, k1, k2, j_type)
                    print_table(results)
                    
                except ValueError:
                    print("Syntax Error. Use: SELECT * FROM t1 [TYPE] JOIN t2 ON k1 k2")
                except Exception as e:
                    print(f"Join Error: {e}")

            # --- STANDARD SELECT ---
            else:
                t_name = parts[3]
                t = db.get_table(t_name)
                if t:
                    if "WHERE" in parts:
                        try:
                            idx = parts.index("WHERE")
                            col = parts[idx + 1]
                            val = parts[idx + 2]
                            print_table(t.select_where(col, val))
                        except:
                            print("Error parsing WHERE.")
                    else:
                        print_table(t.rows)
                else:
                    print(f"Table '{t_name}' not found.")
            
            print(f"⏱️ Time: {(time.time() - start_time):.5f}s")

        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()