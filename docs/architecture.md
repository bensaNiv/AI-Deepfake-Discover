# Architecture Documentation

## System Overview

The Video Fraud Detection Agent is a Python application that analyzes video content to detect AI-generated media. It uses vision-capable language models to examine video frames and provide verdicts on content authenticity.

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│                    (CLI - main.py)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VideoFraudDetectionAgent                        │
│                      (agent.py)                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐│
│  │ Frame       │  │ Video        │  │ Result                  ││
│  │ Analysis    │  │ Analysis     │  │ Aggregation             ││
│  └─────────────┘  └──────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
         │                  │                      │
         ▼                  ▼                      ▼
┌──────────────┐  ┌─────────────────┐  ┌─────────────────────────┐
│   Providers  │  │  Video Utils    │  │      Parsing            │
│ (providers.py)│ │ (video_utils.py)│  │    (parsing.py)         │
└──────────────┘  └─────────────────┘  └─────────────────────────┘
         │                  │
         ▼                  ▼
┌──────────────┐  ┌─────────────────┐
│   Ollama     │  │    OpenCV       │
│   (LLM)      │  │ (Frame Extract) │
└──────────────┘  └─────────────────┘
```

---

## Components

### 1. User Interface (main.py)

**Responsibility**: Command-line interface for user interaction

**Features**:
- Parse command-line arguments
- Initialize agent with configuration
- Display formatted results
- Support JSON output mode

**Dependencies**: agent.py, models.py

### 2. VideoFraudDetectionAgent (agent.py)

**Responsibility**: Core orchestration of video analysis

**Key Methods**:
- `analyze_frame()`: Analyze single image
- `analyze_video()`: Extract and analyze multiple frames
- `_query_llm()`: Route to appropriate provider
- `_load_image()`: Base64 encode images

**Dependencies**: providers.py, video_utils.py, parsing.py, models.py

### 3. Models (models.py)

**Responsibility**: Data structures for analysis

**Classes**:
- `Verdict`: Enum for classification results (AI_GENERATED, AUTHENTIC, UNCERTAIN)
- `AnalysisResult`: Dataclass containing verdict, confidence, reasoning, indicators

### 4. Providers (providers.py)

**Responsibility**: LLM provider implementations

**Functions**:
- `query_ollama()`: Query local Ollama instance
- `query_openai()`: Query OpenAI API (not implemented)
- `query_anthropic()`: Query Anthropic API (not implemented)

**External Dependencies**: Ollama server, requests library

### 5. Video Utilities (video_utils.py)

**Responsibility**: Video processing operations

**Functions**:
- `extract_frames()`: Extract evenly-distributed frames from video
- `cleanup_temp_files()`: Remove temporary frame files

**External Dependencies**: OpenCV (cv2)

### 6. Parsing (parsing.py)

**Responsibility**: Response parsing and result aggregation

**Functions**:
- `parse_llm_response()`: Extract JSON from LLM response
- `aggregate_results()`: Combine multiple frame results

### 7. Prompts (prompts.py)

**Responsibility**: Store prompt templates

**Constants**:
- `SYSTEM_PROMPT`: Agent persona and analysis instructions
- `ANALYSIS_PROMPT_TEMPLATE`: Per-frame analysis request

---

## Data Flow

### Video Analysis Flow

```
1. User runs: python -m src.main --video video.mp4 --frames 5

2. main.py:
   └── Parses arguments
   └── Creates VideoFraudDetectionAgent
   └── Calls agent.analyze_video()

3. agent.py (analyze_video):
   └── Calls video_utils.extract_frames()
       └── OpenCV opens video
       └── Calculates frame indices
       └── Extracts 5 frames to temp directory
       └── Returns frame paths

   └── For each frame:
       └── Calls self.analyze_frame()
           └── Loads image as base64
           └── Calls self._query_llm()
               └── Routes to providers.query_ollama()
                   └── Sends HTTP request to Ollama
                   └── Returns LLM response text
           └── Calls parsing.parse_llm_response()
               └── Extracts JSON from response
               └── Returns AnalysisResult

   └── Calls parsing.aggregate_results()
       └── Counts verdicts across frames
       └── Calculates average confidence
       └── Deduplicates indicators
       └── Returns final AnalysisResult

   └── Calls video_utils.cleanup_temp_files()

4. main.py:
   └── Formats and displays result
```

### Single Frame Analysis Flow

```
1. User runs: python -m src.main --image frame.jpg

2. main.py:
   └── Creates VideoFraudDetectionAgent
   └── Calls agent.analyze_frame()

3. agent.py (analyze_frame):
   └── Loads image as base64
   └── Calls providers.query_ollama()
   └── Calls parsing.parse_llm_response()
   └── Returns AnalysisResult

4. main.py:
   └── Displays result
```

---

## Technology Choices

### Python 3.10+

**Rationale**:
- Modern type hints with `|` union syntax
- Pattern matching support
- Wide ecosystem for ML/AI tooling

### OpenCV (cv2)

**Rationale**:
- Industry standard for video processing
- Efficient frame extraction
- Cross-platform compatibility

**Alternatives Considered**:
- FFmpeg: More powerful but harder to integrate
- MoviePy: Higher-level but slower

### Ollama

**Rationale**:
- Local inference (no API costs)
- Supports vision models (LLaVA)
- Simple HTTP API
- Privacy-preserving (data stays local)

**Alternatives Considered**:
- OpenAI GPT-4V: Higher quality but API costs
- Anthropic Claude: Better reasoning but API costs
- Local transformers: More complex setup

### Requests Library

**Rationale**:
- Simple HTTP client
- Well-documented
- Minimal dependencies

---

## Extensibility

### Adding New LLM Providers

1. Add query function to `providers.py`:

```python
def query_new_provider(model_name: str, image_data: str, context: str) -> str:
    # Implementation
    pass
```

2. Update `_query_llm()` in `agent.py`:

```python
elif self.model_provider == "new_provider":
    return query_new_provider(self.model_name, image_data, context)
```

3. Update CLI choices in `main.py`:

```python
choices=["ollama", "openai", "anthropic", "new_provider"]
```

### Modifying Analysis Prompts

Edit `prompts.py` to modify:
- System prompt for agent persona
- Analysis prompt template for output format

### Adding New Analysis Categories

1. Update `SYSTEM_PROMPT` in `prompts.py`
2. Update result aggregation logic if needed
3. Update documentation

---

## Error Handling

### File Errors
- `FileNotFoundError`: Raised for missing video/image files
- `ValueError`: Raised for unreadable or empty videos

### LLM Errors
- Network timeouts: Handled by requests library (120s timeout)
- Invalid responses: Fallback parsing returns UNCERTAIN verdict
- Provider errors: Specific error messages with recommendations

### Resource Management
- Temporary files: Always cleaned up in `finally` block
- Video handles: Released after frame extraction
