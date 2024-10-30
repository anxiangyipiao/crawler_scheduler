# -*- coding: utf-8 -*-
"""
@File    : scrapyd_server_api.py
@Date    : 2024-07-13
"""

from crawler_scheduler.model.scrapyd_server_model import ScrapydServerModel
from fastapi import APIRouter
from crawler_scheduler.model.request_model import AddScrapydServerRequest, UpdateScrapydServerRequest, UpdateScrapydServerStatusRequest, DeleteScrapydServerRequest, GetScrapydServerRequest

scrapyd_server_api = APIRouter(prefix='/scrapydServer')



# 添加swagger注释
@scrapyd_server_api.post("/addScrapydServer")
def add_scrapyd_server(req: AddScrapydServerRequest):
    """
    添加一个新的 Scrapyd 服务器。

    - **server_url**: Scrapyd 服务器的 URL。
    - **server_name**: Scrapyd 服务器的名称。
    - **username**: Scrapyd 服务器的用户名。
    - **password**: Scrapyd 服务器的密码。
    - **status**: Scrapyd 服务器的状态（启用/禁用）。

    返回一个消息表示操作成功。
    """
    ScrapydServerModel.create(
        server_url=req.server_url,
        server_name=req.server_name,
        username=req.username,
        password=req.password,
        status=req.status
    )
    # return {"message": "Scrapyd服务器添加成功"}

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
    # return {"message": "Scrapyd服务器更新成功"}

# 更新Scrapyd服务器状态
@scrapyd_server_api.post("/updateScrapydServerStatus")
def update_scrapyd_server_status(req: UpdateScrapydServerStatusRequest):
    ScrapydServerModel.update(
        status=req.status
    ).where(
        ScrapydServerModel.id == req.scrapyd_server_id
    ).execute()
    # return {"message": "Scrapyd服务器状态更新成功"}

# 删除Scrapyd服务器
@scrapyd_server_api.post("/deleteScrapydServer")
def delete_scrapyd_server(req: DeleteScrapydServerRequest):
    ScrapydServerModel.delete().where(
        ScrapydServerModel.id == req.scrapyd_server_id
    ).execute()
    # return {"message": "Scrapyd服务器删除成功"}

# 获取Scrapyd服务器信息
@scrapyd_server_api.post("/getScrapydServer")
def get_scrapyd_server(req: GetScrapydServerRequest):
    server = ScrapydServerModel.get_by_id(req.scrapyd_server_id)
    return server

# 获取Scrapyd服务器分页信息
@scrapyd_server_api.post("/getScrapydServerPage")
def get_scrapyd_server_page():
    """
    获取Scrapyd服务器页面信息
    
    Args:
        无
    
    Returns:
        dict: 包含Scrapyd服务器列表和总数量的字典
            - list: Scrapyd服务器列表，每个元素为一个Scrapyd服务器信息字典
            - total: Scrapyd服务器总数量
    
    """
    lst = ScrapydServerModel.select()
    total = ScrapydServerModel.select().count()
    return {
        'list': [server for server in lst],
        'total': total
    }