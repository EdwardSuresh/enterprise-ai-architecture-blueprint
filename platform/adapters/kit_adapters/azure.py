"""Microsoft Foundry / Azure OpenAI adapter (chat completions API).

Environment: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY (or use Entra ID
token auth in production), AZURE_OPENAI_API_VERSION.
`model` is your deployment name from config/models.yaml cloud_bindings.azure.
"""
from __future__ import annotations

import os

from kit.gateway import Completion, ProviderError


class AzureFoundryProvider:
    name = "azure"

    def __init__(self, endpoint: str | None = None, api_key: str | None = None, api_version: str | None = None):
        try:
            from openai import AzureOpenAI
        except ImportError as exc:  # pragma: no cover
            raise ImportError("pip install -e .[azure]") from exc
        self.client = AzureOpenAI(
            azure_endpoint=endpoint or os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=api_key or os.environ["AZURE_OPENAI_API_KEY"],
            api_version=api_version or os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion:
        try:
            # Note: reasoning (o-series) deployments reject max_tokens and expect
            # max_completion_tokens. Switch the argument for those deployments.
            r = self.client.chat.completions.create(
                model=model, max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:  # map SDK errors to the gateway's fallback signal
            raise ProviderError(f"azure: {exc}") from exc
        return Completion(text=r.choices[0].message.content or "",
                          input_tokens=r.usage.prompt_tokens, output_tokens=r.usage.completion_tokens,
                          provider=self.name, model=model)
