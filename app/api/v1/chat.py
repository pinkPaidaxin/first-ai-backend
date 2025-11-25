from fastapi import APIRouter
from typing import List
from app.models.schemas import ChatRequest, ChatResponse, CharacterInfo, Response
from app.services.chat_service import chat_service

router = APIRouter()


@router.get("/characters", response_model=Response[List[CharacterInfo]])
async def get_characters():
    """获取所有可用角色"""
    characters = chat_service.get_available_characters()

    return {
        "code": 0,
        "message": "success",
        "data": {
            "characters": characters,
            "total": len(characters)
        }
    }


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """主要聊天端点"""
    result = await chat_service.chat(
        user_id=request.user_id,
        user_message=request.message,
        character_type=request.character_type
    )
    return ChatResponse(**result)


@router.delete("/conversation/{user_id}")
async def clear_conversation(user_id: str):
    if user_id in chat_service.conversation_histories:
        del chat_service.conversation_histories[user_id]
        return {"message": f"用户 {user_id} 的对话历史已清空"}
    return {"message": "用户对话历史不存在"}
