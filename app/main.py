'''
Author: zhixin.wang
Date: 2025-11-13 11:10:07
LastEditors: zhixin.wang
'''
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.v1 import chat as v1_chat
from app.api.v1 import auth as v1_auth
from app.core.config import settings
from dotenv import load_dotenv
import traceback

# 创建FastAPI应用
app = FastAPI(
    title="AI伴侣API",
    description="一个个性化的AI对话伴侣",
    version="1.0.0"
)

# 添加CORS中间件（允许前端访问）
# 注意：中间件必须在路由之前添加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境要改成具体域名
    allow_credentials=False,  # 使用 "*" 时不能为 True，且 JWT 通过 header 发送，不需要 credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# 全局异常处理器，确保所有错误响应都包含 CORS 头
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器，确保错误响应也包含 CORS 头"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "detail": str(exc) if settings.env == "dev" else "内部服务器错误"
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证错误处理器"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "请求参数验证失败",
            "detail": exc.errors()
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
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
