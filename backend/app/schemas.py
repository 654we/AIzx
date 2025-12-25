from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserProfile(BaseModel):
    id: int
    username: str
    location: str = ""
    subscriptions: list[str] = []


class UpdateLocation(BaseModel):
    location: str = Field(..., min_length=1, max_length=128)


class UpdateSubscriptions(BaseModel):
    tags: list[str] = []
