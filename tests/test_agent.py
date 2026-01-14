"""Unit tests for VideoFraudDetectionAgent."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.agent import VideoFraudDetectionAgent
from src.models import AnalysisResult, Verdict
from src.parsing import aggregate_results, parse_llm_response
from src.prompts import SYSTEM_PROMPT


class TestVerdict:
    """Tests for Verdict enum."""

    def test_verdict_values(self):
        """Test that all verdict values are correctly defined."""
        assert Verdict.AI_GENERATED.value == "ai_generated"
        assert Verdict.AUTHENTIC.value == "authentic"
        assert Verdict.UNCERTAIN.value == "uncertain"

    def test_verdict_count(self):
        """Test that we have exactly 3 verdict types."""
        assert len(Verdict) == 3


class TestAnalysisResult:
    """Tests for AnalysisResult dataclass."""

    def test_create_result(self):
        """Test creating an AnalysisResult."""
        result = AnalysisResult(
            verdict=Verdict.AI_GENERATED,
            confidence=0.95,
            reasoning="Test reasoning",
            indicators=["indicator1", "indicator2"],
            recommendations=["rec1"],
        )

        assert result.verdict == Verdict.AI_GENERATED
        assert result.confidence == 0.95
        assert result.reasoning == "Test reasoning"
        assert len(result.indicators) == 2
        assert len(result.recommendations) == 1

    def test_result_with_empty_lists(self):
        """Test creating result with empty indicator/recommendation lists."""
        result = AnalysisResult(
            verdict=Verdict.UNCERTAIN,
            confidence=0.5,
            reasoning="Uncertain",
            indicators=[],
            recommendations=[],
        )

        assert result.indicators == []
        assert result.recommendations == []


class TestVideoFraudDetectionAgent:
    """Tests for VideoFraudDetectionAgent class."""

    def test_agent_initialization_default(self):
        """Test agent initializes with default values."""
        agent = VideoFraudDetectionAgent()

        assert agent.model_provider == "ollama"
        assert agent.model_name == "llava"
        assert agent._temp_dir is None

    def test_agent_initialization_custom(self):
        """Test agent initializes with custom values."""
        agent = VideoFraudDetectionAgent(
            model_provider="openai",
            model_name="gpt-4-vision",
        )

        assert agent.model_provider == "openai"
        assert agent.model_name == "gpt-4-vision"

    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 100
        assert "security expert" in SYSTEM_PROMPT.lower()

    def test_analyze_frame_file_not_found(self):
        """Test that analyze_frame raises error for missing file."""
        agent = VideoFraudDetectionAgent()

        with pytest.raises(FileNotFoundError):
            agent.analyze_frame("/nonexistent/path/image.jpg")

    def test_analyze_video_file_not_found(self):
        """Test that analyze_video raises error for missing file."""
        agent = VideoFraudDetectionAgent()

        with pytest.raises(FileNotFoundError):
            agent.analyze_video("/nonexistent/path/video.mp4")


class TestResponseParsing:
    """Tests for response parsing functionality."""

    def test_parse_valid_json_response(self):
        """Test parsing a valid JSON response."""
        response = json.dumps({
            "verdict": "AI_GENERATED",
            "confidence": 85,
            "reasoning": "Multiple artifacts detected",
            "indicators": ["artifact1", "artifact2"],
            "recommendations": ["review manually"],
        })

        result = parse_llm_response(response)

        assert result.verdict == Verdict.AI_GENERATED
        assert result.confidence == 0.85
        assert "Multiple artifacts" in result.reasoning
        assert len(result.indicators) == 2

    def test_parse_authentic_verdict(self):
        """Test parsing AUTHENTIC verdict."""
        response = json.dumps({
            "verdict": "AUTHENTIC",
            "confidence": 90,
            "reasoning": "Looks real",
            "indicators": [],
            "recommendations": [],
        })

        result = parse_llm_response(response)

        assert result.verdict == Verdict.AUTHENTIC
        assert result.confidence == 0.90

    def test_parse_uncertain_verdict(self):
        """Test parsing UNCERTAIN verdict."""
        response = json.dumps({
            "verdict": "UNCERTAIN",
            "confidence": 45,
            "reasoning": "Cannot determine",
            "indicators": [],
            "recommendations": ["need more data"],
        })

        result = parse_llm_response(response)

        assert result.verdict == Verdict.UNCERTAIN
        assert result.confidence == 0.45

    def test_parse_invalid_json_fallback(self):
        """Test that invalid JSON falls back to UNCERTAIN."""
        response = "This is not valid JSON at all"

        result = parse_llm_response(response)

        assert result.verdict == Verdict.UNCERTAIN
        assert result.confidence == 0.0
        assert "This is not valid JSON" in result.reasoning

    def test_parse_json_with_extra_text(self):
        """Test parsing JSON embedded in extra text."""
        response = """Here is my analysis:
        {
            "verdict": "AI_GENERATED",
            "confidence": 75,
            "reasoning": "Found issues",
            "indicators": ["issue1"],
            "recommendations": []
        }
        That's my conclusion."""

        result = parse_llm_response(response)

        assert result.verdict == Verdict.AI_GENERATED
        assert result.confidence == 0.75


class TestResultAggregation:
    """Tests for result aggregation functionality."""

    def test_aggregate_empty_results(self):
        """Test aggregating empty results list."""
        result = aggregate_results([])

        assert result.verdict == Verdict.UNCERTAIN
        assert result.confidence == 0.0
        assert "No frames" in result.reasoning

    def test_aggregate_single_result(self):
        """Test aggregating single result."""
        results = [
            AnalysisResult(
                verdict=Verdict.AI_GENERATED,
                confidence=0.9,
                reasoning="AI detected",
                indicators=["artifact"],
                recommendations=["review"],
            )
        ]

        result = aggregate_results(results)

        assert result.verdict == Verdict.AI_GENERATED
        assert result.confidence == 0.9

    def test_aggregate_majority_ai_generated(self):
        """Test aggregation with majority AI_GENERATED."""
        results = [
            AnalysisResult(Verdict.AI_GENERATED, 0.9, "r1", ["i1"], []),
            AnalysisResult(Verdict.AI_GENERATED, 0.8, "r2", ["i2"], []),
            AnalysisResult(Verdict.AUTHENTIC, 0.7, "r3", ["i3"], []),
        ]

        result = aggregate_results(results)

        assert result.verdict == Verdict.AI_GENERATED
        assert "Analyzed 3 frames" in result.reasoning

    def test_aggregate_majority_authentic(self):
        """Test aggregation with majority AUTHENTIC."""
        results = [
            AnalysisResult(Verdict.AUTHENTIC, 0.9, "r1", [], []),
            AnalysisResult(Verdict.AUTHENTIC, 0.85, "r2", [], []),
            AnalysisResult(Verdict.AI_GENERATED, 0.6, "r3", ["i1"], []),
        ]

        result = aggregate_results(results)

        assert result.verdict == Verdict.AUTHENTIC

    def test_aggregate_confidence_average(self):
        """Test that confidence is averaged correctly."""
        results = [
            AnalysisResult(Verdict.AI_GENERATED, 0.8, "r1", [], []),
            AnalysisResult(Verdict.AI_GENERATED, 0.9, "r2", [], []),
            AnalysisResult(Verdict.AI_GENERATED, 1.0, "r3", [], []),
        ]

        result = aggregate_results(results)

        assert result.confidence == pytest.approx(0.9, rel=0.01)

    def test_aggregate_deduplicates_indicators(self):
        """Test that indicators are deduplicated."""
        results = [
            AnalysisResult(Verdict.AI_GENERATED, 0.9, "r1", ["dup", "unique1"], []),
            AnalysisResult(Verdict.AI_GENERATED, 0.9, "r2", ["dup", "unique2"], []),
        ]

        result = aggregate_results(results)

        # Should have 3 unique indicators, not 4
        assert len(result.indicators) == 3
        assert "dup" in result.indicators


class TestProjectStructure:
    """Tests to verify project structure."""

    def test_src_directory_exists(self):
        """Test that src directory exists."""
        assert Path("src").is_dir()

    def test_agent_module_exists(self):
        """Test that agent.py exists."""
        assert Path("src/agent.py").is_file()

    def test_main_module_exists(self):
        """Test that main.py exists."""
        assert Path("src/main.py").is_file()

    def test_models_module_exists(self):
        """Test that models.py exists."""
        assert Path("src/models.py").is_file()

    def test_parsing_module_exists(self):
        """Test that parsing.py exists."""
        assert Path("src/parsing.py").is_file()

    def test_prompts_module_exists(self):
        """Test that prompts.py exists."""
        assert Path("src/prompts.py").is_file()

    def test_providers_module_exists(self):
        """Test that providers.py exists."""
        assert Path("src/providers.py").is_file()

    def test_video_utils_module_exists(self):
        """Test that video_utils.py exists."""
        assert Path("src/video_utils.py").is_file()

    def test_videos_directory_exists(self):
        """Test that videos directory exists."""
        assert Path("videos").is_dir()

    def test_results_directory_exists(self):
        """Test that results directory exists."""
        assert Path("results").is_dir()

    def test_docs_directory_exists(self):
        """Test that docs directory exists."""
        assert Path("docs").is_dir()

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists."""
        assert Path("requirements.txt").is_file()

    def test_readme_exists(self):
        """Test that README.md exists."""
        assert Path("README.md").is_file()

    def test_costs_file_exists(self):
        """Test that COSTS.md exists."""
        assert Path("COSTS.md").is_file()

    def test_prd_file_exists(self):
        """Test that PRD.md exists."""
        assert Path("PRD.md").is_file()

    def test_prompt_book_file_exists(self):
        """Test that PROMPT_BOOK.md exists."""
        assert Path("PROMPT_BOOK.md").is_file()

    def test_contributing_file_exists(self):
        """Test that CONTRIBUTING.md exists."""
        assert Path("CONTRIBUTING.md").is_file()


class TestPromptsModule:
    """Tests for prompts module."""

    def test_system_prompt_contains_security_expert(self):
        """Test system prompt mentions security expert."""
        assert "security expert" in SYSTEM_PROMPT.lower()

    def test_system_prompt_contains_analysis_categories(self):
        """Test system prompt has all analysis categories."""
        assert "FACIAL ANALYSIS" in SYSTEM_PROMPT
        assert "TEMPORAL CONSISTENCY" in SYSTEM_PROMPT
        assert "TECHNICAL ARTIFACTS" in SYSTEM_PROMPT
        assert "CONTEXTUAL ANALYSIS" in SYSTEM_PROMPT

    def test_system_prompt_mentions_verdicts(self):
        """Test system prompt mentions verdict options."""
        assert "AI_GENERATED" in SYSTEM_PROMPT
        assert "AUTHENTIC" in SYSTEM_PROMPT
        assert "UNCERTAIN" in SYSTEM_PROMPT


class TestModelsModule:
    """Tests for models module."""

    def test_verdict_is_enum(self):
        """Test Verdict is an enum."""
        from enum import Enum
        assert issubclass(Verdict, Enum)

    def test_analysis_result_is_dataclass(self):
        """Test AnalysisResult is a dataclass."""
        from dataclasses import is_dataclass
        assert is_dataclass(AnalysisResult)
