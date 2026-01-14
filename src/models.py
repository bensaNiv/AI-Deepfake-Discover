"""Data models for Video Fraud Detection Agent.

This module contains the core data structures used for
analysis results and verdict classifications.
"""

from dataclasses import dataclass
from enum import Enum


class Verdict(Enum):
    """Classification verdict for video analysis."""

    AI_GENERATED = "ai_generated"
    AUTHENTIC = "authentic"
    UNCERTAIN = "uncertain"


@dataclass
class AnalysisResult:
    """Result of video fraud analysis.

    Attributes:
        verdict: Classification result (AI_GENERATED, AUTHENTIC, UNCERTAIN)
        confidence: Confidence score from 0.0 to 1.0
        reasoning: Detailed explanation of the verdict
        indicators: List of specific indicators found
        recommendations: List of recommended follow-up actions
    """

    verdict: Verdict
    confidence: float  # 0.0 to 1.0
    reasoning: str
    indicators: list[str]
    recommendations: list[str]
