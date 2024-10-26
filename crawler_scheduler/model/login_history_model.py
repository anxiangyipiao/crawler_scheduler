# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField
from crawler_scheduler.model.base import BaseModels
from pydantic import BaseModel
from typing import Optional, List

class LoginHistoryModel(BaseModels):
    """登录日志"""
    id = AutoField(primary_key=True)

    username = CharField(max_length=32)
    ip = CharField(max_length=32)
    address = CharField()
    user_agent = CharField()
    system = CharField(max_length=32)
    browser = CharField(max_length=32)
    version = CharField(max_length=32)
    # 登录结果
    result = BooleanField()

    create_time = DateTimeField(default=datetime.now)



# 请求体模型
class DaemonStatusRequest(BaseModel):
    scrapydServerId: int

class AddVersionRequest(BaseModel):
    egg: bytes
    project: str
    scrapydServerId: int

class ListProjectsRequest(BaseModel):
    scrapydServerId: int

class ListVersionsRequest(BaseModel):
    project: str
    scrapydServerId: int

class ListJobsRequest(BaseModel):
    project: str
    scrapydServerId: int

class ListJobsMergeRequest(BaseModel):
    project: str
    status: Optional[str]
    scrapydServerId: int

class CancelRequest(BaseModel):
    project: str
    job: str
    scrapydServerId: int

class CancelAllJobRequest(BaseModel):
    project: str
    scrapydServerId: int

class ListSpidersRequest(BaseModel):
    project: str
    scrapydServerId: int

class ScheduleRequest(BaseModel):
    project: str
    spider: str
    scrapydServerId: int
    options: dict

class DeleteVersionRequest(BaseModel):
    project: str
    version: str
    scrapydServerId: int

class DeleteProjectRequest(BaseModel):
    project: str
    scrapydServerId: int

class LogsRequest(BaseModel):
    scrapydServerId: int

class ProjectLogsRequest(BaseModel):
    project: str
    scrapydServerId: int

class SpiderLogsRequest(BaseModel):
    project: str
    spider: str
    scrapydServerId: int

class JobLogRequest(BaseModel):
    project: str
    spider: str
    job: str
    scrapydServerId: int
