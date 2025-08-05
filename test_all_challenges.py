#!/usr/bin/env python3
"""
Test runner for Cryptopals challenges.
Runs each challenge and verifies it passes by checking for "✅ Passed" in output.
"""

# Created entirely with Claude.AI

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def run_challenge(challenge_file: str) -> Tuple[bool, str, str]:
    """
    Run a single challenge file and return (success, stdout, stderr).
    Success is True if the output contains "✅ Passed".
    """
    try:
        result = subprocess.run(
            [sys.executable, challenge_file],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
        )

        output = result.stdout
        error = result.stderr

        # Check if the challenge passed
        success = "✅ Passed" in output and result.returncode == 0

        return success, output, error

    except subprocess.TimeoutExpired:
        return False, "", "Challenge timed out after 30 seconds"
    except Exception as e:
        return False, "", f"Error running challenge: {str(e)}"


def find_challenge_files() -> List[str]:
    """Find all challenge files in the current directory."""
    challenge_files = []

    # Look for files matching pattern set*-challenge*.py
    for file_path in Path(".").glob("set*-challenge*.py"):
        challenge_files.append(str(file_path))

    # Sort them naturally (set1-challenge1, set1-challenge2, etc.)
    challenge_files.sort(
        key=lambda x: (
            int(x.split("-")[0].replace("set", "")),
            int(x.split("-")[1].replace("challenge", "").replace(".py", "")),
        )
    )

    return challenge_files


def main():
    """Run all challenges and report results."""
    print("🧪 Running Cryptopals Challenge Tests")
    print("=" * 50)

    challenge_files = find_challenge_files()

    if not challenge_files:
        print("❌ No challenge files found!")
        print("Looking for files matching pattern: set*-challenge*.py")
        return 1

    print(f"Found {len(challenge_files)} challenge files:")
    for file in challenge_files:
        print(f"  - {file}")
    print()

    passed = 0
    failed = 0
    results = []

    for challenge_file in challenge_files:
        print(f"Running {challenge_file}...", end=" ")

        success, stdout, stderr = run_challenge(challenge_file)

        if success:
            print("✅ PASSED")
            passed += 1
            results.append((challenge_file, True, stdout, stderr))
        else:
            print("❌ FAILED")
            failed += 1
            results.append((challenge_file, False, stdout, stderr))

    print()
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")

    # Show detailed results for failed tests
    if failed > 0:
        print("\n🔍 Failed Challenge Details:")
        print("-" * 30)

        for challenge_file, success, stdout, stderr in results:
            if not success:
                print(f"\n❌ {challenge_file}:")
                if stdout:
                    print("STDOUT:")
                    print(stdout)
                if stderr:
                    print("STDERR:")
                    print(stderr)
                print("-" * 30)

    # Show summary of passed tests
    if passed > 0:
        print(f"\n✅ Passed Challenges ({passed}):")
        for challenge_file, success, stdout, stderr in results:
            if success:
                # Extract the challenge output (first line after the header)
                lines = stdout.strip().split("\n")
                summary = lines[1] if len(lines) > 1 else "Passed"
                print(f"  {challenge_file}: {summary}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
