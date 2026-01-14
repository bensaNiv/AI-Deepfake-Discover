"""LLM Provider implementations for Video Fraud Detection Agent.

This module contains provider-specific implementations for
querying vision-capable language models.
"""

import os

from .prompts import ANALYSIS_PROMPT_TEMPLATE, SYSTEM_PROMPT


def query_ollama(model_name: str, image_data: str, context: str) -> str:
    """Query Ollama with vision model.

    Args:
        model_name: Name of the Ollama model to use
        image_data: Base64 encoded image
        context: Additional context for the analysis

    Returns:
        Model response text
    """
    import requests

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(context=context)

    response = requests.post(
        f"{ollama_host}/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "images": [image_data],
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json().get("response", "")


def query_openai(model_name: str, image_data: str, context: str) -> str:
    """Query OpenAI with vision model.

    Args:
        model_name: Name of the OpenAI model to use
        image_data: Base64 encoded image
        context: Additional context for the analysis

    Returns:
        Model response text

    Raises:
        NotImplementedError: OpenAI provider not yet implemented
    """
    raise NotImplementedError(
        "OpenAI provider not yet implemented. "
        "Set OPENAI_API_KEY and implement using openai library."
    )


def query_anthropic(model_name: str, image_data: str, context: str) -> str:
    """Query Anthropic with vision model.

    Args:
        model_name: Name of the Anthropic model to use
        image_data: Base64 encoded image
        context: Additional context for the analysis

    Returns:
        Model response text

    Raises:
        NotImplementedError: Anthropic provider not yet implemented
    """
    raise NotImplementedError(
        "Anthropic provider not yet implemented. "
        "Set ANTHROPIC_API_KEY and implement using anthropic library."
    )
