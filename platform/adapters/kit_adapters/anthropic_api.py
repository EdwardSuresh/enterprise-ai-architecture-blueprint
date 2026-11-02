"""Claude API adapter (Messages API). Claude is also offered through
Amazon Bedrock, Microsoft Foundry and Vertex AI; use those adapters to stay
inside one cloud. Set ANTHROPIC_API_KEY.
"""
from __future__ import annotations

from kit.gateway import Completion, ProviderError


class AnthropicProvider:
    name = "anthropic"

    def __init__(self):
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise ImportError("pip install -e .[anthropic]") from exc
        self.client = anthropic.Anthropic()

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion:
        try:
            r = self.client.messages.create(model=model, max_tokens=max_tokens,
                                            messages=[{"role": "user", "content": prompt}])
        except Exception as exc:
            raise ProviderError(f"anthropic: {exc}") from exc
        text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
        return Completion(text=text, input_tokens=r.usage.input_tokens,
                          output_tokens=r.usage.output_tokens, provider=self.name, model=model)
