from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import engine
from models.model import Base, User, Task
from models.schema import UserCreate, TaskCreate
from models.auth import get_db, create_token, get_current_user

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    check = db.query(User).filter(User.email == user.email).first()
    if check:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    return {"message": "Signup successful"}


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email,
        User.password == user.password
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(db_user.email)
    return {"access_token": token}


@router.post("/create_table")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        decription=task.decription,
        due_date=task.due_date,
        priority=task.priority,
        user_id=user.id
    )
    db.add(new_task)
    db.commit()
    return {"message": "Task created"}


@router.get("/getalltask")
def get_tasks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    return tasks
