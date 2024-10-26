from scrapyd_api import ScrapydClient 

# 初始化 Scrapyd 客户端，连接到 Scrapyd 服务
scrapyd = ScrapydClient('http://localhost:6800')

# 列出已部署的项目
projects = scrapyd.list_projects()

print(projects)

# # 列出指定项目的爬虫
# spiders = scrapyd.list_spiders(project='project')

# print(spiders)


# # 启动爬虫
# job_id = scrapyd.schedule('my_project', 'my_spider', some_arg='value')

# # 检查任务状态
# status = scrapyd.job_status('my_project', job_id)

# # 停止任务
# scrapyd.cancel('my_project', job_id)
