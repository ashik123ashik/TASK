from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    email: str
    password: str


class TaskCreate(BaseModel):
    title: str
    decription: str
    due_date: date
    priority: int
