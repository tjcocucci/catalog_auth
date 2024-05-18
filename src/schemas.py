from typing import Any

from peewee import ModelSelect

from pydantic import BaseModel, validator
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return username

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8 or len(password) > 20:
            raise ValueError("Password must be between 8 and 20 characters")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        if not any(char in "@#$^&*+=!." for char in password):
            raise ValueError(
                "Password must contain at least one special character (@#$^&*+=)"
            )
        return password


class UserResponseModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
