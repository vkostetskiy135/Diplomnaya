from fastapi import Form
from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    age: int

    @classmethod
    def as_form(
            cls,
            username: str = Form(...),
            password: str = Form(...),
            first_name: str = Form(...),
            last_name: str = Form(...),
            age: int = Form(...)
    ):
        return cls(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age
        )


class UserProfile(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: int
    slug: str
    id: int



class UpdateUserInfo(BaseModel):
    first_name: str
    last_name: str
    age: int


class UpdateUserAuth(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: int
    slug: str
    id: int

    model_config = {
        "from_attributes": True
    }
