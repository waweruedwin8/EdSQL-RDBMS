import json
import os
import shutil

class Table:
    def __init__(self, name, columns, types=None, primary_key=None, foreign_keys=None, folder="."):
        self.name = name
        self.columns = columns
        self.types = types or {}
        self.primary_key = primary_key
        # Foreign keys support (logic for advanced normalization)
        self.foreign_keys = foreign_keys or {} 
        self.rows = []
        self.indexes = {} 
        self.folder = folder
        self.filename = os.path.join(folder, f"{name}.json")
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.columns = data.get('columns', [])
                    self.types = data.get('types', {})
                    self.primary_key = data.get('primary_key', None)
                    self.foreign_keys = data.get('foreign_keys', {})
                    self.rows = data.get('rows', [])
                    self.indexes = data.get('indexes', {})
            except json.JSONDecodeError:
                print(f"⚠️ {self.filename} corrupted.")
        else:
            self.save()

    def save(self):
        data = {
            "columns": self.columns,
            "types": self.types,
            "primary_key": self.primary_key,
            "foreign_keys": self.foreign_keys,
            "rows": self.rows,
            "indexes": self.indexes
        }
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except PermissionError:
            pass

    # --- INDEXING ---
    def create_index(self, column_name):
        if column_name not in self.columns:
            return
        self.indexes[column_name] = {}
        for idx, row in enumerate(self.rows):
            val = str(row.get(column_name))
            if val not in self.indexes[column_name]:
                self.indexes[column_name][val] = []
            self.indexes[column_name][val].append(idx)
        self.save()

    def select_where(self, column, value):
        """O(1) Lookup if indexed, otherwise O(N)"""
        value = str(value)
        # Use Index if available
        if column in self.indexes:
            row_indices = self.indexes[column].get(value, [])
            return [self.rows[i] for i in row_indices if i < len(self.rows)]
        # Fallback to Linear Search
        return [row for row in self.rows if str(row.get(column)) == value]

    # --- CRUD & VALIDATION ---
    def validate_data(self, row_data):
        for col, val in row_data.items():
            expected = self.types.get(col)
            # Basic type checking (improved to handle negative numbers)
            if expected == 'int' and not str(val).replace('-','').isdigit():
                 raise ValueError(f"Column '{col}' expects INT.")
            elif expected == 'float':
                try:
                    float(val)
                except:
                    raise ValueError(f"Column '{col}' expects FLOAT.")

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError("Column count mismatch")
        row = dict(zip(self.columns, values))
        
        self.validate_data(row)
        
        # --- FOREIGN KEY CHECK (Advanced Normalization Logic) ---
        
        if self.foreign_keys:
            for col, parent_table_name in self.foreign_keys.items():
                val = str(row.get(col))
                # Construct path to parent table
                parent_file = os.path.join(self.folder, f"{parent_table_name}.json")
                
                if not os.path.exists(parent_file):
                    raise ValueError(f"Parent table '{parent_table_name}' does not exist.")
                
                # We must load the parent table to check if ID exists
                with open(parent_file, 'r') as f:
                    p_data = json.load(f)
                    p_pk = p_data.get('primary_key')
                    # Collect all valid IDs from parent
                    existing_ids = [str(r.get(p_pk)) for r in p_data.get('rows', [])]
                    
                if val not in existing_ids:
                    # REJECT the insert if FK is invalid
                    raise ValueError(f"Foreign Key Constraint Failed: Value '{val}' not found in '{parent_table_name}'.")
        # --------------------------------------------

        # Check Primary Key
        if self.primary_key:
            pk_val = str(row[self.primary_key])
            for r in self.rows:
                if str(r.get(self.primary_key)) == pk_val:
                    raise ValueError(f"Duplicate PK: {pk_val}")

        self.rows.append(row)
        
        # Update Indexes
        new_row_idx = len(self.rows) - 1
        for col_name in self.indexes:
            val = str(row.get(col_name))
            if val not in self.indexes[col_name]:
                self.indexes[col_name][val] = []
            self.indexes[col_name][val].append(new_row_idx)

        self.save()
        return True

    def update(self, pk_val, new_data):
        pk_val = str(pk_val)
        updated = False
        for i, row in enumerate(self.rows):
            if str(row.get(self.primary_key)) == pk_val:
                row.update(new_data)
                updated = True
                break
        
        if updated:
            self.save()
            return True
        return False

    def delete(self, pk_val):
        initial = len(self.rows)
        # Filter rows
        self.rows = [r for r in self.rows if str(r.get(self.primary_key)) != str(pk_val)]
        
        if len(self.rows) < initial:
            # Rebuild indexes entirely to stay safe (Lazy approach)
            self.indexes = {} 
            self.save()
            return True
        return False

class Database:
    def __init__(self, root_folder="data"):
        self.root_folder = root_folder
        self.current_db = "default_db"
        self.tables = {}
        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
        self.create_database("default_db")
        self.ensure_system_tables()

    def ensure_system_tables(self):
        self.users_file = os.path.join(self.root_folder, "users.json")
        if not os.path.exists(self.users_file):
            default_users = {"admin": {"pass": "admin123", "role": "root"}}
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f)

    # --- USER MANAGEMENT ---
    def get_users(self):
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def create_user(self, username, password, role="read_only"):
        users = self.get_users()
        if username in users:
            raise ValueError("User exists")
        users[username] = {"pass": password, "role": role}
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

    def drop_user(self, username):
        users = self.get_users()
        if username == "admin": raise ValueError("Cannot drop root")
        if username in users:
            del users[username]
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=4)

    def authenticate(self, username, password):
        users = self.get_users()
        if username in users and users[username]["pass"] == password:
            return users[username]["role"]
        return None

    # --- DB MANAGEMENT ---
    def create_database(self, db_name):
        path = os.path.join(self.root_folder, db_name)
        if not os.path.exists(path):
            os.makedirs(path)

    def drop_database(self, db_name):
        path = os.path.join(self.root_folder, db_name)
        if os.path.exists(path):
            shutil.rmtree(path)
            if self.current_db == db_name: self.current_db = "default_db"

    def use_database(self, db_name):
        path = os.path.join(self.root_folder, db_name)
        if os.path.exists(path):
            self.current_db = db_name
            self.tables = {}

    def get_db_path(self):
        return os.path.join(self.root_folder, self.current_db)

    def show_databases(self):
        return [d for d in os.listdir(self.root_folder) if os.path.isdir(os.path.join(self.root_folder, d))]

    def create_table(self, name, columns, types=None, primary_key=None):
        path = self.get_db_path()
        t = Table(name, columns, types, primary_key, folder=path)
        self.tables[name] = t
        return t

    def get_table(self, name):
        if name in self.tables: return self.tables[name]
        path = self.get_db_path()
        if os.path.exists(os.path.join(path, f"{name}.json")):
            t = Table(name, [], folder=path)
            self.tables[name] = t
            return t
        return None

    def drop_table(self, name):
        path = os.path.join(self.get_db_path(), f"{name}.json")
        if os.path.exists(path):
            os.remove(path)
            if name in self.tables: del self.tables[name]
            return True
        return False

    def show_tables(self):
        path = self.get_db_path()
        return [f[:-5] for f in os.listdir(path) if f.endswith('.json')]

    # --- ADVANCED JOINS ---
    def join(self, t1_name, t2_name, key1, key2, join_type="INNER"):
        
        t1 = self.get_table(t1_name)
        t2 = self.get_table(t2_name)
        if not t1 or not t2: return []

        results = []
        # Helper to get empty columns for NULL filling
        t2_cols_empty = {col: None for col in t2.columns}
        t1_cols_empty = {col: None for col in t1.columns}

        t1_matched_indices = set()
        t2_matched_indices = set()

        # 1. CROSS JOIN
        if join_type == "CROSS":
            for r1 in t1.rows:
                for r2 in t2.rows:
                    results.append({**r1, **r2})
            return results

        # 2. INNER, LEFT, RIGHT, FULL
        for i, r1 in enumerate(t1.rows):
            match_found = False
            for j, r2 in enumerate(t2.rows):
                val1 = str(r1.get(key1))
                val2 = str(r2.get(key2))
                
                if val1 == val2:
                    results.append({**r1, **r2})
                    t1_matched_indices.add(i)
                    t2_matched_indices.add(j)
                    match_found = True
            
            # Left Join Logic: If no match found for this row in t1, append with empty t2 columns
            if not match_found and (join_type in ["LEFT", "FULL", "OUTER"]):
                results.append({**r1, **t2_cols_empty})

        # Right/Full Join Logic: Find rows in t2 that were never matched
        if join_type in ["RIGHT", "FULL", "OUTER"]:
            for j, r2 in enumerate(t2.rows):
                if j not in t2_matched_indices:
                    results.append({**t1_cols_empty, **r2})

        return results