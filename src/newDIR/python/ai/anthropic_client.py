"""Anthropic client wrapper for Claude API."""

from typing import Optional

import anthropic
from anthropic import Anthropic

# Anthropic API endpoint: api.anthropic.com
ANTHROPIC_BASE_URL = "https://api.anthropic.com"


def create_client(api_key: Optional[str] = None) -> Anthropic:
    """Create Anthropic client for api.anthropic.com."""
    return anthropic.Anthropic(api_key=api_key)


class AnthropicClient:
    """Wrapper for Anthropic messages API using client.messages.create()."""

    def __init__(self, api_key: Optional[str] = None):
        self.client: Anthropic = anthropic.Anthropic(api_key=api_key)

    def create_message(
        self,
        prompt: str,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1024,
    ) -> str:
        """Send message to Claude via api.anthropic.com and return response."""
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text if response.content else ""
