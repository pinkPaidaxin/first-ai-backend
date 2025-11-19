from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    user_id: str
    character_type: str = "friendly"


class ChatResponse(BaseModel):
    reply: str
    character_name: str
    user_message: str


class CharacterInfo(BaseModel):
    name: str
    personality: str
    description: str
