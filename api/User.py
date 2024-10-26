

from fastapi import APIRouter, HTTPException
from utils import redis_client
from model.model import UserModel


UserRouter = APIRouter()


# 用户注册
@UserRouter.post("/register")
def register(user: UserModel):
    """
    用户注册。
    """
    key = f"user:{user.username}"
    
    # 检查是否已存在
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # 将用户信息存储到 Redis
    redis_client.hmset(key, {"username": user.username, "password": user.password})
    
    return {"message": "User registered successfully", "user": user.dict()}

# 用户登录
@UserRouter.post("/login")
def login(user: UserModel):
    """
    用户登录。
    """
    key = f"user:{user.username}"
    
    # 获取用户信息
    stored_user = redis_client.hgetall(key)
    
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}


# 删除用户
@UserRouter.delete("/delete_user")
def delete_user(user: UserModel):
    """
    删除用户。
    """
    key = f"user:{user.username}"
    result = redis_client.delete(key)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# 用户信息查询
@UserRouter.get("/get_user")
def get_user(username: str):
    """
    获取用户信息。
    """
    key = f"user:{username}"
    user = redis_client.hgetall(key)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in user.items()}


# 获取所有用户信息
@UserRouter.get("/get_users")
def get_users():
    """
    获取所有用户信息。
    """
    keys = redis_client.keys("user:*")
    users = []
    for key in keys:
        user = redis_client.hgetall(key)
        users.append({k.decode('utf-8'): v.decode('utf-8') for k, v in user.items()})
    return users