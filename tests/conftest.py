from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.model import Account
import pytest
from tests.factory import AccountFactory, CompanyFactory, JobFactory, CategoryFactory


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


@pytest.fixture(scope="function")
def default_account(session: Session):
    account = AccountFactory()

    session.add(account)
    session.commit()
    session.refresh(account)

    yield account


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
