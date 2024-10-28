# -*- coding: utf-8 -*-
# ==============================================
# scrapyd 接口服务
# ==============================================


from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from crawler_scheduler.model.request_model import *
from crawler_scheduler.model import ScrapydServerModel
from crawler_scheduler.service.scrapyd_service import get_client, ScrapydService


scrapyd_api = APIRouter()


# 定义路由
@scrapyd_api.post('/daemonStatus')
def daemon_status(request: Request, req: DaemonStatusRequest = Depends()):
    """
    获取Scrapyd服务器守护进程状态
    
    Args:
        request (Request): 请求对象
        req (DaemonStatusRequest): 请求参数对象，依赖注入获取
    
    Returns:
        dict: Scrapyd服务器守护进程状态
    
    """
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.daemon_status()

@scrapyd_api.post('/addVersion')
def add_version(request: Request, req: AddVersionRequest = Depends()):
    """
    添加版本
    
    Args:
        request (Request): 请求对象
        req (AddVersionRequest, optional): 请求参数, 默认值为 Depends(). Defaults to Depends().
    
    Returns:
        dict: 添加版本后的结果
    
    """
    egg = req.egg
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.add_version(project, egg)




@scrapyd_api.post('/listProjects')
def list_projects(request: Request, req: ListProjectsRequest = Depends()):
    """
    获取Scrapyd服务器上所有的项目列表
    
    Args:
        request (Request): 请求对象
        req (ListProjectsRequest, optional): 请求参数，默认为Depends(). 
            包含Scrapyd服务器ID（scrapydServerId）
    
    Returns:
        List[str]: Scrapyd服务器上所有的项目名称列表
    
    Raises:
        ScrapydServerError: 如果请求Scrapyd服务器失败，会抛出此异常
    
    """
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_projects()

@scrapyd_api.post('/listVersions')
def list_versions(request: Request, req: ListVersionsRequest = Depends()):
    """
    获取指定Scrapyd服务器的项目版本列表
    
    Args:
        request (Request): 请求对象
        req (ListVersionsRequest, optional): 请求参数对象，默认为None。
            project (str): 项目名称
            scrapydServerId (int): Scrapyd服务器ID
    
    Returns:
        dict: 包含项目版本信息的字典
    
    Raises:
        ScrapydServerError: 如果Scrapyd服务器返回错误
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_versions_format(project=project)

@scrapyd_api.post('/listJobs')
def list_jobs(request: Request, req: ListJobsRequest = Depends()):
    """
    列出Scrapyd服务器上的所有作业。
    
    Args:
        request (Request): 请求对象，包含了HTTP请求的所有信息。
        req (ListJobsRequest, optional): 请求参数对象，默认为None。
    
    Returns:
        dict: 包含Scrapyd服务器上指定项目的所有作业信息的字典。
    
    Raises:
        异常类型: 当Scrapyd服务器连接失败或请求参数有误时抛出异常。
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_jobs(project=project)

@scrapyd_api.post('/listJobsMerge')
def list_jobs_merge(request: Request, req: ListJobsMergeRequest = Depends()):
    """
    合并列出Scrapyd服务器上的所有作业。
    
    Args:
        request (Request): HTTP请求对象。
        req (ListJobsMergeRequest, optional): 请求参数对象，默认为None。
    
    Returns:
        ScrapydClient.list_jobs_merge方法的返回值，包含Scrapyd服务器上符合条件的作业列表。
    
    Raises:
        ScrapydClientError: 当ScrapydClient调用出错时抛出。
    
    """
    project = req.project
    status = req.status
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_jobs_merge(project=project, status=status)

@scrapyd_api.post('/cancel')
def cancel(request: Request, req: CancelRequest = Depends()):
    """
    取消Scrapy任务
    
    Args:
        request (Request): FastAPI的请求对象
        req (CancelRequest, optional): 请求体，默认为Depends()。包含项目名project、任务名job和Scrapyd服务器ID scrapydServerId。
    
    Returns:
        dict: Scrapy任务取消的结果，包括状态码status和消息message。
    
    """
    project = req.project
    job = req.job
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.cancel(project=project, job=job)

@scrapyd_api.post('/cancelAllJob')
def cancel_all_job(request: Request, req: CancelAllJobRequest = Depends()):
    """
    取消指定Scrapyd服务器上的所有任务
    
    Args:
        request (Request): HTTP请求对象
        req (CancelAllJobRequest, optional): 取消所有任务的请求参数，默认为Depends()。
    
    Returns:
        dict: 取消所有任务的结果
    
    Raises:
        HTTPException: 当Scrapyd服务器不存在或请求参数不合法时抛出
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.cancel_all_job(project=project)

@scrapyd_api.post('/listSpiders')
def list_spiders(request: Request, req: ListSpidersRequest = Depends()):
    """
    列出指定Scrapyd服务器上指定项目的爬虫列表。
    
    Args:
        request (Request): 请求对象。
        req (ListSpidersRequest, optional): 请求参数对象，默认为None。包含项目名称和Scrapyd服务器ID。
    
    Returns:
        dict: 包含爬虫列表的字典。
    
    Raises:
        ScrapydServerError: 当Scrapyd服务器返回错误时抛出。
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.list_spiders(project=project)

@scrapyd_api.post('/schedule')
def schedule(request: Request, req: ScheduleRequest = Depends()):
    """
    调度爬虫运行
    
    Args:
        request (Request): FastAPI的请求对象
        req (ScheduleRequest, optional): 调度请求体，默认为Depends()。
    
    Returns:
        dict: 响应体，包含状态码为'ok'的字典
    
    """
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

@scrapyd_api.post('/deleteVersion')
def delete_version(request: Request, req: DeleteVersionRequest = Depends()):
    """
    删除指定Scrapyd服务器的项目版本
    
    Args:
        request (Request): 请求对象，包含请求头等信息
        req (DeleteVersionRequest, optional): 删除版本请求对象，默认为Depends()自动解析请求体中的参数. Defaults to Depends().
    
    Returns:
        dict: 删除版本的结果，成功时返回Scrapyd服务器响应的字典
    
    """
    project = req.project
    version = req.version
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.delete_version(project=project, version=version)

@scrapyd_api.post('/deleteProject')
def delete_project(request: Request, req: DeleteProjectRequest = Depends()):
    """
    删除项目
    
    Args:
        request (Request): 请求对象
        req (DeleteProjectRequest, optional): 删除项目请求体, 默认为Depends(). Defaults to Depends().
    
    Returns:
        bool: 删除项目结果
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.delete_project(project=project)

@scrapyd_api.post('/logs')
def logs(request: Request, req: LogsRequest = Depends()):
    """
    获取Scrapyd服务器的日志信息
    
    Args:
        request (Request): FastAPI的请求对象
        req (LogsRequest, optional): 请求参数对象，默认为Depends()自动注入. Defaults to Depends().
    
    Returns:
        dict: Scrapyd服务器的日志信息
    
    """
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.logs()

@scrapyd_api.post('/projectLogs')
def project_logs(request: Request, req: ProjectLogsRequest = Depends()):
    """
    获取项目的日志信息。
    
    Args:
        request (Request): FastAPI 请求对象。
        req (ProjectLogsRequest, optional): 请求参数，默认为Depends()。
    
    Returns:
        str: 项目的日志信息。
    
    Raises:
        如果 scrapyd 服务器不存在或无法连接，则抛出异常。
    
    """
    project = req.project
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.project_logs(project=project)

@scrapyd_api.post('/spiderLogs')
def spider_logs(request: Request, req: SpiderLogsRequest = Depends()):
    """
    获取指定Scrapyd服务器上指定项目的Spider的日志信息。
    
    Args:
        request (Request): 请求对象。
        req (SpiderLogsRequest, optional): 请求参数对象，默认为None。如果未提供，则使用Depends()自动填充。
    
    Returns:
        dict: 包含Spider日志信息的字典。
    
    Raises:
        HTTPError: 如果请求失败，则抛出HTTPError异常。
    
    """
    project = req.project
    spider = req.spider
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    return client.spider_logs(project=project, spider=spider)

@scrapyd_api.post('/jobLog')
def job_log(request: Request, req: JobLogRequest = Depends()):
    """
    查询任务日志
    
    Args:
        request (Request): 请求对象
        req (JobLogRequest, optional): 请求体, 默认为Depends(). Defaults to Depends().
    
    Returns:
        Response: 包含任务日志的响应对象
    
    """
    project = req.project
    spider = req.spider
    job = req.job
    scrapyd_server_id = req.scrapydServerId
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)
    client = get_client(scrapyd_server_row)
    res = client.job_log(project=project, spider=spider, job=job)
    return Response(res, media_type='text/plain;charset=utf-8')

