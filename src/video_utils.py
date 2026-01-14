"""Video processing utilities for Video Fraud Detection Agent.

This module contains utilities for extracting frames from videos
and managing temporary files.
"""

import os
import shutil
import tempfile
from pathlib import Path

import cv2


def extract_frames(video_path: Path, num_frames: int) -> tuple[list[Path], str]:
    """Extract sample frames from a video.

    Extracts evenly distributed frames from the video for analysis.

    Args:
        video_path: Path to video file
        num_frames: Number of frames to extract

    Returns:
        Tuple of (list of paths to extracted frame images, temp directory path)

    Raises:
        ValueError: If video cannot be opened or has no frames
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        raise ValueError(f"Video has no frames: {video_path}")

    # Calculate frame indices to extract (evenly distributed)
    if num_frames >= total_frames:
        frame_indices = list(range(total_frames))
    else:
        step = total_frames / num_frames
        frame_indices = [int(i * step) for i in range(num_frames)]

    # Create temp directory for frames
    temp_dir = tempfile.mkdtemp(prefix="video_fraud_")
    extracted_paths = []

    for idx, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if ret:
            frame_path = Path(temp_dir) / f"frame_{idx:04d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            extracted_paths.append(frame_path)

    cap.release()

    if not extracted_paths:
        cleanup_temp_files(temp_dir)
        raise ValueError(f"Could not extract any frames from: {video_path}")

    return extracted_paths, temp_dir


def cleanup_temp_files(temp_dir: str | None) -> None:
    """Clean up temporary frame files.

    Removes all extracted frames and the temp directory.

    Args:
        temp_dir: Path to temporary directory to remove
    """
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
