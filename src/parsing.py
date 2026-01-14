"""Response parsing utilities for Video Fraud Detection Agent.

This module handles parsing LLM responses and aggregating
results from multiple frame analyses.
"""

import json

from .models import AnalysisResult, Verdict


def parse_llm_response(response: str) -> AnalysisResult:
    """Parse LLM response into structured result.

    Args:
        response: Raw LLM response text

    Returns:
        Structured AnalysisResult
    """
    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            data = json.loads(json_str)

            verdict_map = {
                "AI_GENERATED": Verdict.AI_GENERATED,
                "AUTHENTIC": Verdict.AUTHENTIC,
                "UNCERTAIN": Verdict.UNCERTAIN,
            }

            return AnalysisResult(
                verdict=verdict_map.get(
                    data.get("verdict", "UNCERTAIN"), Verdict.UNCERTAIN
                ),
                confidence=float(data.get("confidence", 50)) / 100.0,
                reasoning=data.get("reasoning", "No reasoning provided"),
                indicators=data.get("indicators", []),
                recommendations=data.get("recommendations", []),
            )
    except (json.JSONDecodeError, KeyError, ValueError):
        pass

    return AnalysisResult(
        verdict=Verdict.UNCERTAIN,
        confidence=0.0,
        reasoning=response,
        indicators=[],
        recommendations=["Manual review recommended due to parsing issues"],
    )


def aggregate_results(results: list[AnalysisResult]) -> AnalysisResult:
    """Aggregate multiple frame results into overall verdict.

    Args:
        results: List of individual frame analysis results

    Returns:
        Aggregated AnalysisResult with combined verdict
    """
    if not results:
        return AnalysisResult(
            verdict=Verdict.UNCERTAIN,
            confidence=0.0,
            reasoning="No frames analyzed",
            indicators=[],
            recommendations=["Provide video frames for analysis"],
        )

    verdict_counts = {v: 0 for v in Verdict}
    total_confidence = 0.0
    all_indicators = []
    all_recommendations = []

    for result in results:
        verdict_counts[result.verdict] += 1
        total_confidence += result.confidence
        all_indicators.extend(result.indicators)
        all_recommendations.extend(result.recommendations)

    max_verdict = max(verdict_counts, key=lambda v: verdict_counts[v])
    avg_confidence = total_confidence / len(results)
    unique_indicators = list(set(all_indicators))
    unique_recommendations = list(set(all_recommendations))

    reasoning = (
        f"Analyzed {len(results)} frames. "
        f"Verdicts: AI={verdict_counts[Verdict.AI_GENERATED]}, "
        f"Authentic={verdict_counts[Verdict.AUTHENTIC]}, "
        f"Uncertain={verdict_counts[Verdict.UNCERTAIN]}. "
        f"Average confidence: {avg_confidence:.1%}"
    )

    return AnalysisResult(
        verdict=max_verdict,
        confidence=avg_confidence,
        reasoning=reasoning,
        indicators=unique_indicators,
        recommendations=unique_recommendations,
    )
