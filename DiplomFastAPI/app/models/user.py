from DiplomFastAPI.app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    slug = Column(String, index=True, unique=True)



