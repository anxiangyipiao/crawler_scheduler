# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField, BooleanField, AutoField
from crawler_scheduler.model.base import BaseModels

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


