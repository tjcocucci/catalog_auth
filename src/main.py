from fastapi import FastAPI, HTTPException
from database import db as connection, User
from schemas import UserRequestModel, UserResponseModel


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
