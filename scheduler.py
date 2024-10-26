# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scrapyd_api import ScrapydAPI
from sqlalchemy.orm import Session
from model import Task, SessionLocal
import logging

scrapyd = ScrapydAPI("http://localhost:6800")
scheduler = BackgroundScheduler()
scheduler.start()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def schedule_task(db: Session, spider_name: str, cron_expression: str):
    trigger = CronTrigger.from_crontab(cron_expression)
    job_id = f"{spider_name}_job"

    def task():
        try:
            scrapyd.schedule("default", spider_name)
            logger.info(f"Scheduled {spider_name} successfully.")
        except Exception as e:
            logger.error(f"Failed to schedule {spider_name}: {str(e)}")

    # 添加任务到调度器并保存到数据库
    scheduler.add_job(task, trigger, id=job_id, replace_existing=True)
    new_task = Task(spider_name=spider_name, cron_expression=cron_expression)
    db.add(new_task)
    db.commit()
    logger.info(f"Scheduled job for spider: {spider_name} with cron: {cron_expression}")

def remove_task(db: Session, spider_name: str):
    job_id = f"{spider_name}_job"
    scheduler.remove_job(job_id)

    # 更新数据库中的任务状态
    task = db.query(Task).filter(Task.spider_name == spider_name).first()
    if task:
        task.status = "removed"
        db.commit()
        logger.info(f"Removed job for spider: {spider_name}")
