from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

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
        "message": "欢迎使用AI伴侣API！",
        "available_endpoints": {
            "文档": "/docs",
            "获取角色列表": "/characters",
            "对话": "/chat"
        }
    }


@app.get("/characters")
async def get_characters():
    """获取所有可用角色"""
    characters = chat_service.get_available_characters()
    return {
        "characters": characters,
        "total": len(characters)
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """主要聊天端点"""
    result = await chat_service.chat(
        user_id=request.user_id,
        user_message=request.message,
        character_type=request.character_type
    )
    return ChatResponse(**result)


@app.delete("/conversation/{user_id}")
async def clear_conversation(user_id: str):
    """清空用户的对话历史"""
    if user_id in chat_service.conversation_histories:
        del chat_service.conversation_histories[user_id]
        return {"message": f"用户 {user_id} 的对话历史已清空"}
    return {"message": "用户对话历史不存在"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
