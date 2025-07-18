from sqlalchemy import Column, Integer, String
from db import Base
from geoalchemy2 import Geometry
class Item(Base):
    __tablename__ = "roads1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4326))


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)