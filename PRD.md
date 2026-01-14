# Product Requirements Document (PRD)

## Project: AI Video Fraud Detection Agent

### Version: 1.0
### Date: January 2026

---

## 1. Executive Summary

This project implements an AI-powered agent specialized in detecting AI-generated video content (deepfakes, synthetic media). The agent analyzes video frames using vision-capable language models to identify artifacts and inconsistencies characteristic of AI-generated content.

---

## 2. Problem Statement

### 2.1 User Problem

With the proliferation of AI-generated video content (deepfakes), there is a critical need for automated tools that can:
- Detect synthetic media in video content
- Provide detailed analysis of detection indicators
- Support security analysts in fraud investigations

### 2.2 Target Users

- Security analysts investigating fraud cases
- Content moderators reviewing uploaded media
- Researchers studying AI-generated content detection
- Digital forensics professionals

---

## 3. Functional Requirements

### 3.1 Core Features

| ID | Feature | Priority | Description |
|----|---------|----------|-------------|
| FR-01 | Video Analysis | High | Analyze video files for AI generation indicators |
| FR-02 | Frame Analysis | High | Analyze individual frames/images |
| FR-03 | Multi-frame Aggregation | High | Combine multiple frame analyses into single verdict |
| FR-04 | Confidence Scoring | High | Provide confidence percentage for verdicts |
| FR-05 | Indicator Reporting | Medium | List specific indicators found |
| FR-06 | JSON Output | Medium | Support structured JSON output format |
| FR-07 | CLI Interface | Medium | Command-line interface for batch processing |

### 3.2 Analysis Categories

The agent analyzes content across four main categories:

1. **Facial Analysis**
   - Unnatural movements/expressions
   - Lighting inconsistencies
   - Edge blurring around faces
   - Eye blinking patterns
   - Teeth/mouth rendering

2. **Temporal Consistency**
   - Inter-frame flickering
   - Shadow consistency
   - Motion blur patterns
   - Audio-visual sync

3. **Technical Artifacts**
   - Compression anomalies
   - Resolution inconsistencies
   - Color banding
   - Edge artifacts

4. **Contextual Analysis**
   - Background consistency
   - Lighting direction
   - Reflection accuracy
   - Physics simulation

---

## 4. Non-Functional Requirements

### 4.1 Performance

| Metric | Requirement |
|--------|-------------|
| Frame analysis time | < 30 seconds per frame |
| Video processing | < 3 minutes for 5-frame sample |
| Memory usage | < 2GB RAM |

### 4.2 Reliability

- Graceful handling of corrupted video files
- Fallback parsing for non-JSON LLM responses
- Automatic cleanup of temporary files

### 4.3 Extensibility

- Support multiple LLM providers (Ollama, OpenAI, Anthropic)
- Configurable frame sampling count
- Pluggable model selection

---

## 5. Success Metrics / KPIs

Based on experiment results with 5-video test dataset:

| Metric | Target | Achieved |
|--------|--------|----------|
| Accuracy | > 75% | 80% |
| Precision | > 70% | 75% |
| Recall | > 90% | 100% |
| F1 Score | > 0.80 | 0.857 |

### 5.1 Key Observations

- **High Recall**: Agent successfully identifies all AI-generated content
- **False Positive Risk**: Some authentic videos with motion artifacts may be flagged
- **Confidence Calibration**: High confidence does not always correlate with accuracy

---

## 6. Dependencies and Constraints

### 6.1 Technical Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| OpenCV | 4.x | Video frame extraction |
| Ollama | Latest | Local LLM inference |
| requests | 2.x | HTTP client |
| python-dotenv | 1.x | Environment management |

### 6.2 External Dependencies

- Vision-capable LLM (e.g., LLaVA via Ollama)
- Sufficient GPU memory for model inference (8GB+ recommended)

### 6.3 Constraints

- Analysis quality depends on LLM capabilities
- Video compression may introduce false indicators
- Real-time analysis not supported (batch processing only)

---

## 7. Out of Scope

- Real-time video stream analysis
- Audio deepfake detection
- Video editing/manipulation (detection only)
- Training custom detection models

---

## 8. Future Enhancements

1. **Confidence Calibration**: Improve correlation between confidence and accuracy
2. **Compression Awareness**: Better distinguish compression artifacts from AI artifacts
3. **Multi-provider Support**: Implement OpenAI and Anthropic providers
4. **Batch Processing**: Add support for processing video directories
5. **Report Generation**: Export detailed HTML/PDF analysis reports

---

## 9. Acceptance Criteria

- [ ] Agent can analyze video files and return structured verdicts
- [ ] Agent can analyze individual images
- [ ] Results include confidence scores and indicator lists
- [ ] CLI supports all documented options
- [ ] Test coverage > 70%
- [ ] Documentation complete
