# Video Fraud Detection - Experiment Results

## Experiment Overview

**Date**: January 2026
**Model Used**: Vision LLM with security expert persona
**Dataset**: 5 videos (3 AI-generated, 2 authentic)
**Task**: Binary classification - detect AI-generated video content

---

## Dataset Summary

| Video | Ground Truth | File |
|-------|--------------|------|
| Video 1 | AI Generated | `vidoe_1.mp4` |
| Video 2 | AI Generated | `video_2.mp4` |
| Video 3 | AI Generated | `video_3.mp4` |
| Video 4 | Authentic | `video_4.mp4` |
| Video 5 | Authentic | `video_5.mp4` |

---

## Results Summary

### Overall Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 80% (4/5) |
| **Precision** | 75% (3/4) |
| **Recall** | 100% (3/3) |
| **F1 Score** | 0.857 |

### Confusion Matrix

```
                    Predicted
                 AI_GEN    AUTH
Actual  AI_GEN     3         0      (True Positives: 3, False Negatives: 0)
        AUTH       1         1      (False Positives: 1, True Negatives: 1)
```

| | Predicted AI | Predicted Authentic |
|---|:---:|:---:|
| **Actual AI** | 3 (TP) | 0 (FN) |
| **Actual Authentic** | 1 (FP) | 1 (TN) |

---

## Per-Video Results

### Video 1 - AI Generated

| Field | Value |
|-------|-------|
| **Ground Truth** | AI Generated |
| **Prediction** | AI_GENERATED |
| **Confidence** | 98% |
| **Result** | ✅ CORRECT |

**Key Indicators Detected:**
- Morphing artifacts: hands appear to 'melt' or fuse with sweater texture
- Anatomical inconsistency: fingers appear and disappear unnaturally
- Teeth and mouth rendering issues
- Temporal hair flickering
- Background physics anomalies (plant warping)

---

### Video 2 - AI Generated

| Field | Value |
|-------|-------|
| **Ground Truth** | AI Generated |
| **Prediction** | AI_GENERATED |
| **Confidence** | 95% |
| **Result** | ✅ CORRECT |

**Key Indicators Detected:**
- Sunglasses morphing with hair during movement
- Anatomical 'liquidity' in shoulders/neck
- Facial distortion during smile
- Background parallax inconsistency
- Static lighting despite body orientation change

---

### Video 3 - AI Generated

| Field | Value |
|-------|-------|
| **Ground Truth** | AI Generated |
| **Prediction** | AI_GENERATED |
| **Confidence** | 95% |
| **Result** | ✅ CORRECT |

**Key Indicators Detected:**
- Anatomical morphing during sit-to-stand transition
- Edge blurring and halos around subject
- Facial structure changes between poses
- Unrealistic fabric physics
- Background texture warping

---

### Video 4 - Authentic (MISCLASSIFIED)

| Field | Value |
|-------|-------|
| **Ground Truth** | Authentic |
| **Prediction** | AI_GENERATED |
| **Confidence** | 98% |
| **Result** | ❌ INCORRECT (False Positive) |

**Why the model failed:**
The model incorrectly flagged this authentic video as AI-generated. The high-confidence error suggests the model may be:
1. Over-sensitive to motion blur and compression artifacts
2. Misinterpreting natural hand movements as "morphing"
3. Confusing video compression artifacts with AI generation artifacts

**Reported Indicators (False Alarms):**
- "Hands merge and sprout extra fingers" - likely motion blur
- "Object permanence failure" - likely fast motion
- "Physics inconsistency" - normal fluid behavior misinterpreted
- "Temporal flickering" - compression artifacts

---

### Video 5 - Authentic

| Field | Value |
|-------|-------|
| **Ground Truth** | Authentic |
| **Prediction** | AUTHENTIC |
| **Confidence** | 95% |
| **Result** | ✅ CORRECT |

**Key Authenticity Indicators:**
- Natural skin micro-textures and pores
- Realistic ocular saccades
- Stable complex background objects
- Precise audio-visual synchronization
- Natural lens bokeh and aberrations

---

## Analysis

### Confidence Distribution

| Verdict | Videos | Avg Confidence |
|---------|--------|----------------|
| AI_GENERATED | 4 | 96.5% |
| AUTHENTIC | 1 | 95.0% |

### Error Analysis

**Total Errors**: 1 (Video 4)
**Error Type**: False Positive
**Error Rate**: 20%

The model shows a tendency toward **false positives** - flagging authentic content as AI-generated. This is concerning for practical applications where falsely accusing authentic content could have serious implications.

### Key Findings

1. **High recall for AI content**: The model correctly identified all 3 AI-generated videos (100% recall)
2. **False positive vulnerability**: Complex motion in authentic videos can trigger false AI detection
3. **Confidence calibration issue**: The false positive had 98% confidence - higher than some correct predictions
4. **Motion artifacts sensitivity**: The model may confuse motion blur with AI morphing artifacts

---

## Recommendations

1. **Threshold tuning**: Consider requiring higher confidence (>98%) for AI_GENERATED verdicts
2. **Multi-frame analysis**: Increase frame sampling to reduce motion blur misinterpretation
3. **Compression awareness**: Train/prompt model to distinguish compression from AI artifacts
4. **Confidence calibration**: High confidence should correlate with accuracy

---

## Raw Data

### Confidence Scores

```
Video 1: 98% (AI_GENERATED) - Correct
Video 2: 95% (AI_GENERATED) - Correct
Video 3: 95% (AI_GENERATED) - Correct
Video 4: 98% (AI_GENERATED) - INCORRECT
Video 5: 95% (AUTHENTIC)    - Correct
```

### Performance Metrics Calculation

```
True Positives (TP)  = 3  (AI correctly identified as AI)
True Negatives (TN)  = 1  (Authentic correctly identified as Authentic)
False Positives (FP) = 1  (Authentic incorrectly identified as AI)
False Negatives (FN) = 0  (AI incorrectly identified as Authentic)

Accuracy  = (TP + TN) / Total = (3 + 1) / 5 = 0.80 = 80%
Precision = TP / (TP + FP) = 3 / (3 + 1) = 0.75 = 75%
Recall    = TP / (TP + FN) = 3 / (3 + 0) = 1.00 = 100%
F1 Score  = 2 * (Precision * Recall) / (Precision + Recall) = 2 * (0.75 * 1.0) / (0.75 + 1.0) = 0.857
```
