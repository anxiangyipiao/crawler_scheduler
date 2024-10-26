# -*- coding: utf-8 -*-
# ==============================================
# scrapyd 接口服务
# ==============================================


from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from crawler_scheduler.service.auth_service import AuthService
from crawler_scheduler.model.request_model import *
from crawler_scheduler.model import ScrapydServerModel
from crawler_scheduler.service.scrapyd_service import get_client, ScrapydService


scrapydApi = FastAPI()


# 全局请求拦截器
@scrapydApi.middleware("http")
async def check_token(request: Request, call_next):
    token = request.headers.get('Token')
    AuthService.check_token(token)
    response = await call_next(request)
    return response


# 定义路由
@scrapydApi.post('/daemonStatus')
async def daemon_status(request: Request, req: DaemonStatusRequest = Depends()):
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.daemon_status()

@scrapydApi.post('/addVersion')
async def add_version(request: Request, req: AddVersionRequest = Depends()):
    egg = req.egg
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.add_version(project, egg)

@scrapydApi.post('/listProjects')
async def list_projects(request: Request, req: ListProjectsRequest = Depends()):
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_projects()

@scrapydApi.post('/listVersions')
async def list_versions(request: Request, req: ListVersionsRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_versions_format(project=project)

@scrapydApi.post('/listJobs')
async def list_jobs(request: Request, req: ListJobsRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_jobs(project=project)

@scrapydApi.post('/listJobsMerge')
async def list_jobs_merge(request: Request, req: ListJobsMergeRequest = Depends()):
    project = req.project
    status = req.status
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_jobs_merge(project=project, status=status)

@scrapydApi.post('/cancel')
async def cancel(request: Request, req: CancelRequest = Depends()):
    project = req.project
    job = req.job
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.cancel(project=project, job=job)

@scrapydApi.post('/cancelAllJob')
async def cancel_all_job(request: Request, req: CancelAllJobRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.cancel_all_job(project=project)

@scrapydApi.post('/listSpiders')
async def list_spiders(request: Request, req: ListSpidersRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_spiders(project=project)

@scrapydApi.post('/schedule')
async def schedule(request: Request, req: ScheduleRequest = Depends()):
    project = req.project
    spider = req.spider
    scrapyd_server_id = req.scrapydServerId
    options = req.options
    kwargs = {
        'project': project,
        'spider': spider,
        'scrapyd_server_id': scrapyd_server_id,
        'options': options
    }
    # fix: 记录手动运行日志
    ScrapydService.run_spider(**kwargs)
    return {"status": "ok"}

@scrapydApi.post('/deleteVersion')
async def delete_version(request: Request, req: DeleteVersionRequest = Depends()):
    project = req.project
    version = req.version
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.delete_version(project=project, version=version)

@scrapydApi.post('/deleteProject')
async def delete_project(request: Request, req: DeleteProjectRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.delete_project(project=project)

@scrapydApi.post('/logs')
async def logs(request: Request, req: LogsRequest = Depends()):
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.logs()

@scrapydApi.post('/projectLogs')
async def project_logs(request: Request, req: ProjectLogsRequest = Depends()):
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.project_logs(project=project)

@scrapydApi.post('/spiderLogs')
async def spider_logs(request: Request, req: SpiderLogsRequest = Depends()):
    project = req.project
    spider = req.spider
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.spider_logs(project=project, spider=spider)

@scrapydApi.post('/jobLog')
async def job_log(request: Request, req: JobLogRequest = Depends()):
    project = req.project
    spider = req.spider
    job = req.job
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    res = client.job_log(project=project, spider=spider, job=job)
    return Response(res, media_type='text/plain;charset=utf-8')

