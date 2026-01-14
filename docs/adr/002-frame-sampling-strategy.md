# ADR-002: Frame Sampling Strategy

## Status

Accepted

## Context

When analyzing a video for AI-generation indicators, we cannot feasibly analyze every frame due to:

1. **Time constraints**: LLM inference takes 10-30 seconds per frame
2. **Cost considerations**: More frames = more compute (even with local inference)
3. **Diminishing returns**: Adjacent frames contain redundant information

We needed to decide:
- How many frames to sample from each video?
- How to distribute the sampled frames across the video?

### Options Considered

| Strategy | Frames | Distribution | Pros | Cons |
|----------|--------|--------------|------|------|
| Single frame | 1 | Middle | Fast | May miss temporal artifacts |
| Sparse | 3 | Start/Middle/End | Quick | Gaps in coverage |
| **Moderate** | **5** | **Even distribution** | **Good balance** | **~2 min processing** |
| Dense | 10 | Even distribution | Thorough | Slow (~5 min) |
| Exhaustive | All | Sequential | Complete | Impractical |

## Decision

We will use **5 evenly-distributed frames** as the default sampling strategy:

1. **Frame count**: 5 frames provides sufficient coverage without excessive processing time
2. **Distribution**: Evenly distributed to capture beginning, middle, and end of video
3. **Configurable**: Users can adjust via `--frames` CLI argument

### Implementation

```python
# video_utils.py
def extract_frames(video_path: Path, num_frames: int) -> tuple[list[Path], str]:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate evenly distributed frame indices
    step = total_frames / num_frames
    frame_indices = [int(i * step) for i in range(num_frames)]

    # Extract frames at calculated positions
    for idx, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        ...
```

### Sampling Visualization

For a 100-frame video with 5 samples:
```
Frame:  0    20    40    60    80   100
        |     |     |     |     |
        ▼     ▼     ▼     ▼     ▼
      [F1]  [F2]  [F3]  [F4]  [F5]
```

## Consequences

### Positive

- **Reasonable processing time**: ~2 minutes for typical video
- **Good temporal coverage**: Captures artifacts throughout video
- **Configurable**: Power users can increase for thorough analysis
- **Memory efficient**: Only 5 frames loaded at a time

### Negative

- **May miss localized artifacts**: Brief anomalies between samples could be missed
- **Fixed distribution**: Doesn't adapt to video content (e.g., scene changes)
- **Not real-time**: Batch processing only

### Future Improvements

- **Adaptive sampling**: Detect scene changes and sample around transitions
- **Motion-based**: Sample more frames during high-motion segments
- **Confidence-driven**: Re-sample if initial results are uncertain
