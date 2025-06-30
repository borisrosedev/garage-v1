import os
import shutil
from uuid import uuid4
from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from ..database import SessionDep
from ..core.security import oauth2_scheme
from ..services.auth_service import get_current_user
from ..database.models import User, UserOut
from pydantic import EmailStr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "../../uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/", response_model=list[User])
async def read_users(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    return session.exec(select(User)).all()

@router.post("/create", response_model=UserOut)
async def create_user(
    session: SessionDep,
    firstname: str = Form(...),
    lastname: str = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    photo: UploadFile = File(...),
):

    existing_user = session.exec(
        select(User).where((User.username == username) | (User.email == email))
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists.")


    _, ext = os.path.splitext(photo.filename)
    safe_filename = f"{uuid4().hex}{ext}"
    photo_path = os.path.join(UPLOAD_DIR, safe_filename)
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)


    user = User(
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        photo_name=safe_filename,
        role=role,
    )
    user.password = password 
    session.add(user)
    session.commit()
    session.refresh(user)

    return user 