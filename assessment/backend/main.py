from fastapi import FastAPI
from routes.route import router
from database.db import Base, engine
import os

app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)


