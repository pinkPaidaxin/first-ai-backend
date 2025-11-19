import openai
from config.settings import settings
from typing import Dict, List

# 设置OpenAI API Key
openai.api_key = settings.OPENAI_API_KEY


class ChatService:
    def __init__(self):
        # 在内存中存储对话历史（生产环境要用数据库）
        self.conversation_histories: Dict[str, List[Dict]] = {}

    def initialize_character(self, user_id: str, character_type: str = "friendly"):
        """为用户初始化角色对话历史"""
        if character_type not in settings.CHARACTER_PROFILES:
            character_type = "friendly"

        character = settings.CHARACTER_PROFILES[character_type]

        # 初始化系统消息和欢迎语
        self.conversation_histories[user_id] = [
            {"role": "system", "content": character["system_prompt"]},
            {"role": "assistant",
             "content": f"你好！我是{character['name']}，{character['personality']}。很高兴认识你！今天想聊点什么？"}
        ]

        return character

    async def chat(self, user_id: str, user_message: str, character_type: str = "friendly") -> Dict:
        """处理用户消息"""

        # 如果是新用户或切换角色，初始化
        if user_id not in self.conversation_histories:
            character = self.initialize_character(user_id, character_type)
        else:
            character = settings.CHARACTER_PROFILES.get(character_type, settings.CHARACTER_PROFILES["friendly"])

        # 添加用户消息到历史
        self.conversation_histories[user_id].append({
            "role": "user",
            "content": user_message
        })

        try:
            # 调用OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=self.conversation_histories[user_id],
                temperature=0.8,  # 创造性稍高
                max_tokens=300
            )

            ai_reply = response.choices[0].message["content"]

            # 添加AI回复到历史
            self.conversation_histories[user_id].append({
                "role": "assistant",
                "content": ai_reply
            })

            # 限制历史记录长度（避免token过多）
            if len(self.conversation_histories[user_id]) > 12:
                # 保留系统消息和最近10条对话
                self.conversation_histories[user_id] = [
                                                           self.conversation_histories[user_id][0]  # system prompt
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

    def get_available_characters(self):
        """获取可用的角色列表"""
        return settings.CHARACTER_PROFILES


# 创建全局服务实例
chat_service = ChatService()
