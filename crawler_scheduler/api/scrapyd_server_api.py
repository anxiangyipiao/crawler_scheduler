# -*- coding: utf-8 -*-
"""
@File    : scrapyd_server_api.py
@Date    : 2024-07-13
"""

from crawler_scheduler.model.scrapyd_server_model import ScrapydServerModel
from fastapi import APIRouter
from crawler_scheduler.model.request_model import AddScrapydServerRequest, UpdateScrapydServerRequest, UpdateScrapydServerStatusRequest, DeleteScrapydServerRequest, GetScrapydServerRequest

scrapyd_server_api = APIRouter()


# 添加Scrapyd服务器
@scrapyd_server_api.post("/addScrapydServer")
def add_scrapyd_server(req: AddScrapydServerRequest):
    ScrapydServerModel.create(
        server_url=req.server_url,
        server_name=req.server_name,
        username=req.username,
        password=req.password,
        status=req.status
    )
    return {"message": "Scrapyd服务器添加成功"}

# 更新Scrapyd服务器
@scrapyd_server_api.post("/updateScrapydServer")
def update_scrapyd_server(req: UpdateScrapydServerRequest):
    ScrapydServerModel.update(
        server_url=req.server_url,
        server_name=req.server_name,
        username=req.username,
        password=req.password,
        status=req.status
    ).where(
        ScrapydServerModel.id == req.scrapyd_server_id
    ).execute()
    return {"message": "Scrapyd服务器更新成功"}

# 更新Scrapyd服务器状态
@scrapyd_server_api.post("/updateScrapydServerStatus")
def update_scrapyd_server_status(req: UpdateScrapydServerStatusRequest):
    ScrapydServerModel.update(
        status=req.status
    ).where(
        ScrapydServerModel.id == req.scrapyd_server_id
    ).execute()
    return {"message": "Scrapyd服务器状态更新成功"}

# 删除Scrapyd服务器
@scrapyd_server_api.post("/deleteScrapydServer")
def delete_scrapyd_server(req: DeleteScrapydServerRequest):
    ScrapydServerModel.delete().where(
        ScrapydServerModel.id == req.scrapyd_server_id
    ).execute()
    return {"message": "Scrapyd服务器删除成功"}

# 获取Scrapyd服务器信息
@scrapyd_server_api.post("/getScrapydServer")
def get_scrapyd_server(req: GetScrapydServerRequest):
    server = ScrapydServerModel.get_by_id(req.scrapyd_server_id)
    return server

# 获取Scrapyd服务器分页信息
@scrapyd_server_api.post("/getScrapydServerPage")
def get_scrapyd_server_page():
    lst = ScrapydServerModel.select()
    total = ScrapydServerModel.select().count()
    return {
        'list': [server for server in lst],
        'total': total
    }