from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Dict
from pydantic.generics import GenericModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


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


class CharacterData(BaseModel):
    characters: Dict[str, CharacterInfo]
    total: int
