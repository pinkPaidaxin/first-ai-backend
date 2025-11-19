# app/core/config.py
from typing import Dict
from pydantic import Field
from pydantic_settings import BaseSettings


class ProviderConfig(BaseSettings):
    api_key: str
    base_url: str
    model_name: str


class Settings(BaseSettings):
    env: str = Field(default="dev", description="当前环境：dev 或 prod")

    # 嵌套配置，自动读取带前缀的环境变量
    deepseek_v31_api_key: str = Field(..., alias="DEEPSEEK_V31_API_KEY")
    deepseek_v31_base_url: str = Field(..., alias="DEEPSEEK_V31_BASE_URL")
    deepseek_v31_model_name: str = Field(..., alias="DEEPSEEK_V31_MODEL_NAME")

    deepseek_r1_api_key: str = Field(..., alias="DEEPSEEK_R1_0528_QWEN3_8B_API_KEY")
    deepseek_r1_base_url: str = Field(..., alias="DEEPSEEK_R1_0528_QWEN3_8B_BASE_URL")
    deepseek_r1_model_name: str = Field(..., alias="DEEPSEEK_R1_0528_QWEN3_8B_MODEL_NAME")

    default_provider: str = Field(default="deepseek_R1_0528_Qwen3_8B", alias="DEFAULT_PROVIDER")
    # default_provider: str = 'deepseekR10528Qwen38B'

    # 添加角色配置
    character_profiles: Dict[str, Dict] = {
        "friendly": {
            "name": "小悠",
            "personality": "温柔又有点调皮的朋友",
            "description": "适合日常聊天和情感陪伴",
            "system_prompt": "你是一个温柔、善解人意的AI朋友，喜欢用轻松的语气陪伴用户。"
        },
        "wise": {
            "name": "知言",
            "personality": "睿智沉稳，擅长分析问题",
            "description": "适合深度对话和思考",
            "system_prompt": "你是一个睿智的AI顾问，善于倾听并提供有深度的建议。"
        }
    }

    def get_provider(self, name: str) -> ProviderConfig:
        if name == "deepseek_v31":
            return ProviderConfig(
                api_key=self.deepseek_v31_api_key,
                base_url=self.deepseek_v31_base_url,
                model_name=self.deepseek_v31_model_name
            )
        elif name == "deepseek_R1_0528_Qwen3_8B":
            return ProviderConfig(
                api_key=self.deepseek_r1_api_key,
                base_url=self.deepseek_r1_base_url,
                model_name=self.deepseek_r1_model_name
            )
        else:
            raise ValueError(f"未知 provider: {name}")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()
