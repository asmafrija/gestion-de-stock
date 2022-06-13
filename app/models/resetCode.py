import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import Base

class ResetCode(Base):
    __tablename__ = "reset_codes"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    reset_code = Column(String, nullable=False)
    status = Column(String(1))
    expired_in = Column(DateTime, default=datetime.datetime.utcnow())
