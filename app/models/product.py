import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from ..database import Base
from sqlalchemy.orm import relationship 

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    lot_number = Column(String, nullable = False)
    quantity = Column(Integer, nullable = False, default = 0)
    temperature = Column(Float, nullable = False)
    creation_date = Column(DateTime, default = datetime.datetime.utcnow())
