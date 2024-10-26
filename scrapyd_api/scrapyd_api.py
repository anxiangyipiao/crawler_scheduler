from __future__ import unicode_literals

from .exceptions import ScrapydException
from session_request import SessionRequest


class ScrapydAPI(SessionRequest):
    """
    文档
    https://scrapyd.readthedocs.io/en/stable/api.html
    """

    def __init__(self, base_url='http://localhost:6800', **kwargs):
        super().__init__(base_url, **kwargs)

    def after_request(self, response):
        """请求后 响应处理器"""
        res = response.json()

        if res['status'] == 'ok':
            return res
        else:
            raise ScrapydException(res['message'])

    def add_version(self, project, version, egg):
        """
        为项目添加版本，如果项目不存在则创建项目。
        
        Args:
            project (str): 项目名称
            version (str): 版本名称
            egg (file-like object): 包含项目代码的Python egg文件
        
        Returns:
            HTTP响应对象，包含添加版本的结果
        
        """
       

        options = {
            'path': '/addversion.json',
            'data': {
                'project': project,
                'version': version
            },
            'files': {'egg': egg}
        }

        return self.post(**options)

    def cancel(self, project, job):
        """
        取消蜘蛛运行（即作业）。
        
        Args:
            project (str): 项目名称
            job (str): 作业ID
        
        Returns:
            None
        
        如果作业正在等待，则将其删除。
        如果作业正在运行，则将其终止。
        """
        
        options = {
            'path': '/cancel.json',
            'data': {
                'project': project,
                'job': job
            }
        }
        self.post(**options)

    def delete_project(self, project):
        """
        删除项目的所有版本。
        
        Args:
            project (str): 要删除的项目名称。
        
        Returns:
            response: 删除项目的响应结果。
        
        说明:
            删除一个项目的所有版本。这是Scrapyd的delete project端点的映射。
        """
        
        options = {
            'path': '/delproject.json',
            'data': {
                'project': project
            },

        }
        return self.post(**options)

    def delete_version(self, project, version):
        """
        删除项目的特定版本。
        
        Args:
            project (str): 项目名称。
            version (str): 要删除的版本号。
        
        Returns:
            response: HTTP响应对象，包含删除操作的结果。
        
        Notes:
            映射到Scrapyd的删除版本接口。
        """
       
        options = {
            'path': '/delversion.json',
            'data': {
                'project': project,
                'version': version
            },
        }
        return self.post(**options)

    def list_jobs(self, project):
        """
        获取指定项目的待处理、正在运行和已完成作业列表。
        
        Args:
            project (str): 项目名称
        
        Returns:
            dict: 包含待处理、正在运行和已完成作业信息的字典，具体结构如下：
            {
            "status": "ok",
            "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
            "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2",
                        "start_time": "2012-09-12 10:14:03.594664"}],
            "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3",
                        "start_time": "2012-09-12 10:14:03.594664",
                        "end_time": "2012-09-12 10:24:03.594664"}]
        }
        
        """
       
        options = {
            'path': '/listjobs.json',
            'params': {
                'project': project
            }
        }

        return self.get(**options)

    def list_projects(self):
        """
        获取上传到此Scrapy服务器的项目列表。
        
        Args:
            无
        
        Returns:
            dict: 包含项目列表的字典。格式如下：
            {"status": "ok", "projects": ["myproject", "otherproject"]}
        
        """
       
        options = {
            'path': '/listprojects.json'
        }

        return self.get(**options)

    def list_spiders(self, project, _version=None):
        """
        获取某个项目的最后一个版本（除非被覆盖）中可用的爬虫列表。
        
        Args:
            project (str): 项目名称
            _version (str, optional): 要检查的项目版本. Defaults to None.
        
        Returns:
            dict: 包含爬虫列表的响应体
        
        """
       
        options = {
            'path': '/listspiders.json',
            'params': {
                'project': project,
                '_version': _version
            }
        }

        return self.get(**options)

    def list_versions(self, project):
        """
        获取某个项目的可用版本列表。
        
        Args:
            project (str): 项目名称
        
        Returns:
            返回包含项目可用版本列表的字典，版本按顺序排列，最后一个为当前使用的版本。
        
        """
    
        options = {
            'path': '/listversions.json',
            'params': {
                'project': project
            }
        }

        return self.get(**options)

    def schedule(self, project, spider, setting=None, jobid=None, _version=None, **kwargs):
        """
        调度一个爬虫运行（也称为作业），返回作业ID。
        
        Args:
            project (str): 项目名称
            spider (str): 爬虫名称
            setting (dict, optional): 运行爬虫时要使用的Scrapy设置，例如: setting={'DOWNLOAD_DELAY': 2}。默认为None。
            jobid (str, optional): 用于标识作业的作业ID，覆盖默认的UUID。默认为None。
            _version (str, optional): 要使用的项目版本。默认为None。
            **kwargs: 任何其他参数都将作为爬虫参数传递。
        
        Returns:
            返回作业ID。
        
        """
       
        params = {
            'path': '/schedule.json',
            'data': {
                'project': project,
                'spider': spider,
                'setting': setting,
                'jobid': jobid,
                '_version': _version,
                **kwargs
            }

        }
        return self.post(**params)

    def daemon_status(self):
        """
        显示服务的负载状态。
        
        Args:
            无
        
        Returns:
            dict: 包含服务负载状态的字典。
        """
      
        params = {
            'path': '/daemonstatus.json'
        }
        return self.get(**params)


if __name__ == '__main__':
    api = ScrapydAPI()
    print(api.daemon_status())
    print(api.add_version(1, 2, 3))
