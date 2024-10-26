# -*- coding: utf-8 -*-
"""
@File    : schedule_history_service.py
@Date    : 2024-07-18
"""
from crawler_scheduler.model import ScheduleHistoryModel


def get_schedule_history_service_by_job_id(spider_job_id):
    """
    根据作业ID获取作业调度历史服务
    
    Args:
        spider_job_id (int): 作业ID
    
    Returns:
        ScheduleHistoryModel: 作业调度历史模型实例或None（如果没有找到对应的作业调度历史）
    
    """
    return ScheduleHistoryModel.select().where(
        ScheduleHistoryModel.spider_job_id == spider_job_id
    ).first()