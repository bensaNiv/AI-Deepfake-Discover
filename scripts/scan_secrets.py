#!/usr/bin/env python3
"""Scan codebase for hardcoded secrets.

This script scans Python source files for potential hardcoded secrets
such as API keys, passwords, tokens, and other sensitive data.

Usage:
    python scripts/scan_secrets.py
    python scripts/scan_secrets.py --path src/
    python scripts/scan_secrets.py --verbose
"""

import argparse
import re
import sys
from pathlib import Path


# Patterns that may indicate hardcoded secrets
SECRET_PATTERNS = [
    # Generic API keys and secrets
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][^"\']{10,}["\']', "API Key"),
    (r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\'][^"\']{10,}["\']', "Secret Key"),
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']+["\']', "Password"),
    (r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\'][^"\']{10,}["\']', "Token"),
    # Provider-specific patterns
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
    (r'sk-ant-[a-zA-Z0-9\-]{20,}', "Anthropic API Key"),
    (r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}', "Bearer Token"),
    # Database connection strings
    (r'(?i)(mysql|postgres|mongodb)://[^\s"\']+:[^\s"\']+@', "Database URL"),
    # AWS credentials
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
    (r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\'][^"\']+["\']', "AWS Secret"),
]

# Files and directories to skip
SKIP_PATTERNS = [
    r'\.git',
    r'__pycache__',
    r'\.pyc$',
    r'\.env$',
    r'\.env\.example$',
    r'node_modules',
    r'\.venv',
    r'venv',
]

# Known false positives (patterns that look like secrets but aren't)
FALSE_POSITIVE_PATTERNS = [
    r'your[_-]?api[_-]?key',
    r'placeholder',
    r'example',
    r'xxx+',
    r'\*+',
    r'<[^>]+>',  # Template placeholders like <your-key>
]


def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    path_str = str(path)
    return any(re.search(pattern, path_str) for pattern in SKIP_PATTERNS)


def is_false_positive(match: str) -> bool:
    """Check if a match is a known false positive."""
    match_lower = match.lower()
    return any(re.search(pattern, match_lower) for pattern in FALSE_POSITIVE_PATTERNS)


def scan_file(file_path: Path, verbose: bool = False) -> list[tuple[int, str, str]]:
    """Scan a single file for secrets.

    Args:
        file_path: Path to the file to scan
        verbose: Whether to print verbose output

    Returns:
        List of (line_number, pattern_name, matched_text) tuples
    """
    findings = []

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            for pattern, pattern_name in SECRET_PATTERNS:
                matches = re.finditer(pattern, line)
                for match in matches:
                    matched_text = match.group(0)
                    if not is_false_positive(matched_text):
                        findings.append((line_num, pattern_name, matched_text[:50]))

    except (OSError, UnicodeDecodeError) as e:
        if verbose:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)

    return findings


def scan_directory(
    root_path: Path, verbose: bool = False
) -> dict[Path, list[tuple[int, str, str]]]:
    """Scan a directory recursively for secrets.

    Args:
        root_path: Root directory to scan
        verbose: Whether to print verbose output

    Returns:
        Dictionary mapping file paths to their findings
    """
    all_findings = {}

    # File extensions to scan
    extensions = {".py", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf"}

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in extensions:
            if should_skip(file_path):
                continue

            if verbose:
                print(f"Scanning: {file_path}", file=sys.stderr)

            findings = scan_file(file_path, verbose)
            if findings:
                all_findings[file_path] = findings

    return all_findings


def main():
    """Run the secrets scanner."""
    parser = argparse.ArgumentParser(
        description="Scan codebase for hardcoded secrets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Path to scan (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SECRET SCANNER")
    print("=" * 60)
    print(f"\nScanning: {args.path.resolve()}\n")

    findings = scan_directory(args.path, args.verbose)

    if findings:
        print("\nPOTENTIAL SECRETS FOUND:")
        print("-" * 60)

        total_count = 0
        for file_path, file_findings in sorted(findings.items()):
            print(f"\n{file_path}:")
            for line_num, pattern_name, matched_text in file_findings:
                print(f"  Line {line_num}: [{pattern_name}] {matched_text}...")
                total_count += 1

        print("\n" + "=" * 60)
        print(f"RESULT: {total_count} potential secret(s) found in {len(findings)} file(s)")
        print("=" * 60)
        print("\nPlease review these findings and:")
        print("1. Remove any actual secrets from the codebase")
        print("2. Use environment variables instead")
        print("3. Add secrets to .gitignore if needed")
        sys.exit(1)
    else:
        print("=" * 60)
        print("RESULT: No secrets found")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
