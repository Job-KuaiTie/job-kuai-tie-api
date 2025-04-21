from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from datetime import datetime, timezone
from app.db import SessionDep
from app.model import Account, AccountCreate, AccountPublic, AccountUpdate
from app.core import hash_password

router = APIRouter()


@router.post("/accounts/", response_model=AccountPublic)
def create_account(account: AccountCreate, session: SessionDep):
    db_account = Account(
        name=account.name,
        email=account.email,
        password_hash=hash_password(account.password),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@router.get("/accounts/", response_model=list[AccountPublic])
def read_accounts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Account]:
    accounts = session.exec(select(Account).offset(offset).limit(limit)).all()
    return accounts


@router.get("/accounts/{account_id}", response_model=AccountPublic)
def read_account(account_id: str, session: SessionDep) -> Account:
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.patch("/accounts/{account_id}", response_model=AccountPublic)
def update_account(account_id: str, account: AccountUpdate, session: SessionDep):
    account_db = session.get(Account, account_id)
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account_data = account.model_dump(exclude_unset=True)

    # PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated.
    # Instead, you should access this attribute from the model class.
    # Deprecated in Pydantic V2.11 to be removed in V3.0.
    # account_db.sqlmodel_update(account_data)

    for key, value in account_data.items():
        # SHould not change email at this stage
        if key != "email":
            setattr(account_db, key, value)

    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return account_db


@router.delete("/accounts/{account_id}")
def delete_account(account_id: str, session: SessionDep):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# app = FastAPI()


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# class CommonHeaders(BaseModel):
#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tag: list[str] = []


# @router.get("/header_demo/")
# async def header_demo(headers: Annotated[CommonHeaders, Header()]):
#     return headers


# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


# @router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# @router.get("/items_with_return/")
# async def read_items_with_return() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0),
#         Item(name="Plumbus", price=32.0),
#     ]


# @router.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}


# @router.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}


# @router.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# # @router.get("/items/")
# # async def read_item(skip: int = 0, limit: int = 10):
# #     return fake_items_db[skip : skip + limit]


# @router.get("/items/")
# async def read_items(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @router.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
