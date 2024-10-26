

from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class ScrapydClienModel(BaseModel):
    url: str
    port: int


class UserModel(BaseModel):
    username: str
    password: str



class TaskModel(BaseModel):
    project: str
    spider: str
    settings: dict = {}