# ADR-003: Majority Voting for Verdict Aggregation

## Status

Accepted

## Context

When analyzing multiple frames from a video, each frame produces an independent verdict:
- `AI_GENERATED`
- `AUTHENTIC`
- `UNCERTAIN`

We needed a strategy to aggregate these individual verdicts into a single video-level verdict.

### Options Considered

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| First frame | Use only the first frame's verdict | Simple, fast | Ignores temporal info |
| Last frame | Use only the last frame's verdict | Simple | Arbitrary choice |
| **Majority vote** | **Most common verdict wins** | **Democratic, robust** | **Ties possible** |
| Weighted vote | Weight by confidence scores | Uses confidence | Confidence unreliable |
| Any positive | AI_GENERATED if any frame says so | High recall | High false positives |
| Unanimous | AI_GENERATED only if all agree | High precision | Low recall |

## Decision

We will use **simple majority voting** to aggregate frame verdicts:

1. Count verdicts from all analyzed frames
2. Select the verdict with the highest count
3. Average confidence scores across all frames
4. Deduplicate indicators and recommendations

### Implementation

```python
# parsing.py
def aggregate_results(results: list[AnalysisResult]) -> AnalysisResult:
    # Count verdicts
    verdict_counts = {v: 0 for v in Verdict}
    for result in results:
        verdict_counts[result.verdict] += 1

    # Select majority verdict
    max_verdict = max(verdict_counts, key=lambda v: verdict_counts[v])

    # Average confidence
    avg_confidence = sum(r.confidence for r in results) / len(results)

    # Combine indicators (deduplicated)
    unique_indicators = list(set(
        indicator for r in results for indicator in r.indicators
    ))

    return AnalysisResult(
        verdict=max_verdict,
        confidence=avg_confidence,
        reasoning=f"Analyzed {len(results)} frames. Verdicts: ...",
        indicators=unique_indicators,
        recommendations=unique_recommendations,
    )
```

### Example

```
Frame 1: AI_GENERATED (98%)
Frame 2: AI_GENERATED (95%)
Frame 3: AI_GENERATED (92%)
Frame 4: AUTHENTIC (85%)
Frame 5: AI_GENERATED (90%)

Counts: AI_GENERATED=4, AUTHENTIC=1, UNCERTAIN=0
Result: AI_GENERATED (avg confidence: 92%)
```

## Consequences

### Positive

- **Robust to outliers**: Single misclassified frame doesn't flip verdict
- **Simple and interpretable**: Easy to understand and explain
- **No hyperparameters**: No thresholds to tune
- **Preserves all evidence**: Indicators from all frames are collected

### Negative

- **Tie handling**: With even frame counts, ties are possible (resolved arbitrarily)
- **Ignores confidence**: High-confidence frames count same as low-confidence
- **No weighting**: Frame position (start/middle/end) not considered

### Tie Resolution

In case of a tie (e.g., 2 AI_GENERATED, 2 AUTHENTIC, 1 UNCERTAIN), Python's `max()` returns the first maximum encountered. Given our Verdict enum order, this means:
1. AI_GENERATED (index 0) - wins ties
2. AUTHENTIC (index 1)
3. UNCERTAIN (index 2)

This bias toward AI_GENERATED in ties is intentional for security applications where false negatives (missing AI content) are more costly than false positives.

### Future Improvements

- **Confidence-weighted voting**: Give more weight to high-confidence frames
- **Temporal consistency**: Check if adjacent frames agree
- **Uncertainty propagation**: Return UNCERTAIN if verdicts are too mixed
