from pydantic import BaseModel
from typing import Optional, List




# login_api 请求体模型
class LoginHistoryParams(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 20



# scrapyd_api 请求体模型
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