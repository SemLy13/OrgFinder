from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models import Base

# Промежуточная таблица для связи Organization - Activity (many-to-many)
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True
    ),
    Column(
        "activity_id",
        Integer,
        ForeignKey("activities.id"),
        primary_key=True
    )
)
