from sqlalchemy.orm import Session
from .. import models,schemas, database
from fastapi import HTTPException, status, Depends
from ..oauth2 import get_current_user 


def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs
    

# def create(request:schemas.Blog, db: Session):
#     new_blog = models.Blog(title=request.title,body=request.body,user_id =2)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # current_user là đối tượng User, có thuộc tính id
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)  # Sử dụng user_id của người dùng hiện tại
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int, request:schemas.Blog,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not found')
    blog.update(request.model_dump())
    db.commit()
    return 'updated'

def show(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not available')
    return blog