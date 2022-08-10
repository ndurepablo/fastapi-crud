from fastapi import APIRouter, Response
from config.db import conn
from models.user import users 
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

# return all users in db
@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall()
# filter user by id
@user.get("/users/{id}", response_model=User, tags=["users"]) 
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()
# create new user
@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name, 
                "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode('utf-8')) # encrypt password
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
# delete user by id
@user.delete("/users/{id}", status_code=HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)
# update user
@user.put("/users/{id}", response_model=User, tags=["users"])
def edit_user(id: str, user: User):
    conn.execute(users.update().values(name = user.name, 
                              email = user.email, 
                              password = user.password
                              ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

