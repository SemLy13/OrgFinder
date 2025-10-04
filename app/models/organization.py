from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship
from app.models import Base


class OrganizationPhone(Base):
    """Телефон организации"""
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(50), nullable=False)
    organization_id = Column(
        Integer, ForeignKey("organizations.id"), nullable=False
    )


class Organization(Base):
    """Организация"""
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Связь с зданием (many-to-one)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    # Связь с деятельностями (many-to-many)
    activities = relationship(
        "Activity",
        secondary="organization_activities",
        back_populates="organizations"
    )

    # Связь с телефонами (one-to-many)
    phones = relationship("OrganizationPhone")
