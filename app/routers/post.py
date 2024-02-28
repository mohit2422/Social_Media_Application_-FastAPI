from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

# Router object is used to splits different path operations into different files
router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

###################################### GET ALL THE POSTS ##################################################

# 1. With regular sql queries 
# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data": posts}

# 2. With sqlalchemy without using sql queries 
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):   #every time we need to pass parameter to work with the database
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # this is used for sending queries to db without using actual SQL Queries command
    return posts

########################################## GET SINGLE POSTS #############################################

# 1. With regular sql queries 
# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
#     # post = find_post(id)  # calling find_post id
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     print(post)
#     return {"post details": post}

# 2. With sqlalchemy without using sql queries 
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        return post

###################################### CREATING A POST ##################################################

# 1. With regular sql queries
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: schemas.Post):
#     print(post.title)
#     # Staging the data to the database
#     cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()  # It will saved inserted data to the Postgres database
#     return {"data": new_post}

# 2. With sqlalchemy without using sql queries
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())   #instead of post.dict we are using post.model_dump
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
               
        
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,1000000)
    #my_post.append(post_dict)
    # print(post.published)
    #print(post.dict())             #convert pydantic model to dictionary
    #return {"data": post_dict}
    
################################# DELETETING A POST ############################################

# 1. With regular sql queries
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # finding the index of the array that has required ID
#     #my_post.pop(index)
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     # index = find_index_post(id)
#     # if index == None:
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     # my_post.pop(index)
#     return {'message': 'post was successfully deleted'}

# 2. With sqlalchemy without using sql queries
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {'message': 'post was successfully deleted'}

################################# UPDATING A POST ############################################
# 1. With regular sql queries
# @app.put("/posts/{id}")
# def update_post(id: int, post: schemas.Post):
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title,post.content,post.published, str(id)))

#     updated_post = cursor.fetchone()
#     conn.commit()
#     # index = find_index_post(id)

#     # if index == None:
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_post[index] = post_dict
#     # return {"data": post_dict}
#     return {"data": updated_post}

# 2. With sqlalchemy without using sql queries
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # post_query.update({'title': 'hey this is my updated title', 'content':'this is my updated content'}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()