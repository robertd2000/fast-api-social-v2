from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    body: str
    id: int

    class Config:
        orm_mode = True


class UserShow(User):
    posts: list[Post]

    class Config:
        orm_mode = True
