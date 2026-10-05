"""OpenAI client wrapper for chat completions and embeddings."""

from typing import Optional

import openai
from openai import OpenAI

# OpenAI API base: api.openai.com
OPENAI_BASE_URL = "https://api.openai.com/v1"

# Generative LLM gateway endpoint (OpenAI-compatible)
LLM_GATEWAY_STAGE_URL = "https://wmtllmgateway.stage.walmart.com/wmtllmgateway/v1/openai"


def create_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    """Create OpenAI client. Uses api.openai.com by default."""
    return openai.OpenAI(
        api_key=api_key,
        base_url=base_url or OPENAI_BASE_URL,
    )


class OpenAIClient:
    """Wrapper for OpenAI chat and embedding operations."""

    def __init__(self, api_key: Optional[str] = None):
        self.client: OpenAI = openai.OpenAI(api_key=api_key)

    def chat_completion(
        self,
        messages: list[dict],
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> str:
        """Generate chat completion using client.chat.completions.create()."""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    def create_embedding(self, text: str, model: str = "text-embedding-3-small") -> list[float]:
        """Create embedding vector using client.embeddings.create()."""
        response = self.client.embeddings.create(
            model=model,
            input=text,
        )
        return response.data[0].embedding
