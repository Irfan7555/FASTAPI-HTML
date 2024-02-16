from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from database import SessionLocal, get_db
from routers.auth import logged_in_users
from fastapi.responses import HTMLResponse, JSONResponse
from models import Blog
from sqlalchemy.orm import Session


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/post_blog', response_class=HTMLResponse)
def post_blog(request: Request, username: str = Form(...), blog_title: str = Form(...), blog_content: str = Form(...), image_url: str = Form(...)):
    # Check if the user is logged in
    if username not in logged_in_users:
        raise HTTPException(status_code=401, detail="Not authenticated")


    db = SessionLocal()
    new_blog = Blog(title=blog_title, content=blog_content, author=username, image_url=image_url)
    db.add(new_blog)
    db.commit()
    db.close()

    return templates.TemplateResponse("post_success.html", {"request": request, "blog_title": blog_title, "blog_content": blog_content, "author": username, "image_url": image_url})


@router.delete('/delete_blog/{blog_id}', response_class=HTMLResponse)
def delete_blog(blog_id: int):
    db = SessionLocal()
    blog = db.query(Blog).get(blog_id) 
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog); db.commit(); db.close()
    return HTMLResponse(content=f"<script>alert('Blog post {blog.title} deleted!'); window.location.href='/';</script>", status_code=200, media_type="text/html")



@router.get('/get/{blog_id}', response_class=JSONResponse)
def get_blog( blog_id: int):
    db = SessionLocal()

    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if blog is None:
        db.close()
        raise HTTPException(status_code=404, detail="Blog not found")

    db.close()
    return JSONResponse(content={"blog_id": blog.id, "title": blog.title, "content": blog.content, "image_url": blog.image_url})


@router.put('/update_blog/{blog_id}')
def update_blog(blog_id: int, blog_title: str = Form(...), blog_content: str = Form(...), image_url: str = Form(...)):
    db = SessionLocal()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        db.close()
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.title, blog.content, blog.image_url = blog_title, blog_content, image_url
    db.commit()
    db.close()
    return {"message": f"Blog post with ID {blog_id} updated successfully"}




@router.get("/blogs_by_author")
def get_blogs_by_author(author_name: str):
    db = SessionLocal()
    try:
        blogs = db.query(Blog).filter(Blog.author == author_name).all()
        if not blogs:
            raise HTTPException(status_code=404, detail="No blogs found for the author")
        return {"author": author_name, "blogs": blogs}
    finally:
        db.close()



