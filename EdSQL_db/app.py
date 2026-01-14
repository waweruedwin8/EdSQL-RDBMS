from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from db import Database 

# --- 1. INITIALIZATION ---
app = FastAPI(
    title="EdSQL RDBMS",
    description="A Hybrid System: Employee Directory App + Strict Microservice API",
    version="5.0.0"
)
db = Database()
templates = Jinja2Templates(directory="templates")

# --- 2. SETUP DATA (Runs on Startup) ---

# A. Setup "company_db" with NEW FIELDS for the Directory App
db.create_database("company_db")
db.use_database("company_db")

# Expanded Schema: includes contact, address, experience, tenure
db.create_table(
    "employees", 
    ["id", "name", "role", "salary", "contact", "address", "experience", "tenure"], 
    types={
        "id": "int", 
        "name": "str", 
        "role": "str", 
        "salary": "int",
        "contact": "str",
        "address": "str",
        "experience": "int",
        "tenure": "int"
    }, 
    primary_key="id"
)

# Seed with some initial data (Only if table is empty)
try:
    t_emp = db.get_table("employees")
    if len(t_emp.rows) == 0:
        # id, name, role, salary, contact, address, experience, tenure
        t_emp.insert([101, "Alice Engineer", "Software Dev", 120000, "alice@pesapal.com", "Nairobi, KE", 5, 2])
        t_emp.insert([102, "Bob Manager", "Project Lead", 145000, "bob@pesapal.com", "Mombasa, KE", 8, 4])
except:
    pass 

# B. Setup "api_service_db" for the Swagger API Demo (Legacy)
db.create_database("api_service_db")
db.use_database("api_service_db")
db.create_table(
    "api_users", 
    ["id", "name", "email"], 
    types={"id": "int", "name": "str", "email": "str"}, 
    primary_key="id"
)
db.get_table("api_users").create_index("email")


# --- 3. ROOT REDIRECT ---
@app.get("/", include_in_schema=False)
async def root():
    """Redirects root users to the directory app"""
    return RedirectResponse(url="/directory")


# --- 4. THE MAIN APPLICATION (Pesapal Directory) ---

@app.get("/directory", response_class=HTMLResponse)
async def employee_directory(request: Request, edit_id: int = None):
    """
    Displays the Employee Directory.
    If 'edit_id' is present (clicked Edit button), it fetches that specific user.
    """
    error_message = None
    employees_data = []
    employee_to_edit = None

    try:
        db.use_database("company_db")
        t = db.get_table("employees")
        
        if t:
            employees_data = t.rows
            
            # If user clicked "Edit", find that specific employee to populate the form
            if edit_id:
                for emp in employees_data:
                    # Handle if row is Dict or List (safety check)
                    c_id = emp['id'] if isinstance(emp, dict) else emp[0]
                    if int(c_id) == int(edit_id):
                        employee_to_edit = emp
                        break
        
    except Exception as e:
        print(f"Error fetching employees: {e}")
        error_message = f"Could not load data: {str(e)}"

    return templates.TemplateResponse("employee_directory.html", {
        "request": request,
        "employees": employees_data,
        "edit_emp": employee_to_edit, 
        "error": error_message
    })

@app.post("/directory/save")
async def save_employee(
    # Hidden ID field (0 = New Hire, >0 = Update Existing)
    emp_id: int = Form(0), 
    name: str = Form(...), 
    role: str = Form(...), 
    salary: int = Form(...),
    contact: str = Form(...),
    address: str = Form(...),
    experience: int = Form(...),
    tenure: int = Form(...)
):
    """
    Handles BOTH Creating and Updating employees.
    """
    try:
        db.use_database("company_db")
        t = db.get_table("employees")
        
        if emp_id > 0:
            # --- UPDATE (Promote, Demote, Edit Info) ---
            updates = {
                "name": name,
                "role": role,
                "salary": salary,
                "contact": contact,
                "address": address,
                "experience": experience,
                "tenure": tenure
            }
            print(f"Updating Employee {emp_id}...")
            t.update(emp_id, updates)
            
        else:
            # --- CREATE NEW HIRE ---
            # Generate ID manually (MAX ID + 1)
            new_id = 1
            if t.rows:
                current_ids = [int(r['id'] if isinstance(r, dict) else r[0]) for r in t.rows]
                if current_ids:
                    new_id = max(current_ids) + 1
            
            print(f"Creating Employee {new_id}...")
            t.insert([new_id, name, role, salary, contact, address, experience, tenure])
            
    except Exception as e:
        print(f"Failed to save employee: {e}")
        
    return RedirectResponse(url="/directory", status_code=303)

@app.post("/directory/delete/{employee_id}")
async def delete_employee(employee_id: int):
    """
    Deletes an employee (Fire).
    """
    try:
        db.use_database("company_db")
        t = db.get_table("employees")
        t.delete(employee_id)
    except Exception as e:
        print(f"Failed to delete: {e}")
    return RedirectResponse(url="/directory", status_code=303)


# --- 5. STRICT API ROUTES (Legacy / Microservice Demo) ---
# Kept to satisfy "Strict Microservice API" requirement if needed

class UserSchema(BaseModel):
    id: int
    name: str
    email: str

def get_api_table():
    db.use_database("api_service_db")
    return db.get_table("api_users")

@app.get("/api/users", response_model=List[dict], tags=["Strict API"])
def get_all_users_json():
    t = get_api_table()
    return t.rows if t else []

@app.post("/api/users", tags=["Strict API"])
def create_user_json(user: UserSchema):
    t = get_api_table()
    try:
        if t.select_where("email", user.email):
            raise HTTPException(status_code=400, detail="Email already exists.")
        t.insert([user.id, user.name, user.email])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success", "user": user}

@app.get("/api/users/{email}", tags=["Strict API"])
def get_user_by_email(email: str):
    t = get_api_table()
    results = t.select_where("email", email)
    if not results:
        raise HTTPException(status_code=404, detail="User not found")
    return results[0]

if __name__ == "__main__":
    print("-------------------------------------------------------")
    print("   EdSQL Final Server Running")
    print("   👉 App: http://127.0.0.1:8000/directory")
    print("   👉 API: http://127.0.0.1:8000/docs")
    print("-------------------------------------------------------")
    uvicorn.run(app, host="127.0.0.1", port=8000)
