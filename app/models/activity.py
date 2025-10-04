from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base


class Activity(Base):
    """Деятельность"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, nullable=False)  # 1, 2 или 3

    parent = relationship(
        "Activity", remote_side=[id], back_populates="children"
    )
    children = relationship("Activity", back_populates="parent")

    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities"
    )
