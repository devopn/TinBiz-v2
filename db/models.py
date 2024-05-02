from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import Boolean
from sqlalchemy import BigInteger
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)
    age = Column(Integer)
    city = Column(String)
    field = Column(String)
    about = Column(String)
    active = Column(Boolean, default=True)

    photo = Column(String)
    filters = Column(JSON, default={})

    moderated = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"{self.name}, {self.age}, {self.city}\n{self.field}\n{self.about}\n{'Анкета активна ✅' if self.active else 'Анкета неактивна ❌'}"
    

class Search(Base):
    __tablename__ = "searches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_id = Column(BigInteger)
    to_id = Column(BigInteger)
    
class Image(Base):
    __tablename__ = "images"

    name = Column(String, primary_key=True)
    id = Column(String)
    
class Admin(Base):
    __tablename__ = "admins"

    id = Column(BigInteger, primary_key=True)