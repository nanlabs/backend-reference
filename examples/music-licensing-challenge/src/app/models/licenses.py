from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class LicenseStatus(Base):
    __tablename__ = "license_statuses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    songs = relationship("Song", back_populates="license_status")
