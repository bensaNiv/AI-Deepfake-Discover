# Research Documentation

## Research Questions

### Primary Research Question

**Can a vision-capable LLM with a security expert persona accurately detect AI-generated video content?**

### Hypotheses

1. **H1**: An LLM prompted as a security expert will identify AI-generated content with >75% accuracy
2. **H2**: Multi-frame analysis will improve detection accuracy over single-frame analysis
3. **H3**: The model will show higher confidence for correctly classified samples

---

## Methodology

### Experimental Design

**Type**: Controlled experiment with ground-truth labeled dataset

**Variables**:
- **Independent**: Video source (AI-generated vs authentic)
- **Dependent**: Classification verdict, confidence score
- **Controlled**: Model (LLaVA), frame count (5), prompt structure

### Dataset

| Property | Value |
|----------|-------|
| Total videos | 5 |
| AI-generated | 3 |
| Authentic | 2 |
| Format | MP4 |
| Duration | 5-15 seconds |

**Dataset Composition**:
- Video 1-3: AI-generated content from various generators
- Video 4-5: Authentic recorded footage

### Evaluation Metrics

1. **Accuracy**: (TP + TN) / Total
2. **Precision**: TP / (TP + FP)
3. **Recall**: TP / (TP + FN)
4. **F1 Score**: 2 * (Precision * Recall) / (Precision + Recall)

### Procedure

1. Initialize agent with LLaVA model via Ollama
2. For each video:
   - Extract 5 evenly-distributed frames
   - Analyze each frame independently
   - Aggregate results using majority voting
   - Record verdict and confidence
3. Compare predictions against ground truth
4. Calculate performance metrics

---

## Parameter Exploration

### Frame Count

**Question**: How does the number of sampled frames affect accuracy?

**Parameter**: `sample_frames` (default: 5)

| Frames | Trade-off |
|--------|-----------|
| 1 | Fast but may miss temporal artifacts |
| 3 | Balance of speed and coverage |
| 5 | Good coverage, moderate speed (default) |
| 10 | Thorough but slower |

**Finding**: 5 frames provides sufficient coverage for videos < 30 seconds

### Confidence Threshold

**Question**: Should we filter low-confidence predictions?

**Analysis**:
- Average confidence for correct predictions: 96.0%
- Average confidence for incorrect predictions: 98.0%

**Finding**: Confidence does not reliably indicate accuracy (see Error Analysis)

### Model Selection

**Question**: Which vision model performs best?

**Models Tested**:
- LLaVA (llava:latest) - Selected for local inference
- LLaVA 13B - Larger but similar performance

**Rationale for LLaVA**:
- Open source
- Runs locally via Ollama
- Good vision understanding
- Reasonable inference speed

---

## Results Summary

### Quantitative Results

| Metric | Value |
|--------|-------|
| Accuracy | 80% (4/5 correct) |
| Precision | 75% |
| Recall | 100% |
| F1 Score | 0.857 |

### Confusion Matrix

|  | Predicted AI | Predicted Authentic |
|---|:---:|:---:|
| **Actual AI** | 3 (TP) | 0 (FN) |
| **Actual Authentic** | 1 (FP) | 1 (TN) |

### Per-Sample Results

| Video | Ground Truth | Prediction | Confidence | Correct |
|-------|--------------|------------|------------|---------|
| 1 | AI Generated | AI_GENERATED | 98% | Yes |
| 2 | AI Generated | AI_GENERATED | 95% | Yes |
| 3 | AI Generated | AI_GENERATED | 95% | Yes |
| 4 | Authentic | AI_GENERATED | 98% | No |
| 5 | Authentic | AUTHENTIC | 95% | Yes |

### Hypothesis Evaluation

| Hypothesis | Result | Evidence |
|------------|--------|----------|
| H1: >75% accuracy | **Supported** | 80% accuracy achieved |
| H2: Multi-frame improves accuracy | **Inconclusive** | No single-frame baseline |
| H3: Higher confidence = correct | **Rejected** | FP had highest confidence |

---

## Error Analysis

### False Positive Analysis (Video 4)

**Ground Truth**: Authentic
**Prediction**: AI_GENERATED (98% confidence)

**Reported Indicators** (False Alarms):
1. "Hands merge and sprout extra fingers"
2. "Object permanence failure in liquid dynamics"
3. "Physics inconsistency in fluid behavior"
4. "Temporal flickering suggesting frame interpolation"

**Root Cause Analysis**:
- Video contained fast hand movements causing motion blur
- Natural fluid dynamics misinterpreted as physics errors
- Video compression artifacts confused with AI artifacts

### Confidence Calibration Issue

**Observation**: The false positive had the highest confidence (98%)

**Implications**:
- Confidence scores cannot be used to filter predictions
- High confidence may indicate overconfidence, not accuracy
- Need additional calibration mechanism

---

## Limitations

1. **Small Dataset**: 5 videos insufficient for statistical significance
2. **Class Imbalance**: 3:2 ratio of AI:authentic
3. **No Temporal Analysis**: Frames analyzed independently
4. **Compression Sensitivity**: Model confused by video artifacts
5. **Single Model**: Only tested with LLaVA

---

## Future Work

### Short-term Improvements

1. **Compression Awareness**: Add prompt guidance about codec artifacts
2. **Confidence Calibration**: Implement temperature scaling
3. **Threshold Tuning**: Require higher confidence for AI verdicts

### Long-term Research

1. **Larger Dataset**: Test with 50+ videos
2. **Cross-Model Comparison**: Compare GPT-4V, Claude, Gemini
3. **Temporal Analysis**: Add inter-frame consistency checks
4. **Hybrid Approach**: Combine LLM with traditional CV features
5. **Adversarial Testing**: Test against detection-aware generators

---

## Analysis Notebooks

For detailed statistical analysis and visualizations, see:
- `notebooks/experiment_analysis.ipynb`

For raw metrics data, see:
- `results/metrics/experiment_metrics.json`
- `results/figures/` for generated visualizations
