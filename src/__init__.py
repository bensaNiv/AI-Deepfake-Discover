"""Project 9 - AI Video Fraud Detection Agent.

A security expert agent specialized in investigating video frauds
and detecting AI-generated video content.
"""

from .agent import VideoFraudDetectionAgent
from .models import AnalysisResult, Verdict

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = [
    "VideoFraudDetectionAgent",
    "AnalysisResult",
    "Verdict",
]
