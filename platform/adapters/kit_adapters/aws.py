"""Amazon Bedrock adapter (Converse API).

Credentials come from the standard AWS chain (IAM role in production).
`model` is a Bedrock model ID or inference profile from cloud_bindings.aws.
"""
from __future__ import annotations

import os

from kit.gateway import Completion, ProviderError


class BedrockProvider:
    name = "aws"

    def __init__(self, region: str | None = None):
        try:
            import boto3
        except ImportError as exc:  # pragma: no cover
            raise ImportError("pip install -e .[aws]") from exc
        self.client = boto3.client("bedrock-runtime", region_name=region or os.environ.get("AWS_REGION", "us-east-1"))

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion:
        try:
            r = self.client.converse(
                modelId=model,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": max_tokens},
            )
        except Exception as exc:
            raise ProviderError(f"aws: {exc}") from exc
        text = "".join(part.get("text", "") for part in r["output"]["message"]["content"])
        u = r.get("usage", {})
        return Completion(text=text, input_tokens=u.get("inputTokens", 0),
                          output_tokens=u.get("outputTokens", 0), provider=self.name, model=model)
