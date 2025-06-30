
from typing import Optional, Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
import jwt
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserOut(SQLModel):
    id: int
    username: str
    email: EmailStr
    role: str
    photo_name: str

    class Config:
        from_attributes = True




class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str
    username: str
    email: str 
    password_hash: str 
    photo_name: str
    role: Optional[str] = Field(default="user")

    @property
    def password(self):
        raise Exception('password is write-only')
    
    @password.setter 
    def password(self, plain_password):
        self.password_hash = pwd_context.hash(plain_password)

   
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password_hash)

