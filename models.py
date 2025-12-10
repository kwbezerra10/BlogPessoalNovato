from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime
class Article(Base):
    __tablename__ = "articles"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(100), index=True)
    content    = Column(String(1000))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=None)


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String(100), index=True)
    password   = Column(String(10))
    
