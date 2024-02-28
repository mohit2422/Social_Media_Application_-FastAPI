from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote

#It will create engine i.e create all our models. It will create the table name "posts" in postgres
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
        
 # it will grab router object from post & user file and imports all this specific routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#                                                 # @ is decorator that reference fastapi instance name app
# @app.get("/")                                   #app is instnace, get is http method and / is path (root url in this case)
# def root():                                     #root is function
#     return {"message": "Welcome to my API !!!"}




