from typing import Annotated

from fastapi import APIRouter, FastAPI, Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException # For handling HTTP exceptions like 404 page not found

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import PostCreate, PostUpdate, PostResponse, UserCreate, UserUpdate, UserResponse

router = APIRouter()

# Define a reusable type
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("", response_model=list[PostResponse])
def get_posts(db: db_dependency):
    result = db.execute(select(models.Post).order_by(models.Post.date_posted.desc()))
    posts = result.scalars().all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: db_dependency):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
# Using PostCreate schema here instead of PostResponse because we are creating a new post.
# fastAPI will automatically parses the JSON body and validates it against the PostCreate schema 
# and return a 422 error if the data is invalid
def create_post(post: PostCreate, db: db_dependency):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post_fully(
    post_id: int,
    post_data: PostCreate, 
    db: db_dependency,
    ):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    
    if post_data.user_id != post.user_id:
        result = db.execute(select(models.User).where(models.User.id == post_data.user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    post.title=post_data.title
    post.content=post_data.content
    post.user_id=post_data.user_id
    
    db.commit()
    db.refresh(post)
    return post

@router.patch("/{post_id}", response_model=PostResponse)
def update_post_partially(
    post_id: int,
    post_data: PostUpdate, # for PUT we use PostCreate 
    db: db_dependency,
    ):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    update_data = post_data.model_dump(exclude_unset=True) # update_data is a dictionary

    for field , value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post

@router.delete(
        "/{post_id}", 
        status_code=status.HTTP_204_NO_CONTENT
        )
def delete_post(post_id: int, db:db_dependency):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()