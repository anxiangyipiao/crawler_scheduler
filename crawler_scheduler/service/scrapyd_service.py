# -*- coding: utf-8 -*-
import json

from requests.auth import HTTPBasicAuth
from crawler_scheduler.scrapyd_api import ScrapydClient


from crawler_scheduler.enums.schedule_type_enum import ScheduleTypeEnum
from crawler_scheduler.model.schedule_history_model import ScheduleHistoryModel
from crawler_scheduler.service import scrapyd_server_service


def get_client(scrapyd_server_row):
    """
    获取scrapyd 客户端的工厂方法
    @since 2.0.8
    :return:
    """

    # 初始化参数字典
    params = {
        'base_url': scrapyd_server_row.server_url.rstrip('/')  # 基础URL，去除末尾的斜杠
    }

    # 如果scrapyd_server_row中有用户名和密码
    if scrapyd_server_row.username and scrapyd_server_row.password:
        # 更新参数字典，添加HTTP基本认证信息
        params.update({
            'auth': HTTPBasicAuth(scrapyd_server_row.username, scrapyd_server_row.password)  # HTTP基本认证信息
        })

    # 返回Scrapyd客户端实例
    return ScrapydClient(**params)


class ScrapydService(object):

    @classmethod
    def run_spider(cls, **kwargs):
       
        # 获取项目名和爬虫名
        project = kwargs['project']
        spider = kwargs['spider']

        # 获取scrapyd服务器ID
        scrapyd_server_id = kwargs['scrapyd_server_id']

        # 获取调度类型，默认为ONLY_ONE_SERVER
        schedule_type = kwargs.get('schedule_type') or ScheduleTypeEnum.ONLY_ONE_SERVER

        # 获取调度任务ID和其他参数
        schedule_job_id = kwargs.get('schedule_job_id')
        options = kwargs.get('options')

        # 默认值处理
        # 如果options存在，则将其解析为字典，否则初始化一个空字典
        if options:
            opts = json.loads(options)
        else:
            opts = {}

        try:
            # 根据调度类型选择服务器
            # 如果是随机轮询，则获取可用的scrapyd服务器
            if schedule_type == ScheduleTypeEnum.RANDOM_SERVER:
                # 随机轮询
                scrapyd_server_row = scrapyd_server_service.get_available_scrapyd_server()
            # 如果是指定服务器，则根据scrapyd服务器ID获取可用的scrapyd服务器
            else:
                # 指定服务器
                scrapyd_server_row = scrapyd_server_service.get_available_scrapyd_server_by_id(
                    scrapyd_server_id=scrapyd_server_id
                )

            # 如果没有可用的scrapyd服务器，则抛出异常
            if not scrapyd_server_row:
                raise Exception("没有可用的scrapyd")

            # 获取scrapyd服务器ID
            scrapyd_server_id = scrapyd_server_row.id

            # 获取scrapyd客户端
            client = get_client(scrapyd_server_row)

            # 提交爬虫任务
            res = client.schedule(project=project, spider=spider, **opts)

            # 获取爬虫任务ID
            spider_job_id = res['jobid']
            message = ''

        except Exception as e:
            # 捕获异常并记录错误信息
            message = str(e)
            spider_job_id = ''

        # 记录调度历史
        ScheduleHistoryModel.insert_row(
            scrapyd_server_id=scrapyd_server_id,
            project=project,
            spider=spider,
            schedule_job_id=schedule_job_id,
            spider_job_id=spider_job_id,
            options=options,
            message=message
        )

    @classmethod
    def get_status(cls):
        # 尝试获取客户端
        try:
            # 获取客户端
            client = get_client(None)

            # 调用客户端的daemon_status方法
            res = client.daemon_status()
            # 根据返回结果判断状态
            status = True if res['status'] == 'ok' else False
        except Exception:
            # 捕获异常，设置状态为False
            status = False

        # 返回状态
        return status

    def get_active_jobs_count(scrapyd_server_row):
        
        """
        获取指定Scrapyd服务器上的活跃任务数。
        
        :param scrapyd_server_row: 包含Scrapyd服务器信息的对象
        :return: 活跃任务的数量
        """
        
        client = get_client(scrapyd_server_row)
        jobs = client.list_jobs(scrapyd_server_row.project)  # 假设项目名已经存在于服务器行中
        active_jobs = jobs['running'] + jobs['pending']
        return len(active_jobs)




if __name__ == '__main__':
    ScrapydService.run_spider(project='project', spider='baidu', schedule_job_id="xx")
