# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scheduler import schedule_task, remove_task
import uvicorn


app = FastAPI()

class ScheduleRequest(BaseModel):
    spider_name: str
    cron_expression: str

@app.post("/schedule")
def add_schedule_task(request: ScheduleRequest):
    try:
        schedule_task(request.spider_name, request.cron_expression)
        return {"message": "Task scheduled successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/schedule/{spider_name}")
def delete_schedule_task(spider_name: str):
    try:
        remove_task(spider_name)
        return {"message": "Task removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=18000)