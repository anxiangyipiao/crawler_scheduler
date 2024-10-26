# api.py

from fastapi import APIRouter, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from tasks import sample_task
from model.model import ScheduledTaskModel
from typing import List



ScheduleRouter = APIRouter()
scheduler = BackgroundScheduler()

# 启动调度器
scheduler.start()

@ScheduleRouter.post("/add_task", response_model=ScheduledTaskModel)
def add_task(task: ScheduledTaskModel):
    """
    添加一个定时任务，按指定的间隔（秒）执行 sample_task。
    """
    job = scheduler.add_job(
        sample_task,
        IntervalTrigger(seconds=task.interval),
        id=task.id,  # 任务 ID
        name=task.name  # 任务名称
    )
    task.next_run_time = job.next_run_time  # 更新下次运行时间
    task.status = "running"  # 更新任务状态
    return task

@ScheduleRouter.get("/list_tasks", response_model=List[ScheduledTaskModel])
def list_tasks():
    """
    列出所有定时任务。
    """
    jobs = scheduler.get_jobs()
    tasks = []
    for job in jobs:
        task = ScheduledTaskModel(
            id=job.id,
            name=job.name,
            interval=job.trigger.interval,
            next_run_time=job.next_run_time,
            status=job.next_run_time is not None and "running" or "stopped"
        )
        tasks.append(task)
    return tasks
