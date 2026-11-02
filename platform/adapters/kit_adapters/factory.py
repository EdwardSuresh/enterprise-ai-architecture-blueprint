from __future__ import annotations


def get_provider(cloud: str, **kwargs):
    """Return a Provider for 'azure', 'aws', 'gcp' or 'anthropic'."""
    if cloud == "azure":
        from .azure import AzureFoundryProvider
        return AzureFoundryProvider(**kwargs)
    if cloud == "aws":
        from .aws import BedrockProvider
        return BedrockProvider(**kwargs)
    if cloud == "gcp":
        from .gcp import VertexProvider
        return VertexProvider(**kwargs)
    if cloud == "anthropic":
        from .anthropic_api import AnthropicProvider
        return AnthropicProvider(**kwargs)
    raise ValueError(f"unknown cloud '{cloud}'")
