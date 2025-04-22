from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm  # OAuth2PasswordBearer
from app.db import SessionDep

from app.security import authenticate_account, get_current_account, create_access_token
from app.model import Token, Account

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/accounts/me/", response_model=Account)
async def read_accounts_me(
    current_account: Annotated[Account, Depends(get_current_account)],
    session: SessionDep,
):
    return current_account


@router.get("/accounts/me/items/")
async def read_own_items(
    current_account: Annotated[Account, Depends(get_current_account)],
    session: SessionDep,
):
    return [{"item_id": "Foo", "owner": current_account.account_id}]
