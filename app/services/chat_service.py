'''
Author: zhixin.wang
Date: 2025-11-13 11:45:15
LastEditors: zhixin.wang
'''
from openai import AsyncOpenAI
from app.core.config import settings
from typing import Dict, List

provider = settings.get_provider(settings.default_provider)
# 初始化 OpenAI 客户端（用于 DeepSeek）
client = AsyncOpenAI(
    api_key=provider.api_key,
    base_url=provider.base_url

)
# print('provider.api_key', provider.api_key)


class ChatService:
    def __init__(self):
        self.conversation_histories: Dict[str, List[Dict]] = {}

    def initialize_character(self, user_id: str, character_type: str = "friendly"):
        if character_type not in settings.character_profiles:
            character_type = "friendly"

        character = settings.character_profiles[character_type]

        self.conversation_histories[user_id] = [
            {"role": "system", "content": character["system_prompt"]},
            {"role": "assistant",
             "content": f"你好！我是{character['name']}，{character['personality']}。很高兴认识你！今天想聊点什么？"}
        ]

        return character

    async def chat(self, user_id: str, user_message: str, character_type: str = "friendly") -> Dict:
        if user_id not in self.conversation_histories:
            character = self.initialize_character(user_id, character_type)
        else:
            character = settings.character_profiles.get(character_type, settings.character_profiles["friendly"])

        self.conversation_histories[user_id].append({
            "role": "user",
            "content": user_message
        })

        try:
            # 使用新版 OpenAI SDK 调用 DeepSeek 接口
            response = await client.chat.completions.create(
                model=provider.model_name,
                messages=self.conversation_histories[user_id],
                temperature=0.8,
                max_tokens=300
            )

            ai_reply = response.choices[0].message.content

            self.conversation_histories[user_id].append({
                "role": "assistant",
                "content": ai_reply
            })

            if len(self.conversation_histories[user_id]) > 12:
                self.conversation_histories[user_id] = [
                                                           self.conversation_histories[user_id][0]
                                                       ] + self.conversation_histories[user_id][-10:]

            return {
                "reply": ai_reply,
                "character_name": character["name"],
                "user_message": user_message
            }

        except Exception as e:
            return {
                "reply": f"抱歉，我遇到了一些问题：{str(e)}",
                "character_name": character["name"],
                "user_message": user_message
            }

    @staticmethod
    def get_available_characters():
        return settings.character_profiles


chat_service = ChatService()
