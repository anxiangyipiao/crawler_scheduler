# -*- coding: utf-8 -*-
import json
import logging
import uuid
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from crawler_scheduler.config import JOB_STORES_DATABASE_URL, resolve_log_file
from crawler_scheduler.enums.schedule_type_enum import ScheduleTypeEnum
from crawler_scheduler.model.schedule_history_model import ScheduleHistoryModel
from crawler_scheduler.service.scrapyd_service import ScrapydService
from crawler_scheduler.service.stats_collection_service import StatsCollectionService
from crawler_scheduler.utils.sqlite_util import make_sqlite_dir
from crawler_scheduler.utils.time_util import TimeUtil

apscheduler_logger = logging.getLogger('apscheduler')

# file_handler = logging.FileHandler(resolve_log_file('apscheduler.log'))
file_handler = RotatingFileHandler(
    filename=resolve_log_file('apscheduler.log'),
    maxBytes=1024 * 1024 * 1,  # 1MB
    backupCount=1,
    encoding='utf-8'
)

apscheduler_logger.addHandler(file_handler)

# ==============================================
# 调度器服务配置
# ==============================================

make_sqlite_dir(JOB_STORES_DATABASE_URL)

JOBSTORES = {
    'default': SQLAlchemyJobStore(url=JOB_STORES_DATABASE_URL)
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


# ==============================================
# 调度器服务
class ScheduleService(object):

    @classmethod
    def add_job(cls, project, spider, cron,
                scrapyd_server_id,
                schedule_type=ScheduleTypeEnum.ONLY_ONE_SERVER,
                job_id=None, options=None):
    
        # 必传参数校验
        # 检查项目名称是否为空
        if not project:
            raise Exception('project is null')

        # 检查爬虫名称是否为空
        if not spider:
            raise Exception('spider is null')

        # 处理cron表达式
        # 将cron表达式分割成时间部分
        crons = cron.split(' ')

        # 过滤掉空字符串
        crons = filter(lambda x: x, crons)

        # 提取出分钟、小时、日、月、星期几
        minute, hour, day, month, day_of_week = crons

        # 可选参数处理
        if options:
        
            # 将options参数从json字符串转换为字典
            opt = json.loads(options)

            # 检查转换后的options是否为字典类型
            if not isinstance(opt, dict):
                raise Exception("options参数的json数据不能解析为字典dict对象")

        # 生成job_id
        if job_id is None:
            job_id = cls.get_job_id()

        # 构建传递给ScrapydService.run_spider的参数字典
        kwargs = {
            'scrapyd_server_id': scrapyd_server_id,
            'schedule_type': schedule_type,
            'project': project,
            'spider': spider,
            'cron': cron,
            'options': options,
            'schedule_job_id': job_id
        }

        # 调用scheduler的add_job方法添加定时任务
        scheduler.add_job(
            func=ScrapydService.run_spider,  # 定时任务要执行的函数
            trigger='cron',  # 触发类型为cron
            id=job_id,  # 定时任务的唯一标识
            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,  # cron表达式的时间部分
            replace_existing=True,  # 如果已存在同名任务则替换
            kwargs=kwargs)  # 传递给ScrapydService.run_spider的参数

    @classmethod
    def get_job_id(cls):
        """spider_job_id"""
        return uuid.uuid4().hex

    @classmethod
    def get_log_list(cls, page=1, size=20,
                     status=None,
                     project=None,
                     spider=None,
                     schedule_job_id=None,
                     scrapyd_server_id=None
                     ):
        """
        获取调度日志列表
        
        Args:
            cls (type): 类类型，此参数用于类方法中的cls参数，此处无需手动传入
            page (int, optional): 页码，默认为1。
            size (int, optional): 每页显示的记录数，默认为20。
            status (str, optional): 日志状态，默认为None，表示不筛选状态。可选值为'success'和'error'，分别表示成功和失败。
            project (str, optional): 项目名称，默认为None，表示不筛选项目。
            spider (str, optional): 爬虫名称，默认为None，表示不筛选爬虫。
            schedule_job_id (str, optional): 调度任务ID，默认为None，表示不筛选调度任务ID。
            scrapyd_server_id (str, optional): Scrapyd服务器ID，默认为None，表示不筛选Scrapyd服务器ID。
        
        Returns:
            list: 包含日志信息的列表，每个元素是一个字典，包含调度日志的详细信息。
        
        """

        query = ScheduleHistoryModel.select()

        if scrapyd_server_id:
            query = query.where(ScheduleHistoryModel.scrapyd_server_id == scrapyd_server_id)
        if project:
            query = query.where(ScheduleHistoryModel.project == project)
        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)
        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(ScheduleHistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(ScheduleHistoryModel.spider_job_id == '')

        rows = query.order_by(
            ScheduleHistoryModel.create_time.desc()
        ).paginate(page, size).dicts()

        return list(rows)

    @classmethod
    def get_log_list_with_stats(cls, page=1, size=20,
                                status=None,
                                project=None,
                                spider=None,
                                scrapyd_server_id=None,
                                schedule_job_id=None):
        """
        获取调度日志和运行日志。
        
        Args:
            cls (type): 类类型，调用时传入。
            page (int, optional): 页码，默认为1。
            size (int, optional): 每页显示条数，默认为20。
            status (str, optional): 日志状态，默认为None，表示所有状态。
            project (str, optional): 项目名称，默认为None，表示所有项目。
            spider (str, optional): Spider名称，默认为None，表示所有Spider。
            scrapyd_server_id (int, optional): Scrapyd服务器ID，默认为None，表示所有Scrapyd服务器。
            schedule_job_id (int, optional): 调度任务ID，默认为None，表示所有调度任务。
        
        Returns:
            list: 包含调度日志和运行日志的列表，每个元素为字典类型，包含以下字段：
                - spider_job_id (str): Spider任务ID。
                - status (bool): 调度状态，True表示已调度，False表示未调度。
                - schedule_mode (str): 调度模式，'自动'或'手动'。
                - run_status (str): 运行状态，'finished'表示完成，'unknown'表示未知。
                - item_count (int): Item总数，包括已丢弃和已抓取的Item数量。
                - log_error_count (int): 错误日志数量。
                - duration_str (str): 运行时间，格式为HH:MM:SS。
        
        """
        rows = cls.get_log_list(
            page=page, size=size, status=status,
            project=project, spider=spider,
            schedule_job_id=schedule_job_id,
            scrapyd_server_id=scrapyd_server_id
        )

        # 关联schedule
        spider_job_ids = []

        for row in rows:
            # 调度状态
            if row['spider_job_id'] != '':
                spider_job_ids.append(row['spider_job_id'])
                row['status'] = True
            else:
                row['status'] = False

            # 调度模式
            if row['schedule_job_id']:
                row['schedule_mode'] = '自动'
            else:
                row['schedule_mode'] = '手动'

        stats_dict = StatsCollectionService.get_dict_by_spider_job_ids(spider_job_ids)

        # 运行状态
        for row in rows:
            spider_job_id = row['spider_job_id']

            if spider_job_id in stats_dict:
                stats_row = stats_dict[spider_job_id]
                row['run_status'] = 'finished'
                row['item_count'] = stats_row['item_dropped_count'] + stats_row['item_scraped_count']
                row['log_error_count'] = stats_row['log_error_count']
                row['duration_str'] = TimeUtil.format_duration(stats_row['duration'])
            else:
                row['run_status'] = 'unknown'
        return rows

    @classmethod
    def get_log_total_count(cls, project=None, spider=None, schedule_job_id=None, scrapyd_server_id=None):
        """计算日志总条数"""
        query = ScheduleHistoryModel.select()

        if scrapyd_server_id:
            query = query.where(ScheduleHistoryModel.scrapyd_server_id == scrapyd_server_id)

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        return query.count()

    @classmethod
    def get_log_success_count(cls, project=None, spider=None, schedule_job_id=None, scrapyd_server_id=None):
        """计算成功日志条数"""
        query = ScheduleHistoryModel.select()

        if scrapyd_server_id:
            query = query.where(ScheduleHistoryModel.scrapyd_server_id == scrapyd_server_id)

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(ScheduleHistoryModel.spider_job_id != '')
        return query.count()

    @classmethod
    def get_log_error_count(cls, project=None, spider=None, schedule_job_id=None, scrapyd_server_id=None):
        """计算失败日志条数"""
        query = ScheduleHistoryModel.select()

        if scrapyd_server_id:
            query = query.where(ScheduleHistoryModel.scrapyd_server_id == scrapyd_server_id)

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(ScheduleHistoryModel.spider_job_id == '')
        return query.count()

    @classmethod
    def remove_log(cls, project=None, spider=None, schedule_job_id=None, status=None, scrapyd_server_id=None):
        """移除日志"""
        query = ScheduleHistoryModel.delete()

        if scrapyd_server_id:
            query = query.where(ScheduleHistoryModel.scrapyd_server_id == scrapyd_server_id)

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(ScheduleHistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(ScheduleHistoryModel.spider_job_id == '')

        return query.execute()

    @classmethod
    def remove_history_log(cls, days=7):
        """移除历史日志"""
        max_datetime = datetime.now() - timedelta(days=days)

        query = ScheduleHistoryModel.delete().where(
            ScheduleHistoryModel.create_time <= max_datetime
        )

        return query.execute()
