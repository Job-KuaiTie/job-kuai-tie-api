import factory
from app.model import (
    Account,
    Company,
    Job,
    Category,
    # JobCategoryLink,
)
from app.security import hash_password
from datetime import datetime, timezone
from nanoid import generate
from faker import Faker

fake = Faker()


class EntityFactory(factory.Factory):
    """Abstract Factory for all entity."""

    class Meta:
        abstract = True  # This prevents instantiation without a model

    id = factory.LazyFunction(lambda: generate(size=13))
    name = factory.LazyFunction(lambda: fake.text(max_nb_chars=20).replace(".", ""))
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class AccountFactory(EntityFactory, factory.Factory):
    """Factory for Account"""

    class Meta:
        model = Account

    email = factory.Faker("email")

    @factory.lazy_attribute
    def password_hash(self):
        password_hash = hash_password(fake.password(length=12))
        return password_hash


class ResourceFactory(EntityFactory, factory.Factory):
    """Abstract Factory to add an optional decription field."""

    class Meta:
        abstract = True  # This prevents instantiation without a model

    description = factory.LazyAttribute(
        lambda o: fake.paragraph(nb_sentences=5) if o.optional else None
    )
    owner = factory.SubFactory(AccountFactory)

    class Params:
        optional = True


class CompanyFactory(ResourceFactory, factory.Factory):
    """Factory for Company"""

    class Meta:
        model = Company

    # Optional
    url = factory.LazyAttribute(lambda o: fake.url() if o.optional else None)
    size = factory.LazyAttribute(
        lambda o: fake.random_int(min=1, max=1000000) if o.optional else None
    )


class JobFactory(ResourceFactory, factory.Factory):
    """Factory for Job"""

    class Meta:
        model = Job

    company = factory.SubFactory(CompanyFactory)
    tier = factory.Faker("random_int", min=1, max=3)

    # Optional
    applied_at = factory.LazyAttribute(
        lambda o: fake.date_time() if o.optional else None
    )
    url = factory.LazyAttribute(lambda o: fake.url() if o.optional else None)
    min_yearly_salary = factory.LazyAttribute(
        lambda o: fake.random_int(min=200000, max=100000000) if o.optional else None
    )
    max_yearly_salary = factory.LazyAttribute(
        lambda o: (o.min_yearly_salary + fake.random_int(min=0, max=1000000))
        if o.optional
        else None
    )


class CategoryFactory(ResourceFactory, factory.Factory):
    """Factory for Category"""

    class Meta:
        model = Category

    color = factory.Faker("hex_color")
