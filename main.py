# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from scheduler import schedule_task, remove_task, get_db
from model import Task

app = FastAPI()

class ScheduleRequest(BaseModel):
    spider_name: str
    cron_expression: str

@app.post("/schedule")
def add_schedule_task(request: ScheduleRequest, db: Session = Depends(get_db)):
    try:
        schedule_task(db, request.spider_name, request.cron_expression)
        return {"message": "Task scheduled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/schedule/{spider_name}")
def delete_schedule_task(spider_name: str, db: Session = Depends(get_db)):
    try:
        remove_task(db, spider_name)
        return {"message": "Task removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
