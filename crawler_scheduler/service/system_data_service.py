# -*- coding: utf-8 -*-
from crawler_scheduler.model import ScrapydServerModel
from crawler_scheduler.service import scrapyd_server_service
from crawler_scheduler.service.schedule_service import scheduler
from crawler_scheduler.service.scrapyd_service import ScrapydService, get_client
from crawler_scheduler.utils.system_info_util import SystemInfoUtil
from crawler_scheduler.version import VERSION


# 系统数据服务 首页数据
class SystemDataService(object):
    @classmethod
    def get_system_data(cls, scrapyd_server_id=None):
        """
        获取系统数据
        
        Args:
            cls (class): 类引用，通常传入类自身
            scrapyd_server_id (int, optional): Scrapyd服务器ID. Defaults to None.
        
        Returns:
            list: 包含系统数据的列表，每个元素都是一个字典，包含以下字段：
                title (str): 数据标题
                count (int): 数据数量
                route (dict): 路由信息，包含以下字段：
                    name (str): 路由名称
                    query (dict, optional): 路由查询参数，默认为空字典
        
        """
        if scrapyd_server_id:
            scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

            client = get_client(scrapyd_server_row)

        try:
            res = client.daemon_status()
        except Exception:
            res = {}

        try:
            projects = len(client.list_projects())
        except Exception:
            projects = 0

        return [
            {
                'title': '项目数量',
                'count': projects,
                'route': {'name': 'project'}
            },
            {
                'title': '定时任务',
                'count': len(scheduler.get_jobs()),
                'route': {'name': 'schedule'}

            },
            {
                'title': '任务总数',
                'count': res.get('total', 0),
                'route': {'name': 'job'}
            },
            {
                'title': '等待任务',
                'count': res.get('pending', 0),
                'route': {'name': 'job', 'query': {'status': 'pending'}}
            },
            {
                'title': '运行任务',
                'count': res.get('running', 0),
                'route': {'name': 'job', 'query': {'status': 'running'}}
            },
            {
                'title': '完成任务',
                'count': res.get('finished', 0),
                'route': {'name': 'job', 'query': {'status': 'finished'}}
            }
        ]

    @classmethod
    def get_system_config(cls):
        """
        获取系统配置信息。
        
        Args:
            cls (type): 类类型，传入的类应该包含此静态方法。
        
        Returns:
            dict: 包含系统配置信息的字典，具体包含Scrapyd服务器的配置信息和Spider管理系统的版本信息。
                - scrapyd: Scrapyd服务器的配置信息，包含url、可用服务器数量、服务器状态。
                    - url (str): Scrapyd服务器的URL地址，此处默认为空字符串。
                    - count (int): 可用的Scrapyd服务器数量。
                    - status (bool): Scrapyd服务器是否可用，根据可用服务器数量是否大于0来判断。
                - spider_admin: Spider管理系统的版本信息。
                    - version (str): Spider管理系统的版本号。
        
        """
        available_scrapyd_server_count = scrapyd_server_service.get_available_scrapyd_server_count()

        return {
            'scrapyd': {
                # 'url': SCRAPYD_SERVER,
                # 'status': ScrapydService.get_status()
                'url': '',
                'count': available_scrapyd_server_count,
                'status': available_scrapyd_server_count > 0
            },
            'spider_admin': {
                'version': VERSION
            }
        }

    @classmethod
    def get_system_info(cls):
        """
        获取系统信息。
        
        Args:
            cls (type): 类对象，此参数在实例方法中通常不需要显式传递，但在类方法中需要。
        
        Returns:
            dict: 包含系统信息的字典，目前包括虚拟内存和磁盘使用情况。
        
        """
        return {
            'virtual_memory': SystemInfoUtil.get_virtual_memory(),
            'disk_usage': SystemInfoUtil.get_disk_usage(),
            # 'net_io_counters': cls.get_net_io_counters(),
        }
