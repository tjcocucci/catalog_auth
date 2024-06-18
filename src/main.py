from typing import Annotated, Union

from fastapi import FastAPI, HTTPException, Header
from database import db as connection, User
from schemas import UserRequestModel, UserResponseModel
from datetime import datetime, timedelta
import settings
from jose import jwt

app = FastAPI(
    title="auth", description="User authentication and authorization", version="0.1.0"
)


@app.on_event("startup")
def startup():
    if connection.is_closed():
        connection.connect()
        print("Connection opened")
    connection.create_tables([User])


@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()
        print("Connection closed")


@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")

    hashed_password = User.create_password(user.password)
    user = User.create(username=user.username, password=hashed_password)

    return user


@app.get("/users", response_model=list[UserResponseModel])
async def get_users():
    return User.select()


@app.get("/users/{user_id}", response_model=UserResponseModel)
async def get_user(user_id: int):
    user = User.select().where(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = User.select().where(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_instance()
    return {"message": "User deleted"}


@app.post("/login")
async def login(user: UserRequestModel):
    userFromDB = User.select().where(User.username == user.username).first()
    if not userFromDB:
        raise HTTPException(status_code=404, detail="User not found")
    if not userFromDB.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(userFromDB.username)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


def create_access_token(username: str) -> str:
    """
    Function to generate JWT token with username and expiration time
    """
    payload = {
        "sub": username,
        "exp": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


@app.get("/session")
async def session(Authorization: Annotated[Union[str, None], Header()] = None):
    """
    Check if the token is valid. Will not work in swagger UI due to browser security
    """ 
    try:
        print(Authorization)
        payload = jwt.decode(Authorization, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
