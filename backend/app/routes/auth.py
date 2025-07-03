from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from ..services.auth_service import authenticate_user, create_access_token
from ..models import Token
from ..database import SessionDep

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep, 
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"username": user.username},
        expires_delta=timedelta(minutes=15),
    )
    return Token(access_token=access_token, token_type="bearer")
