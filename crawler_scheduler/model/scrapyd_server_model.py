# -*- coding: utf-8 -*-
"""
scrapyd_server_model.py
"""
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField
from playhouse.shortcuts import model_to_dict

from crawler_scheduler.model.base import BaseModels


class ScrapydServerModel(BaseModels):
   
    id = IntegerField(primary_key=True)   #类型的主键，唯一标识每个 Scrapyd 服务器配置。

    server_url = CharField()    #存储 Scrapyd 服务器的 URL 地址，用于连接和管理爬虫任务。
    # 别名
    server_name = CharField(default="") #存储 Scrapyd 服务器的别名，默认值为空字符串，可以用来描述服务器的用途或位置。

    username = CharField(default="") #存储连接 Scrapyd 服务器所需的用户名和密码。默认值为空字符串，可以留空或作为 Scrapyd 服务器的认证信息。
    password = CharField(default="") #存储连接 Scrapyd 服务器所需的用户名和密码。默认值为空字符串，可以留空或作为 Scrapyd 服务器的认证信息。

    status = IntegerField(default=0) #用于表示 Scrapyd 服务器的状态，默认值为 0。通常用于表示服务器是否正常工作，例如 0 可能表示“空闲”或“不可用”，而 1 表示“正常”或“已

    # 最后提交任务的时间
    last_time = DateTimeField(default=datetime.now) #用于记录最后一次提交任务到该 Scrapyd 服务器的时间，默认为当前时间 datetime.now。

    create_time = DateTimeField(default=datetime.now) #记录该服务器配置的创建时间，默认值为当前时间 datetime.now
    update_time = DateTimeField(default=datetime.now) #记录该服务器配置的创建时间，默认值为当前时间 datetime.now

    def to_dict(self):
        return model_to_dict(self)

