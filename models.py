from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    email= Column(String(50), unique=True)
    password = Column(Integer)