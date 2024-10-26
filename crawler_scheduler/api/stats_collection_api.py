# -*- coding: utf-8 -*-

"""
spider运行结果数据收集模块
"""

from pprint import pprint


from crawler_scheduler.model.stats_collection_model import StatsCollectionModel
from crawler_scheduler.service import schedule_history_service
from crawler_scheduler.service.stats_collection_service import StatsCollectionService
from fastapi import APIRouter
from crawler_scheduler.model.request_model import AddItemRequest, ListItemRequest, DeleteRequest

stats_collection_api = APIRouter()


# 添加数据项
@stats_collection_api.post("/addItem")
def add_item(req: AddItemRequest):
    pprint(req.dict())

    spider_job_id = req.job_id
    project = req.project
    spider = req.spider
    item_scraped_count = req.item_scraped_count
    item_dropped_count = req.item_dropped_count
    start_time = req.start_time
    finish_time = req.finish_time
    duration = req.duration
    finish_reason = req.finish_reason
    log_error_count = req.log_error_count

    # 查询 scrapyd_server_id
    schedule_history_row = schedule_history_service.get_schedule_history_service_by_job_id(spider_job_id=spider_job_id)
    if schedule_history_row:
        scrapyd_server_id = schedule_history_row.scrapyd_server_id
    else:
        scrapyd_server_id = 0

    StatsCollectionModel.create(
        spider_job_id=spider_job_id,
        scrapyd_server_id=scrapyd_server_id,
        project=project,
        spider=spider,
        item_scraped_count=item_scraped_count,
        item_dropped_count=item_dropped_count,
        start_time=start_time,
        finish_time=finish_time,
        finish_reason=finish_reason,
        log_error_count=log_error_count,
        duration=duration
    )
    return {"message": "数据项添加成功"}

# 列出数据项
@stats_collection_api.post("/listItem")
def list_item(req: ListItemRequest):
    page = req.page
    size = req.size
    project = req.project
    spider = req.spider
    order_prop = req.order_prop
    order_type = req.order_type
    scrapyd_server_id = req.scrapyd_server_id

    return {
        'list': StatsCollectionService.list(
            page=page, size=size,
            scrapyd_server_id=scrapyd_server_id,
            project=project, spider=spider,
            order_prop=order_prop, order_type=order_type
        ),
        'total': StatsCollectionService.count(project=project, spider=spider)
    }

# 删除数据项
@stats_collection_api.post("/delete")
def delete(req: DeleteRequest):
    project = req.project
    spider = req.spider
    scrapyd_server_id = req.scrapyd_server_id

    StatsCollectionService.delete(
        project=project,
        scrapyd_server_id=scrapyd_server_id,
        spider=spider
    )
    return {"message": "数据项删除成功"}