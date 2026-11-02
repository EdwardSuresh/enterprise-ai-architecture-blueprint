"""Google Vertex AI adapter (Google Gen AI SDK in Vertex mode).

Auth via Application Default Credentials. Set GOOGLE_CLOUD_PROJECT and
GOOGLE_CLOUD_LOCATION. `model` comes from cloud_bindings.gcp.
"""
from __future__ import annotations

import os

from kit.gateway import Completion, ProviderError


class VertexProvider:
    name = "gcp"

    def __init__(self, project: str | None = None, location: str | None = None):
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover
            raise ImportError("pip install -e .[gcp]") from exc
        self._types = types
        self.client = genai.Client(vertexai=True,
                                   project=project or os.environ["GOOGLE_CLOUD_PROJECT"],
                                   location=location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"))

    def complete(self, prompt: str, model: str, max_tokens: int = 512) -> Completion:
        try:
            r = self.client.models.generate_content(
                model=model, contents=prompt,
                config=self._types.GenerateContentConfig(max_output_tokens=max_tokens),
            )
        except Exception as exc:
            raise ProviderError(f"gcp: {exc}") from exc
        u = getattr(r, "usage_metadata", None)
        return Completion(text=r.text or "",
                          input_tokens=getattr(u, "prompt_token_count", 0) or 0,
                          output_tokens=getattr(u, "candidates_token_count", 0) or 0,
                          provider=self.name, model=model)
