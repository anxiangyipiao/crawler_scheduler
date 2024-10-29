# -*- coding: utf-8 -*-
# ==============================================
# 系统信息接口
# ==============================================

from fastapi import APIRouter
from crawler_scheduler.model.request_model import SystemDataRequest
from crawler_scheduler.service.system_data_service import SystemDataService

system_info_api = APIRouter(prefix='/system')


# 系统信息接口
@system_info_api.post('/systemInfo')
def get_system_info():
    return SystemDataService.get_system_info()

# 系统数据接口
@system_info_api.post("/systemData")
def get_system_data(req: SystemDataRequest):
    return SystemDataService.get_system_data(scrapyd_server_id=req.scrapydServerId)

# 系统配置接口
@system_info_api.post("/systemConfig")
def get_system_config():
    return SystemDataService.get_system_config()