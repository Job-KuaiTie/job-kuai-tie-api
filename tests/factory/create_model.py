from tests.factory import AccountFactory, JobFactory, CompanyFactory, CategoryFactory
from app.model import Account
from sqlmodel import Session


def create_account(session: Session):
    account = AccountFactory()

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


def create_job(account: Account, session: Session):
    job = JobFactory(owner=account)

    session.add(job)
    session.commit()
    session.refresh(job)

    return job


def create_company(account: Account, session: Session):
    company = CompanyFactory(owner=account)

    session.add(company)
    session.commit()
    session.refresh(company)

    return company


def create_category(account: Account, session: Session):
    category = CategoryFactory(owner=account)

    session.add(category)
    session.commit()
    session.refresh(category)

    return category
