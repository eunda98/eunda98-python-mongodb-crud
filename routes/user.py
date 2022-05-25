
from operator import truediv
from os import access
from shutil import register_unpack_format
from bson import ObjectId
from fastapi import APIRouter, status, Response
from bson import ObjectId
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm 
from fastapi import Depends,HTTPException
from datetime import date, timedelta, datetime
from models.user import User
from config.db import conn, collection_name
from schemas.user import userEntity, usersEntity
from passlib.context import CryptContext


user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
async def find_all_users():
    # print(list(conn.local.user.find()))
    return usersEntity(collection_name.find())

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username,password):
    try:
        bus=collection_name.find_one({"username": username})
        password_check=pwd_context.verify(password,bus["password"])
        return password_check
    
    except User.DoesNotExist:
        return False
SECRET_KEY='uibiyvitrixcjhgb'
ALGORITHM='HS256'

def create_access_token(data:dict,expires_delta:timedelta):
    to_encode=data.copy()
    expire=datetime.utcnow()+expires_delta
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
@user.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username= form_data.username
    password=form_data.password

    if authenticate_user(username,password):
        access_token = create_access_token(data={"sub":username}, expires_delta=timedelta(minutes=30))
        return{"access_token":access_token, "token_type":"bearer"}
    else:
        raise HTTPException(status_code=400,detail="Incorrect username or password")

@user.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"token":token}

@user.post('/users', response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = get_password_hash(new_user["password"])
    del new_user["id"]
    id = collection_name.insert_one(new_user).inserted_id
    user = collection_name.find_one({"_id": id})
    return userEntity(user)


@user.get('/users/{id}', response_model=User, tags=["users"])
async def find_user(id: str,token: str = Depends(oauth2_scheme)):
    return userEntity(collection_name.find_one({"_id": ObjectId(id)}))


@user.put("/users/{id}", response_model=User, tags=["users"])
async def update_user(id: str, user: User,token: str = Depends(oauth2_scheme)):
    collection_name.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(user)
    })
    
    return userEntity(collection_name.find_one({"_id": ObjectId(id)}))


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str,token: str = Depends(oauth2_scheme)):
    collection_name.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=HTTP_204_NO_CONTENT)



