# ADR-001: Local LLM Inference with Ollama

## Status

Accepted

## Context

The Video Fraud Detection Agent requires a vision-capable language model to analyze video frames for AI-generation indicators. We needed to decide between:

1. **Cloud APIs** (OpenAI GPT-4V, Anthropic Claude, Google Gemini)
   - Higher quality models
   - Pay-per-use pricing
   - Requires internet connection
   - Data leaves local machine

2. **Local Inference** (Ollama with LLaVA)
   - Open-source models
   - Zero API costs
   - Works offline
   - Data stays local

### Considerations

- **Cost**: This is an experimental/academic project with limited budget
- **Privacy**: Video content may be sensitive and shouldn't leave the machine
- **Reproducibility**: Results should be reproducible without API access
- **Quality**: Detection accuracy is important but not production-critical

## Decision

We will use **Ollama with LLaVA** as the primary inference backend for the following reasons:

1. **Zero Cost**: Unlimited experiments without API charges
2. **Privacy**: Video frames never leave the local machine
3. **Reproducibility**: Anyone can run the same model locally
4. **Simplicity**: Single dependency (Ollama) with simple HTTP API

The architecture supports future cloud providers through the provider abstraction in `providers.py`, but Ollama is the recommended default.

### Implementation

```python
# providers.py - Ollama implementation
def query_ollama(model_name: str, image_data: str, context: str) -> str:
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    response = requests.post(f"{ollama_host}/api/generate", ...)
    return response.json().get("response", "")
```

## Consequences

### Positive

- **No API costs**: Experiment freely without budget concerns
- **Privacy preserved**: Sensitive video content stays local
- **Offline capable**: Works without internet after model download
- **Fast iteration**: No rate limits or API quotas
- **Reproducible**: Same model version produces consistent results

### Negative

- **Lower quality**: LLaVA may be less capable than GPT-4V or Claude
- **Hardware requirements**: Requires GPU with 8GB+ VRAM for comfortable inference
- **Setup complexity**: Users must install Ollama and download models
- **Slower inference**: Local GPU typically slower than cloud infrastructure

### Neutral

- Cloud providers can be added later through the existing abstraction
- Quality comparison between local and cloud models could be future research
