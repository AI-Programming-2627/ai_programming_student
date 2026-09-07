"""
Grade Calculator

Runs all test files, collects results, and computes a weighted score
based on the WEIGHTS defined in each test file.

Usage:
    uv run python grade.py
    uv run python grade.py --verbose   # show per-test details
"""
import argparse
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Import weights from each test file
from tests.test1 import WEIGHTS as WEIGHTS_1
from tests.test2 import WEIGHTS as WEIGHTS_2
from tests.test3 import WEIGHTS as WEIGHTS_3

# Combine all weights
ALL_WEIGHTS = {}
ALL_WEIGHTS.update(WEIGHTS_1)
ALL_WEIGHTS.update(WEIGHTS_2)
ALL_WEIGHTS.update(WEIGHTS_3)

# Group by test file for display
WEIGHTS_BY_FILE = {
    "test1": WEIGHTS_1,
    "test2": WEIGHTS_2,
    "test3": WEIGHTS_3,
}

# Test file paths (relative to repo root)
TEST_FILES = [
    "tests/test1.py",
    "tests/test2.py",
    "tests/test3.py",
]


def run_tests(junit_xml_path=".pytest_grades.xml"):
    """Run all tests with JUnit XML output and return the exit code."""
    import pytest

    args = ["-v", "--tb=short", f"--junitxml={junit_xml_path}"] + TEST_FILES
    return pytest.main(args)


def parse_results(xml_path):
    """Parse the JUnit XML file and return a dict of test_name -> passed (bool)."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = {}

    for testsuite in root.findall("testsuite"):
        for testcase in testsuite.findall("testcase"):
            name = testcase.get("name")
            failure = testcase.find("failure")
            error = testcase.find("error")
            results[name] = (failure is None and error is None)

    return results


def compute_score(results):
    """Compute the weighted score from test results.

    Returns (earned_points, total_points, grade_percent, details).
    """
    total_points = sum(ALL_WEIGHTS.values())
    earned_points = 0
    details = []

    for test_name, weight in ALL_WEIGHTS.items():
        passed = results.get(test_name, False)
        if passed:
            earned_points += weight
            status = "PASS"
        else:
            status = "FAIL"

        details.append((test_name, weight, status, passed))

    grade_percent = (earned_points / total_points) * 100 if total_points > 0 else 0
    return earned_points, total_points, grade_percent, details


def print_report(earned, total, percent, details, results, verbose=False):
    """Print a formatted grade report."""
    print("=" * 60)
    print("  FLOOR CLEANING AGENT - GRADE REPORT")
    print("=" * 60)

    if verbose:
        print()
        for test_name, weight, status, _ in details:
            icon = "[PASS]" if status == "PASS" else "[FAIL]"
            print(f"  {icon} {test_name:<55s} {weight:>2d}pt  {status}")
    else:
        for file_label, file_weights in WEIGHTS_BY_FILE.items():
            file_earned = sum(
                w for tn, w in file_weights.items() if results.get(tn, False)
            )
            file_total = sum(file_weights.values())
            print(f"\n  {file_label}.py:  {file_earned}/{file_total} pts")

    print()
    print("-" * 60)
    print(f"  TOTAAL:  {earned:3d} / {total}  ({percent:.1f}%)")
    print("=" * 60)

    return percent, earned, total


def write_github_summary(earned, total, percent, details):
    """Write the grade to the GitHub Actions step summary ($GITHUB_STEP_SUMMARY)."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    lines = [
        "## Score",
        "",
        f"**{earned} / {total}**  ({percent:.1f}%)",
        "",
        "| Test | Weight | Status |",
        "|---|---|---|",
    ]
    for test_name, weight, status, _ in details:
        lines.append(f"| {test_name} | {weight} | **{status}** |")

    with open(summary_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bereken het cijfer voor de vloerreinigingsagent"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Toon resultaat per individuele test"
    )
    args = parser.parse_args()

    xml_path = ".pytest_grades.xml"

    print("Tests worden uitgevoerd...")
    exit_code = run_tests(xml_path)

    results = parse_results(xml_path)

    # Clean up temp file
    Path(xml_path).unlink(missing_ok=True)

    earned, total, percent, details = compute_score(results)
    print_report(earned, total, percent, details, results, verbose=args.verbose)
    write_github_summary(earned, total, percent, details)

    if exit_code != 0:
        sys.exit(1)