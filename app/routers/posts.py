from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db 
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)



@router.get("/", response_model=List[schemas.PostVotes])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    # For more private applications i.e Notetaking app
    # posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #For social media style applications
    # posts = db.query(models.Post).all()
    
    #To see votes functionality for social media functionality
    posts= db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()

    new_post = models.Post(owner_id= get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostVotes)
def get_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)): 
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s  """, (str(id),))
    # post = cursor.fetchone()
    
    ## For social media stye applications where anyone can request any one entry
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    ##For social media with votes functionality
    post= db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = 404
        #return {'message' : f"post with id: {id} was not found"}
    return post

    ## For more private applications where only that user can retrieve his entry
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    #if not post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    #if post.owner_id != get_current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    #return post
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %sRETURNING *""", (post.title, post.content, post.published, str(id), ))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()