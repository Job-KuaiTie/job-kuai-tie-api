from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from app.model import TokenData, Account
from app.security import verify_password
from app.db import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def get_account(account_id: str, session: SessionDep) -> Account | None:
    return session.get(Account, account_id)


def get_account_by_email(email: str, session: SessionDep) -> Account | None:
    statement = select(Account).where(Account.email == email)
    # Account expected to be only one or not existed
    return session.exec(statement).one_or_none()


def authenticate_account(email: str, password: str, session: SessionDep):
    account = get_account_by_email(email, session)
    if not account:
        return False
    if not verify_password(password, account.password_hash):
        return False
    return account


async def get_current_account(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("sub")
        if account_id is None:
            raise credentials_exception
        token_data = TokenData(account_id=account_id)
    except InvalidTokenError:
        raise credentials_exception
    account = get_account(account_id=token_data.account_id, session=session)
    if account is None:
        raise credentials_exception
    return account


CurrentAccountDep = Annotated[Account, Depends(get_current_account)]
