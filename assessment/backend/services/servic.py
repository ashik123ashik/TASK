from sqlalchemy.orm import Session
from passlib.hash import argon2 
from models.model import   users , Task , TaskAttachment
from groq import Groq
from database.db import UPLOAD_DIR
from fastapi import FastAPI, UploadFile, File , HTTPException
import mimetypes

app = FastAPI()
import os
from fastapi.responses import FileResponse
from datetime import date
from models.auth import  login_user

def  signup_service (db : Session ,x:str, a:str , b : str):
    bb = argon2.hash(b)
    user = users(name = x ,email = a , password = bb)
    db.add(user)
    db.commit()
    db.refresh(user)
    login_user(db , a , b)

def task_input_service(a:str , b:str ,c:date , d:int , db : Session):
    up = Task( title = a,
    description = b,
    due_date = c,
    priority  = d)
    db.add(up)
    db.commit()
    db.refresh(up)
    return {"message" : "uploaded successfull from backend"}

def getalltask_service(db : Session):
    temp = db.query(Task).all()
    return temp

def gettaskdate_service(db: Session):
    temp = db.query(Task).order_by(Task.due_date.asc()).all()
    return temp

def gettaskpriority_service(db: Session):
    temp = db.query(Task).order_by(Task.priority.desc()).all()
    return temp

def edit_task_service(db: Session, task_id: int, data):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = data.title
    task.description = data.decription
    task.due_date = data.due_date
    task.priority = data.priority

    db.commit()
    db.refresh(task)

    return task

def download_file(file_name:str):
    file_path = os.path.join(UPLOAD_DIR,file_name)
    if not file_path:
        return{"msg":"not found"}
    mime_type,_= mimetypes.guess_type(file_path)
    return FileResponse (path = file_path , filename = file_name , media_type = mime_type)

def delete_task_service(db:Session , x :int):
    task = db.query(Task).filter(Task.id == x).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


UPLOAD_DIR = "uploads"
def attach_file_service(db: Session, task_id: int, file: UploadFile):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    attach = TaskAttachment(task_id=task_id,filename=file.filename)

    db.add(attach)
    db.commit()

    return {"message": "File attached successfully"}









# def get_all_user(db:Session):
#     d=db.query(users).all()
#     return d

# def learning_material_creator(title : str):
#     rules=f"""hey , you have to create a learning material for the students with the given title ,  generate 100 words with necessary important things and the title is {title}"""
#     response1 = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "system", "content":rules},],temperature=0)
#     result =( response1.choices[0].message.content )
#     return result

# def moduleinput(db : Session , title : str):
#     aidata = learning_material_creator(title)
#     x = modules(quiz = title , learning_material = aidata)
#     db.add(x)
#     db.commit()
#     db.refresh(x)
#     return "your module title is added and the learning material will be added by grok ai , enjoy"

# def getmodule(db :Session):
#     result = db.query(modules).all()
#     return result

# def userinput_service (db:Session , name : str , password : str , email : str , role : str):
#     uploader = users(name = name , password = argon2.hash(password) , email = email , role = role)
#     db.add(uploader)
#     db.commit()
#     db.refresh(uploader)
#     return ("user details uploaded successfully")

# def course_enroll(db : Session , cou : str , id : int , modid : int):
#     uploader = courses(student_id = id , course_name = cou , module_id = modid )
#     role = db.query(users.role).filter(users.id == id).scalar()
#     if role == "admin":
#         return {"message" : " person is admin da, so course enroll panna mudiyaathu    , so to check students details /only_students"}
#     elif role == "student":
#         db.add(uploader)
#         db.commit()
#         db.refresh(uploader)
#         setof = db.query(courses).all()
#         return setof
    
# def only_students(db:Session):
#     al = db.query(users).filter(users.role == "student").all()
#     return al
    

# def view_course_enroll(db : Session , name : str):
#     byid = db.query(users.id).filter(users.name == name).scalar()
#     selective = db.query(courses).filter(courses.id == byid).all()
#     return selective

# def check_all_enrolled_course(db : Session):
#     selective = db.query(courses).all()
#     return selective
    
# def groq_service(db :Session , promp : str):
#     response1 = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "system", "content":promp},],temperature=0)
#     result =( response1.choices[0].message.content )
#     uploader = chatsaverclass( question = promp , response = result)
#     db.add(uploader)
#     db.commit()
#     db.refresh(uploader)
#     return result

# TO CHECK THE LOCATION
# from database.db import base, engine
# def check():
#     return ("USING DATABASE:", engine.url)

# def getall_students(db: Session):
#     students = db.query(Student).all()
#     return students

# def Create_student(db: Session, name: str, email: str, password: str, age: int, role: str):
#     hashed_password = argon2.hash(password)

#     new_student = Student(
#         name=name,
#         email=email,
#         password=hashed_password,
#         age=age,
#         role=role
#     )

    # db.add(new_student)
    # db.commit()
    # db.refresh(new_student)
#     return "done"


# def login(db: Session, name1: str, password: str):
#     student = db.query(Student).filter(Student.name == name1).first()
#     student-name = db.query(Student.role).filter(Student.name == name1).first()------to extract  only role
#     if not student:
#         return "user not found"

#     if argon2.verify(password, student.password):
#         return afterlogin(db, name1)
#     else:
#         return "please enter valid data"





    

# def login_service(db : Session , name_given : str , password : str):----------------------my old simple login version
#         truename = db.query(users).filter(users.name == name_given).first()
#         ids = db.query(users.id).filter(users.name == name_given)
#         if not truename:
#             return "user not found"
        

#         if argon2.verify(password, truename.password):
#             return afterlogin(db, name_given ,ids)
#         else:
#             return "please enter valid data"
        
# def afterlogin(db : Session , name:str , id : int):--------------------------------------temorary off
#      truerole = db.query(users.role).filter(users.id == id).scalar()
#      if (truerole == "admin"):
#           return {"message":"ok you are admin , so you can access /enter_the_module  /enter_user_details   /get_module   /course_enroll    /check_all_enrolled_course"}
#      elif (truerole == "student"):
#         return {"message":"ok you are student , so you can access /get_module  /check_course_enroll <--with your name"}