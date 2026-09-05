import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.api_key = (
            api_key
            or os.getenv("LLM_API_KEY")
        )

        self.base_url = (
            base_url
            or os.getenv("LLM_BASE_URL")
        )

        self.model = (
            model
            or os.getenv("LLM_MODEL")
        )

        if not self.api_key:
            raise ValueError(
                "LLM_API_KEY is not configured"
            )

        if not self.model:
            raise ValueError(
                "LLM_MODEL is not configured"
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate(
        self,
        prompt: str | list[dict[str, Any]],
        max_retries: int = 3,
    ) -> str:

        if isinstance(prompt, str):
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        else:
            messages = prompt

        for attempt in range(max_retries):

            response = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
            )

            choice = response.choices[0]
            content = choice.message.content

            if content and content.strip():
                return content.strip()

            print(
                f"[LLMClient] Empty response "
                f"(attempt {attempt + 1}/{max_retries}, "
                f"finish_reason={choice.finish_reason})"
            )

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

        raise ValueError(
            f"LLM returned empty content "
            f"after {max_retries} attempts"
        )