import json
import logging
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from schedule.config import JOB_STORES_DATABASE_URL, resolve_log_file
from schedule.utils.sqlite_util import make_sqlite_dir


apscheduler_logger = logging.getLogger('apscheduler')

file_handler = RotatingFileHandler(
    filename=resolve_log_file('apscheduler.log'),
    maxBytes=1024 * 1024 * 1,  # 1MB
    backupCount=1,
    encoding='utf-8'
)

apscheduler_logger.addHandler(file_handler)

make_sqlite_dir(JOB_STORES_DATABASE_URL)

JOBSTORES = {
    'default': SQLAlchemyJobStore(url=JOB_STORES_DATABASE_URL)
}

JOB_DEFAULTS = {
    'misfire_grace_time': None,
    'coalesce': True,
    'max_instances': 1
}

scheduler = BackgroundScheduler(jobstores=JOBSTORES, job_defaults=JOB_DEFAULTS)

scheduler.start()



class ScheduleService:

    @classmethod
    def add_job(cls, project, spider, cron, scrapyd_server_id, 
                schedule_type='cron', job_id=None, options=None):
        """
        添加定时任务到调度器中。
        """
        if not project or not spider:
            raise ValueError("Both 'project' and 'spider' parameters are required.")
        
        try:
            minute, hour, day, month, day_of_week = cron.split()
        except ValueError:
            raise ValueError("Invalid cron expression format.")

        if job_id is None:
            job_id = cls.get_job_id()

        if options:
            try:
                opt = json.loads(options)
                if not isinstance(opt, dict):
                    raise TypeError("The 'options' parameter must be a valid JSON object representing a dictionary.")
            except json.JSONDecodeError:
                raise ValueError("The 'options' parameter is not a valid JSON string.")
        else:
            opt = {}

        kwargs = {
            'scrapyd_server_id': scrapyd_server_id,
            'schedule_type': schedule_type,
            'project': project,
            'spider': spider,
            'cron': cron,
            'options': opt,
            'schedule_job_id': job_id
        }

        trigger = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week)

        scheduler.add_job(
            func=cls.execute_spider,  
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            kwargs=kwargs
        )
        print(f"Job {job_id} added to the queue.")

    @staticmethod
    def execute_spider(scrapyd_server_id, schedule_type, project, spider, cron, options, schedule_job_id):
        """
        执行爬虫的具体逻辑。
        """
        print(f"Starting job {schedule_job_id}: {spider} from project {project}.")
        cls.print_queue_status()
        
        start_time = datetime.now()
        try:
            # 这里应该是实际的爬虫执行逻辑
            print(f"Executing spider {spider} from project {project} on server {scrapyd_server_id}")
            # 模拟成功
            status = 'success'
            message = 'Task completed successfully.'
        except Exception as e:
            status = 'failure'
            message = str(e)
        finally:
            end_time = datetime.now()
            cls.log_job_history(schedule_job_id, project, spider, start_time, end_time, status, message)
            print(f"Job {schedule_job_id} finished with status: {status}.")
            cls.print_queue_status()

    @classmethod
    def log_job_history(cls, job_id, project, spider, start_time, end_time, status, message):
        """
        记录任务执行的历史到 Redis。
        """
        history = {
            'job_id': job_id,
            'project': project,
            'spider': spider,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'status': status,
            'message': message
        }
        redis_client.rpush('job_history', json.dumps(history))

    @classmethod
    def get_job_id(cls):
        """生成唯一的任务ID"""
        return uuid.uuid4().hex

    @classmethod
    def get_job_history(cls):
        """
        获取所有任务执行历史。
        """
        history_list = []
        for item in redis_client.lrange('job_history', 0, -1):
            history_list.append(json.loads(item))
        return history_list

    @classmethod
    def print_queue_status(cls):
        """
        打印当前任务队列的状态。
        """
        jobs = scheduler.get_jobs()
        if jobs:
            print("Current job queue:")
            for job in jobs:
                print(f"- Job ID: {job.id}, Next Run Time: {job.next_run_time}")
        else:
            print("No jobs in the queue.")

if __name__ == "__main__":
    # 示例：添加一个测试任务
    ScheduleService.add_job('test_project', 'test_spider', '*/5 * * * *', 'server_1')