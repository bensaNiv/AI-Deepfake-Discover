# Prompt Book

## AI Interactions During Development

This document records the prompts and AI interactions used during the development of the Video Fraud Detection Agent.

---

## 1. Project Definition Prompt

### Initial Project Prompt

```
The project is an experiment: I create an agent that his specialty is that
he is a security expert that investigates video frauds. The experiment goes
like that: I will take the agent (that you will write) give him a video -
and he will need to tell me if it was made by AI or not.
```

### Key Requirements Extracted

1. Agent with security expert persona
2. Video analysis capability
3. Binary classification: AI-generated vs authentic
4. Experimental validation approach

---

## 2. Agent System Prompt

### Version 1.0 (Current)

```
You are a senior security expert specializing in digital forensics
and video fraud investigation. Your expertise includes:

- Detecting AI-generated video content (deepfakes, synthetic media)
- Analyzing visual artifacts and inconsistencies
- Identifying manipulation patterns in video frames
- Assessing authenticity of digital media

When analyzing a video or video frame, you should look for:

1. FACIAL ANALYSIS:
   - Unnatural facial movements or expressions
   - Inconsistent lighting on face vs background
   - Blurring around face edges or hair
   - Eye blinking patterns (too regular or absent)
   - Teeth and mouth rendering issues

2. TEMPORAL CONSISTENCY:
   - Flickering or morphing between frames
   - Inconsistent shadows across time
   - Unnatural motion blur
   - Audio-visual sync issues

3. TECHNICAL ARTIFACTS:
   - Compression artifacts in unusual places
   - Resolution inconsistencies
   - Color banding or unusual gradients
   - Edge artifacts around subjects

4. CONTEXTUAL ANALYSIS:
   - Background consistency
   - Lighting direction consistency
   - Reflection accuracy
   - Physics of movement (hair, clothing, objects)

Provide your analysis in a structured format with:
- Overall verdict (AI_GENERATED, AUTHENTIC, or UNCERTAIN)
- Confidence level (0-100%)
- Detailed reasoning
- Specific indicators found
- Recommendations for further investigation

Be thorough but acknowledge limitations when image quality or context
is insufficient.
```

### Design Rationale

| Element | Purpose |
|---------|---------|
| "Senior security expert" | Establishes authoritative persona |
| Four analysis categories | Ensures comprehensive coverage |
| Structured output format | Enables parsing and aggregation |
| Uncertainty acknowledgment | Prevents overconfident predictions |

---

## 3. Analysis Request Prompt

### Frame Analysis Template

```
Analyze this video frame ({context}) for signs of AI generation.

Provide your analysis in the following JSON format:
{
    "verdict": "AI_GENERATED" | "AUTHENTIC" | "UNCERTAIN",
    "confidence": 0-100,
    "reasoning": "detailed explanation",
    "indicators": ["indicator1", "indicator2", ...],
    "recommendations": ["recommendation1", ...]
}
```

### Evolution Notes

- **v1.0**: Initial JSON-based output format
- JSON structure chosen for reliable parsing
- Context parameter added for frame identification

---

## 4. Development Assistance Prompts

### 4.1 Architecture Design

```
Help me design a Python agent architecture for video fraud detection:
- Should support multiple LLM providers (Ollama, OpenAI, Anthropic)
- Need to extract frames from video files
- Must aggregate multiple frame analyses
- CLI interface for command-line usage
```

### 4.2 Test Generation

```
Generate pytest test cases for the VideoFraudDetectionAgent class:
- Test frame analysis with mocked LLM responses
- Test video analysis with frame extraction
- Test error handling for missing files
- Test response parsing for various formats
```

### 4.3 Documentation

```
Create comprehensive documentation for a video fraud detection agent:
- README with installation and usage
- Architecture documentation with component diagrams
- Experiment results analysis
```

---

## 5. Prompt Iteration History

### Iteration 1: Basic Detection

**Prompt**: "Is this image AI generated?"

**Issue**: Too simple, inconsistent output format

### Iteration 2: Expert Persona

**Prompt**: "As a security expert, analyze this image for deepfake indicators"

**Issue**: Output format varied, hard to parse

### Iteration 3: Structured Output (Current)

**Prompt**: Full system prompt with JSON output specification

**Result**: Consistent, parseable results with detailed analysis

---

## 6. Future Prompt Improvements

### Planned Enhancements

1. **Chain-of-Thought**: Add step-by-step reasoning requirements
2. **Few-Shot Examples**: Include authentic/AI examples in prompt
3. **Confidence Calibration**: Add instructions for confidence scoring
4. **Compression Awareness**: Explicitly address compression artifacts

### Example Future Prompt Addition

```
IMPORTANT: Video compression can create artifacts similar to AI generation.
Before concluding a video is AI-generated, consider:
- Is the artifact consistent with standard video codecs (H.264, H.265)?
- Does the artifact appear in areas of high motion (normal) or static (suspicious)?
- Are artifacts present throughout or only in specific frames?
```

---

## 7. Lessons Learned

### What Worked

1. **Expert persona** increases analysis depth
2. **Structured categories** ensure comprehensive coverage
3. **JSON output** enables reliable parsing
4. **Uncertainty option** reduces false confidence

### What Needs Improvement

1. **Compression artifacts** confused with AI artifacts
2. **High confidence** doesn't correlate with accuracy
3. **Motion blur** misinterpreted as morphing

### Recommended Changes

1. Add explicit compression artifact guidance
2. Implement confidence calibration
3. Increase frame sampling for motion-heavy videos
