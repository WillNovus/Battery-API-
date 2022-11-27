from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix ="/posts",
    tags = ["Posts"]
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int=0, search: Optional[str]=""):
    #cur.execute("SELECT * FROM posts")
    #posts = cur.fetchall()
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    print(results)

    return results

@router.get("/{id}", response_model =schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cur.fetchone()
    #post_query = db.query(models.Post).filter(models.Post.id == id)
    #post = post_query.first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    return post

# The path operation below allows for posting payload w/o parsing as seen from the variable type and Body param.
# From fastapi.params import Body.
'''@router.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"New Post":f"title : {payload['title']} content: {payload['contents']}"}'''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                #(post.title, post.content, post.published))
    #new_post = cur.fetchone()
    #conn.commit()
    #print(new_post)
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""DELETE FROM posts WHERE id = %s RETURNING* """, (str(id), ))
    #deleted_post = cur.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cur.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
  