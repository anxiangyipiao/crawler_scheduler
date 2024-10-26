# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 初始化数据库连接
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





# 定时任务模型
class cron_Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    spider_name = Column(String, index=True)
    cron_expression = Column(String)
    status = Column(String, default="scheduled")  # 任务状态，初始为 scheduled
    created_at = Column(DateTime, default=datetime.utcnow)

# 创建数据库表
Base.metadata.create_all(bind=engine)
