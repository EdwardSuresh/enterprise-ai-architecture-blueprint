"""Adapters are tested with stub clients, so CI needs no cloud credentials."""
import types

import pytest

from kit.gateway import ProviderError


def _ns(**kw):
    return types.SimpleNamespace(**kw)


def test_azure_adapter_maps_response():
    from kit_adapters.azure import AzureFoundryProvider
    p = AzureFoundryProvider.__new__(AzureFoundryProvider)
    resp = _ns(choices=[_ns(message=_ns(content="hi"))], usage=_ns(prompt_tokens=5, completion_tokens=2))
    p.client = _ns(chat=_ns(completions=_ns(create=lambda **kw: resp)))
    out = p.complete("q", "my-deployment")
    assert (out.text, out.input_tokens, out.output_tokens, out.provider) == ("hi", 5, 2, "azure")


def test_bedrock_adapter_maps_response():
    from kit_adapters.aws import BedrockProvider
    p = BedrockProvider.__new__(BedrockProvider)
    resp = {"output": {"message": {"content": [{"text": "hello"}]}}, "usage": {"inputTokens": 7, "outputTokens": 3}}
    p.client = _ns(converse=lambda **kw: resp)
    out = p.complete("q", "model-id")
    assert (out.text, out.input_tokens, out.output_tokens) == ("hello", 7, 3)


def test_vertex_adapter_maps_response():
    from kit_adapters.gcp import VertexProvider
    p = VertexProvider.__new__(VertexProvider)
    p._types = _ns(GenerateContentConfig=lambda **kw: kw)
    resp = _ns(text="yo", usage_metadata=_ns(prompt_token_count=4, candidates_token_count=1))
    p.client = _ns(models=_ns(generate_content=lambda **kw: resp))
    out = p.complete("q", "model")
    assert (out.text, out.input_tokens, out.output_tokens) == ("yo", 4, 1)


def test_anthropic_adapter_maps_response_and_errors():
    from kit_adapters.anthropic_api import AnthropicProvider
    p = AnthropicProvider.__new__(AnthropicProvider)
    resp = _ns(content=[_ns(type="text", text="ok")], usage=_ns(input_tokens=3, output_tokens=1))
    p.client = _ns(messages=_ns(create=lambda **kw: resp))
    assert p.complete("q", "m").text == "ok"

    def boom(**kw):
        raise RuntimeError("down")
    p.client = _ns(messages=_ns(create=boom))
    with pytest.raises(ProviderError):
        p.complete("q", "m")


def test_factory_rejects_unknown_cloud():
    from kit_adapters import get_provider
    with pytest.raises(ValueError):
        get_provider("mainframe")
