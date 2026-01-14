# Cost Analysis

## Overview

This project uses **Ollama** with locally-hosted vision models, which means **zero API costs** for all experiments. All LLM inference runs on local hardware.

## Cost Breakdown

### API/Service Costs

| Service | Usage | Cost per Unit | Total Cost |
|---------|-------|---------------|------------|
| Ollama (local) | 25+ frame analyses | $0.00 | **$0.00** |
| OpenAI API | Not used | N/A | $0.00 |
| Anthropic API | Not used | N/A | $0.00 |
| Google Gemini | Not used | N/A | $0.00 |

### Hardware Costs (Existing Equipment)

| Resource | Description | Estimated Value |
|----------|-------------|-----------------|
| GPU | Local GPU for vision model inference | (existing hardware) |
| CPU | For Ollama serving | (existing hardware) |
| Storage | Model weights (~4-8GB for llava) | (existing storage) |

### Development Time

| Activity | Estimated Hours |
|----------|-----------------|
| Agent implementation | 2-3 hours |
| Prompt engineering | 1-2 hours |
| Video collection | 1-2 hours |
| Running experiments | 1-2 hours |
| Analysis & visualization | 1-2 hours |
| Documentation | 1-2 hours |
| **Total** | **7-13 hours** |

## Model Selection Rationale

### Chosen Model: `llava`

**Why this model:**
- Vision-capable (can analyze images and video frames)
- Good quality for artifact detection
- Runs locally with Ollama
- Open source, no API costs
- Reasonable inference time (~10-30 seconds per frame)

**Alternatives considered:**
- `llava:13b` - Better quality but requires more VRAM
- `bakllava` - Alternative vision model
- GPT-4V - Better quality but expensive ($0.01-0.03 per image)
- Claude Vision - Good quality but requires API costs

## Cost Optimization Strategies

### 1. Local Model Hosting
Running Ollama locally eliminates all API costs, making it possible to run unlimited analyses without budget concerns.

### 2. Frame Sampling
Instead of analyzing every frame, we sample 5-10 frames evenly distributed across the video, reducing inference time while maintaining accuracy.

### 3. Result Caching
Results are saved to JSON files, allowing re-analysis without re-running expensive LLM calls.

### 4. Batch Processing
Videos can be processed in batches with results saved incrementally.

## Budget Summary

| Category | Planned | Actual |
|----------|---------|--------|
| API Costs | $0 | $0 |
| Cloud Compute | $0 | $0 |
| **Total** | **$0** | **$0** |

## Cloud Cost Estimates

If this experiment were run using cloud APIs instead of local Ollama:

| Provider | Cost per Image | 5 Videos × 5 Frames | Total |
|----------|----------------|---------------------|-------|
| GPT-4V | ~$0.02 | 25 images | ~$0.50 |
| Claude Vision | ~$0.02 | 25 images | ~$0.50 |
| Gemini Pro Vision | ~$0.001 | 25 images | ~$0.03 |

## Notes

- This project was designed to be cost-free by using local inference
- For production deployment with higher throughput, consider cloud APIs
- Local inference provides privacy benefits - videos never leave your machine
- GPU with 8GB+ VRAM recommended for comfortable llava inference
