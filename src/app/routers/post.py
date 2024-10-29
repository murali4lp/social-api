from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

import app.models as models
from app.database import get_db
from app.schema import PostCreate, PostOut, PostResponse
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

def row_to_dict(row):
    return {
        'post': row[0],
        'votes': row[1]
    }

@router.get("/", response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(
    get_current_user
), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Using only psycopg adapter
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = [row_to_dict(row) for row in result]
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(
    get_current_user
)):
    # Using only psycopg adapter
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.model_dump(), owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(
    get_current_user
)):
    # Using only psycopg adapter
    # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} was not found")
    return row_to_dict(post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(
    get_current_user
)):
    # Using only psycopg adapter
    # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int, post_data: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(
    get_current_user
)):
    # Using only psycopg adapter
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id - {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized")
    
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post