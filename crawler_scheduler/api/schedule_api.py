# -*- coding: utf-8 -*-
# ==============================================
# 调度器接口服务
# ==============================================


from fastapi import APIRouter, Request, Depends
from crawler_scheduler.utils.scheduler_util import SchedulerUtil
from crawler_scheduler.service.schedule_service import ScheduleService, scheduler
from crawler_scheduler.model.request_model import *


schedule_api = APIRouter(prefix='/schedule')


#########################
#   任务管理
#########################

# 获取任务列表
@schedule_api.post("/getJobs")
def get_jobs(req: GetJobsRequest):
    order_prop = req.order_prop
    order_type = req.order_type

    jobs = scheduler.get_jobs()
    lst = SchedulerUtil.jobs_to_dict(jobs)

    if order_prop == 'spider':
        is_reverse = (order_type == 'descending')
        def _sort(item):
            return item['kwargs']['spider']
        lst = sorted(lst, key=_sort, reverse=is_reverse)
    return lst

# 添加或更新任务
@schedule_api.post("/addJob")
def add_job(req: AddJobRequest):
    ScheduleService.add_job(
        project=req.project,
        spider=req.spider,
        cron=req.cron,
        scrapyd_server_id=req.scrapyd_server_id,
        schedule_type=req.schedule_type,
        options=req.options,
        job_id=req.job_id
    )
    return {"message": "任务修改成功"}

# 移除任务
@schedule_api.post("/removeJob")
def remove_job(req: JobActionRequest):
    scheduler.remove_job(job_id=req.job_id)
    return {"message": "任务移除成功"}

# 暂停任务
@schedule_api.post("/pauseJob")
def pause_job(req: JobActionRequest):
    scheduler.pause_job(job_id=req.job_id)
    return {"message": "暂停成功"}

# 继续任务
@schedule_api.post("/resumeJob")
def resume_job(req: JobActionRequest):
    scheduler.resume_job(job_id=req.job_id)
    return {"message": "继续运行"}

# 获取任务详情
@schedule_api.post("/jobDetail")
def job_detail(req: JobDetailRequest):
    job = scheduler.get_job(job_id=req.job_id)
    return SchedulerUtil.job_to_dict(job)


#########################
#   调度器管理
#########################

@schedule_api.post("/start")
def start():
    """启动调度"""
    scheduler.start()


@schedule_api.post("/state")
def state():
    """查看状态"""
    return {
        'state': SchedulerUtil.get_state_name(scheduler.state)
    }


@schedule_api.post("/shutdown")
def shutdown():
    """关闭调度"""
    scheduler.shutdown()


@schedule_api.post("/pause")
def pause():
    """全部任务暂停"""
    scheduler.pause()


@schedule_api.post("/resume")
def resume():
    """全部任务继续"""
    scheduler.resume()


@schedule_api.post("/removeAllJobs")
def remove_all_jobs():
    """全部任务移除"""
    scheduler.remove_all_jobs()


# ==============================================
# 调度日志
# ==============================================

@schedule_api.post("/scheduleLogs")
def schedule_logs(req: ScheduleLogsRequest):
    """调度日志"""
    logs = ScheduleService.get_log_list_with_stats(
        scrapyd_server_id=req.scrapyd_server_id,
        project=req.project,
        spider=req.spider,
        page=req.page,
        size=req.size,
        status=req.status,
        schedule_job_id=req.schedule_job_id
    )
    total_count = ScheduleService.get_log_total_count(
        scrapyd_server_id=req.scrapyd_server_id,
        project=req.project,
        spider=req.spider,
        schedule_job_id=req.schedule_job_id
    )
    success_count = ScheduleService.get_log_success_count(
        scrapyd_server_id=req.scrapyd_server_id,
        project=req.project,
        spider=req.spider,
        schedule_job_id=req.schedule_job_id
    )
    error_count = ScheduleService.get_log_error_count(
        scrapyd_server_id=req.scrapyd_server_id,
        project=req.project,
        spider=req.spider,
        schedule_job_id=req.schedule_job_id
    )
    return {
        'list': logs,
        'total': total_count,
        'success': success_count,
        'error': error_count
    }

# 删除调度日志
@schedule_api.post("/removeScheduleLogs")
def remove_schedule_logs(req: RemoveScheduleLogsRequest):
    """删除调度日志"""
    ScheduleService.remove_log(
        scrapyd_server_id=req.scrapyd_server_id,
        project=req.project,
        spider=req.spider,
        schedule_job_id=req.schedule_job_id,
        status=req.status
    )
    return {"message": "日志删除成功"}
