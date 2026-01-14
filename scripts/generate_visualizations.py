"""Generate visualization graphs for experiment results."""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Results data
videos = ["Video 1", "Video 2", "Video 3", "Video 4", "Video 5"]
ground_truth = ["AI", "AI", "AI", "Authentic", "Authentic"]
predictions = ["AI", "AI", "AI", "AI", "Authentic"]
confidence = [98, 95, 95, 98, 95]
correct = [True, True, True, False, True]

# Output directory
output_dir = Path(__file__).parent.parent / "results" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)


def create_confidence_chart():
    """Create confidence scores bar chart with correctness indicators."""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ["#2ecc71" if c else "#e74c3c" for c in correct]
    bars = ax.bar(videos, confidence, color=colors, edgecolor="black", linewidth=1.2)

    # Add value labels on bars
    for bar, conf, corr in zip(bars, confidence, correct):
        label = f"{conf}%\n{'✓' if corr else '✗'}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() - 8,
            label,
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
            color="white",
        )

    # Add ground truth labels below x-axis
    for i, (video, gt) in enumerate(zip(videos, ground_truth)):
        ax.text(i, -3, f"({gt})", ha="center", va="top", fontsize=9, color="gray")

    ax.set_ylim(0, 105)
    ax.set_ylabel("Confidence (%)", fontsize=12)
    ax.set_xlabel("Video (Ground Truth)", fontsize=12)
    ax.set_title("Model Confidence by Video\n(Green = Correct, Red = Incorrect)", fontsize=14, fontweight="bold")
    ax.axhline(y=90, color="orange", linestyle="--", alpha=0.7, label="90% threshold")
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(output_dir / "confidence_by_video.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confidence_by_video.png'}")


def create_confusion_matrix():
    """Create confusion matrix visualization."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Confusion matrix values
    cm = np.array([[3, 0], [1, 1]])  # [[TP, FN], [FP, TN]]

    # Create heatmap
    im = ax.imshow(cm, cmap="Blues")

    # Labels
    classes = ["AI Generated", "Authentic"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(classes, fontsize=11)
    ax.set_yticklabels(classes, fontsize=11)
    ax.set_xlabel("Predicted", fontsize=12, fontweight="bold")
    ax.set_ylabel("Actual", fontsize=12, fontweight="bold")
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")

    # Add text annotations
    labels = [["TP = 3", "FN = 0"], ["FP = 1", "TN = 1"]]
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > 1.5 else "black"
            ax.text(j, i, f"{cm[i, j]}\n({labels[i][j]})",
                   ha="center", va="center", fontsize=14, fontweight="bold", color=color)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Count", fontsize=11)

    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'confusion_matrix.png'}")


def create_metrics_summary():
    """Create metrics summary bar chart."""
    fig, ax = plt.subplots(figsize=(8, 5))

    metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
    values = [80, 75, 100, 85.7]
    colors = ["#3498db", "#9b59b6", "#2ecc71", "#f39c12"]

    bars = ax.bar(metrics, values, color=colors, edgecolor="black", linewidth=1.2)

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{val:.1f}%",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    ax.set_ylim(0, 115)
    ax.set_ylabel("Percentage (%)", fontsize=12)
    ax.set_title("Model Performance Metrics", fontsize=14, fontweight="bold")
    ax.axhline(y=100, color="gray", linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_dir / "performance_metrics.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_dir / 'performance_metrics.png'}")


if __name__ == "__main__":
    print("Generating visualizations...")
    create_confidence_chart()
    create_confusion_matrix()
    create_metrics_summary()
    print("Done!")
