import datetime
from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

class ConfirmationCode(Base):
    __tablename__ = "confirmation_codes"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    confirmation_code = Column(String, nullable=False)
    status = Column(String(1))
    created_on = Column(DateTime, default=datetime.datetime.utcnow())