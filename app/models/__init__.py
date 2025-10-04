from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.organization import Organization, OrganizationPhone  # noqa
from app.models.building import Building  # noqa
from app.models.activity import Activity  # noqa
from app.models.associations import organization_activities  # noqa
