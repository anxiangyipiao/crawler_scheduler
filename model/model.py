

from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class ScrapydClienModel(BaseModel):
    url: str
    port: int


class UserModel(BaseModel):
    username: str
    password: str



class ScheduledTaskModel(BaseModel):
    id: Optional[str]  # 任务的唯一标识符
    name: str  # 任务的名称
    interval: int  # 任务的执行间隔（秒）
    next_run_time: Optional[datetime]  # 下次运行时间
    status: str  # 任务状态（例如：'running', 'paused', 'stopped'）

    class Config:
        orm_mode = True  # 允许从 ORM 模型转换