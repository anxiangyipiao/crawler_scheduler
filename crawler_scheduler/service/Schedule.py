from itertools import cycle
from apscheduler.schedulers.background import BackgroundScheduler
from scrapyd_api import ScrapydAPI
from utils import redis_client
import requests


# 轮询调度器，用于轮询 Scrapyd 客户端
class RoundRobinScrapydScheduler:
    def __init__(self):
        self.scrapyd_clients = []
        self.client_pool = None  # 轮询池初始化为空

    def update_clients_from_redis(self):
        """从 Redis 更新 Scrapyd 客户端列表"""
        clients = []
        keys = redis_client.keys("scrapyd_client:*")
        for key in keys:
            data = redis_client.hgetall(key)
            url = data.get("url").decode('utf-8')
            port = data.get("port").decode('utf-8')
            full_url = f"http://{url}:{port}"
            clients.append(ScrapydAPI(full_url))
        
        # 更新客户端列表和轮询池
        self.scrapyd_clients = clients
        self.client_pool = cycle(self.scrapyd_clients)

    def is_client_busy(self, client: ScrapydAPI) -> bool:
        """检查 Scrapyd 客户端是否繁忙"""
        try:
            response = requests.get(f"{client.target}/daemonstatus.json")
            if response.status_code == 200:
                status = response.json()
                active_jobs = status.get("running", 0) + status.get("pending", 0)
                # 设置一个最大任务数的阈值，比如10，超过则认为繁忙
                return active_jobs > 10
        except requests.RequestException:
            # 请求失败视为繁忙
            return True
        return False

    def get_next_client(self) -> ScrapydAPI:
        """获取下一个不繁忙的 Scrapyd 客户端"""
        if self.client_pool is None:
            self.update_clients_from_redis()

        for _ in range(len(self.scrapyd_clients)):
            client = next(self.client_pool)
            if not self.is_client_busy(client):
                return client

        raise RuntimeError("所有 Scrapyd 客户端都繁忙")

# 实例化调度器
scrapyd_scheduler = RoundRobinScrapydScheduler()
scheduler = BackgroundScheduler()
scheduler.add_job(scrapyd_scheduler.update_clients_from_redis, 'interval', minutes=1)  # 每隔1分钟更新
scheduler.start()
