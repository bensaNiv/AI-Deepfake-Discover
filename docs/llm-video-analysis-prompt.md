# Video Fraud Detection - LLM Analysis Prompt

Use this document to manually analyze videos/images for AI-generation detection using any vision-capable LLM (GPT-4V, Claude, Gemini, etc.).

---

## System Prompt

Copy and paste this as the system prompt or initial context:

```
You are a senior security expert specializing in digital forensics and video fraud investigation. Your expertise includes:

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

Be thorough but acknowledge limitations when image quality or context is insufficient.
```

---

## Analysis Request Prompt

After setting the system prompt, use this prompt when uploading an image/frame:

```
Analyze this video frame for signs of AI generation.

If the video has "Veo" watermark - ignore it - that dosent indicate - on both real and unreal videos has this water mark.

Provide your analysis in the following JSON format:
{
    "verdict": "AI_GENERATED" | "AUTHENTIC" | "UNCERTAIN",
    "confidence": 0-100,
    "reasoning": "detailed explanation",
    "indicators": ["indicator1", "indicator2", ...],
    "recommendations": ["recommendation1", ...]
}
```

---

## Required Response Format

The LLM MUST respond with a JSON object containing these exact fields:

```json
{
    "verdict": "AI_GENERATED | AUTHENTIC | UNCERTAIN",
    "confidence": <number between 0-100>,
    "reasoning": "<detailed explanation string>",
    "indicators": ["<indicator1>", "<indicator2>", ...],
    "recommendations": ["<recommendation1>", "<recommendation2>", ...]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | string | One of: `AI_GENERATED`, `AUTHENTIC`, or `UNCERTAIN` |
| `confidence` | number | Confidence level from 0 to 100 |
| `reasoning` | string | Detailed explanation of the analysis |
| `indicators` | array | List of specific signs/artifacts found |
| `recommendations` | array | Suggested next steps for investigation |

---

## Response Examples

### Example 1: AI-Generated Content Detected

```json
{
    "verdict": "AI_GENERATED",
    "confidence": 85,
    "reasoning": "Multiple indicators suggest this frame is AI-generated. The subject's face shows characteristic deepfake artifacts including unnatural smoothness around the hairline, inconsistent lighting between the face and neck, and subtle warping near the ear boundaries. The eye reflections do not match the apparent light source in the scene.",
    "indicators": [
        "Unnatural smoothness at hairline boundary",
        "Inconsistent lighting between face and neck",
        "Warping artifacts near ear boundaries",
        "Eye reflections inconsistent with scene lighting",
        "Slight color banding on skin tones"
    ],
    "recommendations": [
        "Analyze additional frames for temporal consistency",
        "Compare with known authentic footage of the subject",
        "Check audio track for sync issues",
        "Examine at higher resolution if available"
    ]
}
```

### Example 2: Authentic Content

```json
{
    "verdict": "AUTHENTIC",
    "confidence": 78,
    "reasoning": "The frame appears to be authentic footage. Lighting is consistent across all elements, facial features show natural variation and imperfections, and no obvious AI generation artifacts are present. The background elements maintain proper perspective and the subject's hair and clothing physics appear natural.",
    "indicators": [
        "Consistent lighting across face and background",
        "Natural skin texture with pores visible",
        "Proper perspective in background elements",
        "Natural hair movement and physics",
        "No edge artifacts or warping detected"
    ],
    "recommendations": [
        "Verify source metadata if available",
        "Cross-reference with other footage from same source",
        "Consider analyzing audio for additional verification"
    ]
}
```

### Example 3: Uncertain/Inconclusive

```json
{
    "verdict": "UNCERTAIN",
    "confidence": 45,
    "reasoning": "The image quality and compression artifacts make it difficult to definitively determine authenticity. Some areas show potential AI generation indicators, but these could also be attributed to heavy compression or poor camera quality. The face is partially obscured which limits facial analysis capabilities.",
    "indicators": [
        "Heavy compression artifacts throughout",
        "Possible smoothing around facial boundaries (inconclusive)",
        "Low resolution limits detailed analysis"
    ],
    "recommendations": [
        "Obtain higher quality source if available",
        "Analyze multiple frames from the same video",
        "Manual expert review recommended",
        "Check video metadata and provenance"
    ]
}
```

---

## Instructions for Multi-Frame Video Analysis

When analyzing a full video:

1. **Extract frames**: Take 5-10 frames evenly distributed throughout the video
2. **Analyze each frame**: Use the prompt above for each frame
3. **Aggregate results**:
   - Count verdicts across all frames
   - Calculate average confidence
   - Combine unique indicators
   - Final verdict = majority verdict

### Aggregated Response Format

For full video analysis, provide a summary:

```json
{
    "verdict": "AI_GENERATED",
    "confidence": 72,
    "reasoning": "Analyzed 5 frames. Verdicts: AI=3, Authentic=1, Uncertain=1. Average confidence: 72.0%",
    "indicators": [
        "Unnatural eye blinking pattern (frames 1, 3, 4)",
        "Inconsistent lighting on face (frames 2, 3)",
        "Soft edges around hairline (frames 1, 4, 5)",
        "Temporal flickering between frames"
    ],
    "recommendations": [
        "Compare with known authentic footage of subject",
        "Analyze audio track separately for sync issues",
        "Consider forensic analysis of video metadata"
    ]
}
```

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  VIDEO FRAUD DETECTION                      │
├────────────────────────────────────────────────────────────┤
│  VERDICTS:                                                  │
│    • AI_GENERATED - Content appears artificially created    │
│    • AUTHENTIC    - Content appears genuine                 │
│    • UNCERTAIN    - Cannot determine with confidence        │
├────────────────────────────────────────────────────────────┤
│  CONFIDENCE LEVELS:                                         │
│    • 80-100%  High confidence in verdict                    │
│    • 60-79%   Moderate confidence, some ambiguity           │
│    • 40-59%   Low confidence, significant uncertainty       │
│    • 0-39%    Very low confidence, inconclusive             │
├────────────────────────────────────────────────────────────┤
│  KEY INDICATORS TO CHECK:                                   │
│    □ Facial boundaries and hairline                         │
│    □ Eye reflections and blinking                           │
│    □ Lighting consistency                                   │
│    □ Edge artifacts and warping                             │
│    □ Background consistency                                 │
│    □ Motion and physics (hair, clothing)                    │
│    □ Audio-visual sync (if applicable)                      │
└────────────────────────────────────────────────────────────┘
```

---

## Usage Notes

1. **Always use the system prompt first** - This establishes the expert persona and analysis framework
2. **Upload the image with the analysis request** - Attach the frame/image along with the analysis prompt
3. **Expect JSON output** - The response should be valid JSON matching the format above
4. **For videos, analyze multiple frames** - Single frames may miss temporal artifacts
5. **Consider context** - Low quality or heavily compressed media may yield uncertain results
