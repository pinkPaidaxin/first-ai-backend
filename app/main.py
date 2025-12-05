'''
Author: zhixin.wang
Date: 2025-11-13 11:10:07
LastEditors: zhixin.wang
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat as v1_chat
from app.api.v1 import auth as v1_auth
from dotenv import load_dotenv

# 创建FastAPI应用
app = FastAPI(
    title="AI伴侣API",
    description="一个个性化的AI对话伴侣",
    version="1.0.0"
)

# 添加CORS中间件（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境要改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "code": 0,
        "message": "欢迎使用AI伴侣API！",
        "available_endpoints": {
            "文档": "/docs",
            "获取角色列表": "/characters",
            "对话": "/chat"
        }
    }


app.include_router(v1_chat.router, prefix="/v1")
app.include_router(v1_auth.router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
