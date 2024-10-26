# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scrapyd_api import ScrapydAPI
import logging

# 初始化 Scrapyd API 客户端，连接 Scrapyd 服务
scrapyd = ScrapydAPI("http://localhost:6800")

# 初始化调度器
scheduler = BackgroundScheduler()
scheduler.start()

# 创建日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def schedule_task(spider_name: str, cron_expression: str):
    """
    添加定时任务到调度器
    """
    trigger = CronTrigger.from_crontab(cron_expression)
    job_id = f"{spider_name}_job"

    # 定义调度器任务的回调函数
    def task():
        try:
            scrapyd.schedule("default", spider_name)
            logger.info(f"Scheduled {spider_name} successfully.")
        except Exception as e:
            logger.error(f"Failed to schedule {spider_name}: {str(e)}")

    # 添加任务到调度器
    scheduler.add_job(task, trigger, id=job_id, replace_existing=True)
    logger.info(f"Scheduled job for spider: {spider_name} with cron: {cron_expression}")

def remove_task(spider_name: str):
    """
    从调度器中移除指定任务
    """
    job_id = f"{spider_name}_job"
    scheduler.remove_job(job_id)
    logger.info(f"Removed job for spider: {spider_name}")
