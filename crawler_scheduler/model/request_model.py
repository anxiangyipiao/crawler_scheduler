from pydantic import BaseModel
from typing import Optional, List




# login_api 请求体模型
class LoginHistoryParams(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 20


class LoginParams(BaseModel):
    username: str
    password: str



# system_info_api 请求体模型
class SystemDataRequest(BaseModel):
    scrapydServerId: int

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



# schedule_api 请求模型
class GetJobsRequest(BaseModel):
    order_prop: Optional[str] = None
    order_type: Optional[str] = 'descending'

class AddJobRequest(BaseModel):
    job_id: Optional[str] = None
    project: str
    spider: str
    cron: str
    scrapyd_server_id: int
    schedule_type: str
    options: Optional[dict] = None

class JobActionRequest(BaseModel):
    job_id: str

class JobDetailRequest(BaseModel):
    job_id: str

class ScheduleLogsRequest(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 20
    status: Optional[str] = None
    project: Optional[str] = None
    spider: Optional[str] = None
    schedule_job_id: Optional[str] = None
    scrapyd_server_id: Optional[int] = None

class RemoveScheduleLogsRequest(BaseModel):
    status: Optional[str] = None
    project: Optional[str] = None
    spider: Optional[str] = None
    schedule_job_id: Optional[str] = None
    scrapyd_server_id: Optional[int] = None
