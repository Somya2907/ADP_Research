"""SDK clients for Anthropic (Claude Opus 4.6) and OpenAI (GPT-5).

Deliberately thin — no LangChain or LlamaIndex. We want to see exactly what
goes into and comes out of each API call because prompt iteration on the
F-I-R-A-C-O schema will require that visibility.

Both clients cache responses via diskcache so repeated calls with identical
inputs (during prompt development) don't burn API budget.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from anthropic import Anthropic
from openai import OpenAI

from .cache import cached_call


@dataclass
class LLMResponse:
    """Uniform response wrapper across providers."""
    text: str
    model: str
    input_tokens: int
    output_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class TeacherClient:
    """Claude Opus 4.6 (teacher / reference model) via Anthropic SDK."""

    def __init__(self, model: str | None = None):
        self.client = Anthropic()
        self.model = model or os.environ.get("TEACHER_MODEL", "claude-opus-4-6")

    @cached_call(namespace="teacher")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 8192,
        temperature: float = 0.0,
    ) -> LLMResponse:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in resp.content if b.type == "text")
        return LLMResponse(
            text=text,
            model=self.model,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
        )


class AgentClient:
    """GPT-5 (agent / model under evaluation) via OpenAI SDK."""

    def __init__(self, model: str | None = None):
        self.client = OpenAI()
        self.model = model or os.environ.get("AGENT_MODEL", "gpt-5")

    @cached_call(namespace="agent")
    def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 8192,
        temperature: float = 0.0,
    ) -> LLMResponse:
        resp = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        usage = resp.usage
        return LLMResponse(
            text=resp.choices[0].message.content or "",
            model=self.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )
