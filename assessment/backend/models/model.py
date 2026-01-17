from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    decription = Column(String)
    due_date = Column(Date)
    priority = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
