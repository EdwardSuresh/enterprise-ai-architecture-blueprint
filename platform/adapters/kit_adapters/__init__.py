"""Cloud adapters: the ONLY cloud-specific code in the kit.

Each adapter implements the kit.gateway.Provider contract:
    complete(prompt, model, max_tokens) -> kit.gateway.Completion

SDKs are imported lazily, so the core runs without them. Install one with
`pip install -e .[azure]`, `.[aws]`, `.[gcp]` or `.[anthropic]`.

These adapters are reference code. They are not exercised in CI because CI has
no cloud credentials; test them in your own sandbox (see labs/01-llm-gateway).
"""
from .factory import get_provider

__all__ = ["get_provider"]
