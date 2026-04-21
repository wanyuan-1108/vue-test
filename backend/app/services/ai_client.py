import json
import os
import re
from pathlib import Path
from typing import Optional, Type

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

from app.core.config import get_settings


load_dotenv(Path(__file__).resolve().parents[2] / '.env')


class AIClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def api_key(self) -> str:
        return os.getenv("DASHSCAPE_API_KEY", "").strip()

    @property
    def has_credentials(self) -> bool:
        return bool(self.api_key)

    def assert_ready(self) -> None:
        if not self.has_credentials:
            raise ValueError(
                "未检测到阿里云百炼 API Key。请在 backend/.env 中填写 DASHSCAPE_API_KEY，然后重启后端服务。"
            )

    def _chat(self, *, system_prompt: str, user_prompt: str) -> str:
        self.assert_ready()
        try:
            response = requests.post(
                f"{self.settings.dashscape_base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.settings.dashscape_model,
                    "temperature": self.settings.dashscape_temperature,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
                timeout=self.settings.dashscape_timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise ValueError(
                f"调用阿里云百炼接口超时（>{self.settings.dashscape_timeout} 秒）。请检查本机网络是否能访问 dashscope.aliyuncs.com，或在 backend/.env 中增大 DASHSCAPE_TIMEOUT。"
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ValueError(
                f"调用阿里云百炼接口失败：{exc}。请检查网络、代理设置和 DASHSCAPE_BASE_URL。"
            ) from exc
        response.raise_for_status()
        payload = response.json()

        if payload.get("error"):
            raise ValueError(f"阿里云百炼接口调用失败：{payload}")

        choices = payload.get("choices") or []
        if not choices:
            raise ValueError(f"阿里云百炼返回内容为空：{payload}")

        message = choices[0].get("message") or {}
        content = message.get("content")

        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content = "\n".join(part for part in text_parts if part)

        if not isinstance(content, str) or not content.strip():
            raise ValueError(f"阿里云百炼返回 message.content 为空：{payload}")

        return content.strip()

    def _extract_json_text(self, text: str) -> str:
        fenced = re.findall(r"```json\s*(.*?)\s*```", text, flags=re.S | re.I)
        if fenced:
            return fenced[0].strip()

        fenced_generic = re.findall(r"```\s*(.*?)\s*```", text, flags=re.S)
        if fenced_generic:
            candidate = fenced_generic[0].strip()
            if candidate.startswith("{") and candidate.endswith("}"):
                return candidate

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]

        raise ValueError(f"未能从模型返回中提取 JSON：{text}")

    def structured_json(self, *, system_prompt: str, user_prompt: str, schema: Type[BaseModel]) -> Optional[BaseModel]:
        schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False, indent=2)
        prompt = (
            f"{user_prompt}\n\n"
            "请严格输出 JSON，不要输出解释，不要输出 Markdown。\n"
            f"必须符合以下 JSON Schema：\n{schema_json}"
        )
        raw_text = self._chat(system_prompt=system_prompt, user_prompt=prompt)
        json_text = self._extract_json_text(raw_text)
        return schema.model_validate_json(json_text)

    def text(self, *, system_prompt: str, user_prompt: str) -> Optional[str]:
        return self._chat(system_prompt=system_prompt, user_prompt=user_prompt)
