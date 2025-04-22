# from typing import Annotated
from fastapi import APIRouter, HTTPException  # , Query

# from sqlmodel import select
from app.db import SessionDep
from app.model import Account, AccountCreate, AccountPublic, AccountUpdate
from app.security import hash_password, get_account_by_email, CurrentAccountDep

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.post("/", response_model=AccountPublic)
def create_account(account: AccountCreate, session: SessionDep):
    account_email = account.email
    if get_account_by_email(account_email, session) is not None:
        # In the future, it should be no matter email existed or not, send confirmation email.
        # To aovid guessing email by malicious user.
        raise HTTPException(status_code=404, detail="Email is registered.")

    db_account = Account(
        name=account.name,
        email=account_email,
        password_hash=hash_password(account.password),
    )
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


# Login protected


@router.get("/me", response_model=AccountPublic)
def read_my_account(current_account: CurrentAccountDep, session: SessionDep) -> Account:
    return current_account


@router.patch("/me", response_model=AccountPublic)
def update_my_account(
    current_account: CurrentAccountDep, account: AccountUpdate, session: SessionDep
):
    account_db = current_account
    account_data = account.model_dump(exclude_unset=True)

    for key, value in account_data.items():
        # SHould not change email at this stage
        if key != "email":
            setattr(account_db, key, value)

    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return account_db


@router.delete("/me")
def delete_my_account(current_account: CurrentAccountDep, session: SessionDep):
    session.delete(current_account)
    session.commit()
    return {"ok": True}


# @router.get("/", response_model=list[AccountPublic])
# def read_accounts(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[Account]:
#     accounts = session.exec(select(Account).offset(offset).limit(limit)).all()
#     return accounts


# @router.get("/{account_id}", response_model=AccountPublic)
# def read_account(account_id: str, current_account: CurrentAccountDep, session: SessionDep) -> Account:
#     account = session.get(Account, account_id)
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     return account


# @router.patch("/{account_id}", response_model=AccountPublic)
# def update_account(account_id: str, account: AccountUpdate, session: SessionDep):
#     account_db = session.get(Account, account_id)
#     if not account_db:
#         raise HTTPException(status_code=404, detail="Account not found")
#     account_data = account.model_dump(exclude_unset=True)

#     # PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated.
#     # Instead, you should access this attribute from the model class.
#     # Deprecated in Pydantic V2.11 to be removed in V3.0.
#     # account_db.sqlmodel_update(account_data)

#     for key, value in account_data.items():
#         # SHould not change email at this stage
#         if key != "email":
#             setattr(account_db, key, value)

#     session.add(account_db)
#     session.commit()
#     session.refresh(account_db)
#     return account_db


# @router.delete("/{account_id}")
# def delete_account(account_id: str, session: SessionDep):
#     account = session.get(Account, account_id)
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     session.delete(account)
#     session.commit()
#     return {"ok": True}
