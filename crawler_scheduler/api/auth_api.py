# -*- coding: utf-8 -*-

"""
行为历史模块
"""

from fastapi import APIRouter, Request, Depends
from crawler_scheduler.service.action_history_service import ActionHistoryService,login_history_wrap
from crawler_scheduler.service.auth_service import AuthService
from crawler_scheduler.model.request_model import LoginHistoryParams


auth_api = APIRouter()


@auth_api.post('/loginHistoryList')
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


@auth_api.post('/login')
@login_history_wrap
def login(request: Request):
    data = request.json()
    username = data.get('username')
    password = data.get('password')

    return AuthService.login(
        username=username,
        password=password
    )