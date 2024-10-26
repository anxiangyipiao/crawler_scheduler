# -*- coding: utf-8 -*-

"""
行为历史模块
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from crawler_scheduler.service.action_history_service import ActionHistoryService,login_history_wrap
from crawler_scheduler.service.auth_service import AuthService

User = FastAPI()

# 定义请求体模型
class LoginHistoryParams(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 20


@User.post('/loginHistoryList')
def login_history_list(params: LoginHistoryParams = Depends()):
    page = params.page
    size = params.size

    rows = ActionHistoryService.get_login_history(
        page=page, size=size
    )
    total = ActionHistoryService.get_login_history_count()

    return {
        'list': rows,
        'total': total
    }



@User.post('/login')
@login_history_wrap
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    return await AuthService.login(
        username=username,
        password=password
    )