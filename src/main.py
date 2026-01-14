"""Main entry point for Video Fraud Detection Agent.

Usage:
    python -m src.main --image path/to/frame.jpg
    python -m src.main --video path/to/video.mp4
"""

import argparse
import sys
from pathlib import Path

from .agent import VideoFraudDetectionAgent
from .models import Verdict


def main():
    """Run the video fraud detection agent."""
    parser = argparse.ArgumentParser(
        description="Analyze videos/images for AI-generated content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--image",
        type=Path,
        help="Path to a single image/frame to analyze",
    )
    parser.add_argument(
        "--video",
        type=Path,
        help="Path to a video file to analyze",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=5,
        help="Number of frames to sample from video (default: 5)",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="ollama",
        choices=["ollama", "openai", "anthropic"],
        help="LLM provider to use (default: ollama)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llava",
        help="Model name to use (default: llava)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    if not args.image and not args.video:
        parser.error("Either --image or --video must be specified")

    # Initialize agent
    agent = VideoFraudDetectionAgent(
        model_provider=args.provider,
        model_name=args.model,
    )

    # Run analysis
    try:
        if args.image:
            result = agent.analyze_frame(args.image)
        else:
            result = agent.analyze_video(args.video, sample_frames=args.frames)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotImplementedError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output results
    if args.json:
        import json

        output = {
            "verdict": result.verdict.value,
            "confidence": result.confidence,
            "reasoning": result.reasoning,
            "indicators": result.indicators,
            "recommendations": result.recommendations,
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(result)


def print_report(result):
    """Print a formatted analysis report.

    Args:
        result: AnalysisResult to display
    """
    verdict_symbols = {
        Verdict.AI_GENERATED: "🚨 AI GENERATED",
        Verdict.AUTHENTIC: "✅ AUTHENTIC",
        Verdict.UNCERTAIN: "⚠️  UNCERTAIN",
    }

    print("\n" + "=" * 60)
    print("VIDEO FRAUD DETECTION REPORT")
    print("=" * 60)

    print(f"\nVERDICT: {verdict_symbols.get(result.verdict, result.verdict.value)}")
    print(f"CONFIDENCE: {result.confidence:.1%}")

    print(f"\nREASONING:\n{result.reasoning}")

    if result.indicators:
        print("\nINDICATORS FOUND:")
        for indicator in result.indicators:
            print(f"  • {indicator}")

    if result.recommendations:
        print("\nRECOMMENDATIONS:")
        for rec in result.recommendations:
            print(f"  • {rec}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
