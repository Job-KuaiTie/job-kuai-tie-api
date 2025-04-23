from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm  # OAuth2PasswordBearer

from app.db import SessionDep
from app.security import authenticate_account, create_access_token
from app.model import Token
from app.config import settings

router = APIRouter(tags=["security"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    account = authenticate_account(
        email=form_data.username, password=form_data.password, session=session
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": account.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
