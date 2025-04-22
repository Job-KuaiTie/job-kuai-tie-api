from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.model import Account
import pytest
from faker import Faker


from tests.factory import (
    AccountCreateFactory,
    CompanyFactory,
    JobFactory,
    CategoryFactory,
)
from app.security import hash_password


fake = Faker()


@pytest.fixture(name="session")
def session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# @pytest.fixture(scope="function")
# def default_account(session: Session):
#     account = AccountFactory()

#     session.add(account)
#     session.commit()
#     session.refresh(account)

#     yield account

# @pytest.fixture(scope="function")
# def default_created_account(session: Session):
#     account = AccountCreateFactory()

#     db_account = Account(
#         name=account.name,
#         email=account.email,
#         password_hash=hash_password(account.password),
#     )

#     session.add(db_account)
#     session.commit()

#     yield account


@pytest.fixture(scope="function")
def default_password():
    yield fake.password(length=12)


@pytest.fixture(scope="function")
def default_account(session: Session, default_password):
    account = AccountCreateFactory(password=default_password)

    db_account = Account(
        name=account.name,
        email=account.email,
        password_hash=hash_password(account.password),
    )

    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    yield db_account


@pytest.fixture(scope="function")
def default_token(client, default_password, default_account):
    # Get the token by client
    response = client.post(
        "/token/",
        data={"username": default_account.email, "password": default_password},
    )
    # Return the token
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def default_company(session: Session, default_account: Account):
    company = CompanyFactory(owner=default_account)

    session.add(company)
    session.commit()
    session.refresh(company)
    yield company


@pytest.fixture(scope="function")
def default_job(session: Session, default_account: Account):
    job = JobFactory(owner=default_account)

    session.add(job)
    session.commit()
    session.refresh(job)

    yield job


@pytest.fixture(scope="function")
def default_category(session: Session, default_account: Account):
    category = CategoryFactory(owner=default_account)

    session.add(category)
    session.commit()
    session.refresh(category)

    yield category
