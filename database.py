from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from models import Blog, Base
from sqlalchemy.orm import Session
from sqlalchemy import desc



DATABASE_URL = "postgresql://postgres:123456789@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)



def get_latest_blog_posts(db: Session, limit: int = 10):
    return db.query(Blog).order_by(desc(Blog.id)).limit(limit).all()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

