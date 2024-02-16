from routers import auth, blog_post
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

print("Hello")
app = FastAPI()

# Mount the "static" directory to serve static files (CSS in this case)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(blog_post.router)