"""
Grade Calculator

Dynamically discovers all week*/test_week*.py files, runs all tests,
collects results, and computes a weighted score with per-week breakdowns.

Usage:
    uv run python grade.py
    uv run python grade.py --verbose   # show per-test details
"""
import argparse
import glob
import importlib.util
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def discover_weeks():
    """Discover all week directories with test files.

    Returns a list of (week_label, test_file_path, weights_dict) sorted by week number.
    """
    test_files = sorted(glob.glob("exercises/week*/test_week*.py"))
    weeks = []

    for test_path in test_files:
        # Extract week label from path, e.g. "week01/test_week01.py" -> "week01"
        week_label = Path(test_path).parent.name

        # Import weights dynamically
        module_name = test_path.replace(os.sep, ".").replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, test_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        weights = getattr(module, "WEIGHTS", {})
        weeks.append((week_label, test_path, weights))

    return weeks


def run_tests(junit_xml_path=".pytest_grades.xml"):
    """Run all tests with JUnit XML output and return the exit code."""
    import pytest

    test_files = sorted(glob.glob("exercises/week*/test_week*.py"))
    args = ["-v", "--tb=short", f"--junitxml={junit_xml_path}"] + test_files
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


def compute_score(results, weeks):
    """Compute the weighted score from test results.

    Returns (earned_points, total_points, grade_percent, week_details, all_details).
    """
    # Build a mapping of test_name -> weight from all weeks
    all_weights = {}
    for week_label, test_path, weights in weeks:
        all_weights.update(weights)

    total_points = sum(all_weights.values())
    earned_points = 0
    all_details = []

    for test_name, weight in all_weights.items():
        passed = results.get(test_name, False)
        if passed:
            earned_points += weight
            status = "PASS"
        else:
            status = "FAIL"

        all_details.append((test_name, weight, status, passed))

    grade_percent = (earned_points / total_points) * 100 if total_points > 0 else 0

    # Per-week breakdown
    week_details = []
    for week_label, test_path, weights in weeks:
        week_earned = sum(
            w for tn, w in weights.items() if results.get(tn, False)
        )
        week_total = sum(weights.values())
        week_pct = (week_earned / week_total * 100) if week_total > 0 else 0
        week_details.append((week_label, week_earned, week_total, week_pct))

    return earned_points, total_points, grade_percent, week_details, all_details


def build_progress_bar(percent, width=20):
    """Build a simple ASCII progress bar."""
    filled = int(percent / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return bar


def print_report(earned, total, percent, week_details, all_details, results, weeks, verbose=False):
    """Print a formatted grade report with per-week breakdowns."""
    print("=" * 72)
    print("  FLOOR CLEANING AGENT — WEEKLY PROGRESS REPORT")
    print("=" * 72)

    # ── Per-week summary ──────────────────────────────────────────
    print()
    print("  WEEK          SCORE       PROGRESS")
    print("  ─────────────────────────────────────────────────────")
    for week_label, week_earned, week_total, week_pct in week_details:
        bar = build_progress_bar(week_pct)
        print(f"  {week_label}    {week_earned:2d}/{week_total:<2d} pts  {bar} {week_pct:5.1f}%")

    print("  ─────────────────────────────────────────────────────")

    # ── Total ─────────────────────────────────────────────────────
    total_bar = build_progress_bar(percent)
    print(f"  TOTAAL    {earned:3d}/{total:<2d} pts  {total_bar} {percent:5.1f}%")

    # ── Per-test details (verbose) ────────────────────────────────
    if verbose:
        print()
        print("─" * 72)
        print("  DETAILED TEST RESULTS")
        print("─" * 72)

        # Group details by week for the verbose output
        week_weights_map = {}
        for week_label, test_path, weights in weeks:
            week_weights_map[week_label] = weights

        for week_label, week_earned, week_total, week_pct in week_details:
            print(f"\n  ── {week_label} ──")
            week_weights = week_weights_map.get(week_label, {})
            for test_name, weight, status, _ in all_details:
                if test_name in week_weights:
                    icon = "[PASS]" if status == "PASS" else "[FAIL]"
                    print(f"    {icon} {test_name:<55s} {weight:>2d}pt  {status}")

    # ── Legend ────────────────────────────────────────────────────
    print()
    print("─" * 72)
    print(f"  EINDCIFER:  {earned:3d} / {total}  ({percent:.1f}%)")
    print("=" * 72)

    return percent, earned, total


def write_github_summary(earned, total, percent, week_details, all_details):
    """Write the grade to the GitHub Actions step summary ($GITHUB_STEP_SUMMARY)."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    lines = [
        "## Weekly Progress Score",
        "",
        f"**{earned} / {total}**  ({percent:.1f}%)",
        "",
        "| Week | Score | Progress |",
        "|---|---|---|",
    ]
    for week_label, week_earned, week_total, week_pct in week_details:
        bar = build_progress_bar(week_pct, width=12)
        lines.append(f"| {week_label} | {week_earned}/{week_total} | {bar} {week_pct:.0f}% |")

    lines.append("")
    lines.append("### Per-test details")
    lines.append("| Test | Weight | Status |")
    lines.append("|---|---|---|")
    for test_name, weight, status, _ in all_details:
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

    # Discover all weeks
    weeks = discover_weeks()

    # Clean up temp file
    Path(xml_path).unlink(missing_ok=True)

    earned, total, percent, week_details, all_details = compute_score(results, weeks)
    print_report(earned, total, percent, week_details, all_details, results, weeks, verbose=args.verbose)
    write_github_summary(earned, total, percent, week_details, all_details)

    if exit_code != 0:
        sys.exit(1)