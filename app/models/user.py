import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, false
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow())
    is_active = Column(Boolean, nullable=False, default=True)
    is_confirmed = Column(Boolean, nullable=False, default=False)
