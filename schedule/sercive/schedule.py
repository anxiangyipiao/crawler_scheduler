
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore


# Redis 作业存储配置
JOBSTORES = {
    'default': RedisJobStore(host='localhost', port=6379, db=0)
}


JOB_DEFAULTS = {
    'misfire_grace_time': None,
    'coalesce': True,
    'max_instances': 1
}

# 初始化调度器
scheduler = BackgroundScheduler(jobstores=JOBSTORES, job_defaults=JOB_DEFAULTS)

# 启动调度器
scheduler.start()