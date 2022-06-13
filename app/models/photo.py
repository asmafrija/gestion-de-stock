import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from ..database import Base

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, nullable=False)
    photo_url = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow())
    dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=True)
    dog = relationship("Dog", foreign_keys=[dog_id])
    