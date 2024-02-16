import json
from typing import Optional
from fastapi import  Form, HTTPException, Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, get_latest_blog_posts

router = APIRouter()



templates = Jinja2Templates(directory="templates")

try:
    with open("registered_users.json", "r") as file:
        content = file.read()
        if content:
            registered_users = json.loads(content)
        else:
            registered_users = []
except FileNotFoundError:
    registered_users = []
except json.JSONDecodeError:
    registered_users = []

logged_in_users = []

def get_user(username: str) -> Optional[dict]:
    for user_data in registered_users:
        if isinstance(user_data, dict) and user_data.get("username") == username:
            return user_data
    return None

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    db = SessionLocal()
    
    # Retrieve the latest blog posts
    latest_blog_posts = get_latest_blog_posts(db)
    
    db.close()
    
    return templates.TemplateResponse("index.html", {"request": request, "latest_blog_posts": latest_blog_posts})


@router.post('/register', response_class=HTMLResponse)
def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        # Simulate user registration and append the username to the list
        user_data = {"username": username, "password": password}
        registered_users.append(user_data)

        # Serialize the registered_users list to JSON and save it to a file
        with open("registered_users.json", "w") as file:
            json.dump(registered_users, file)

        return templates.TemplateResponse("thankyou.html", {"request": request, "username": username})
    except:
        return "Error"

@router.get("/registered-users", response_class=JSONResponse)
async def get_registered_users():
    return {"registered_users": registered_users}




file_path = 'registered_users.json'

@router.get('/login', response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@router.post('/login', response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    result_password = next(
        (item.get("password", item.get("passsword")) for item in json_data if "username" in item and item["username"] == username), None)

    if result_password and result_password == password:
        logged_in_users.append(username)
        return templates.TemplateResponse("login_success.html", {"request": request, "username": username})
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/logged_in_users", response_class=JSONResponse)
async def get_logged_in_users():
    return {"logged_in_users": logged_in_users}