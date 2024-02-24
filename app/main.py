from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# from typing import Optional, List
#from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
# from models import Post
from .database import engine
from .routers import post,user,auth

#It will create engine i.e create all our models. It will create the table name "posts" in postgres
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connecting to Postgres Database with Fastapi
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Mohit#2206', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful !!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ",error)
        time.sleep(2)

my_post = [{"title": "title of post 1","content":"content of post 1","id":1}, {"title":"favorite foods","content":"I like Pizza","id":2}]

# function call for returning values of id match 
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
# function call for returning index of id match
def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i
        
 # it will grab router object from post & user file and imports all this specific routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#                                                 # @ is decorator that reference fastapi instance name app
# @app.get("/")                                   #app is instnace, get is http method and / is path (root url in this case)
# def root():                                     #root is function
#     return {"message": "Welcome to my API !!!"}




