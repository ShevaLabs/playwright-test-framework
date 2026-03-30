#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_tests(args):
    """Run tests"""
    cmd = [
        "pytest",
        "-v",
        f"--env={args.env}",
        f"--browser={args.browser}",
        f"--alluredir=./reports/allure-results",
    ]

    if args.headless:
        cmd.append("--headless")

    if args.slow_mo:
        cmd.append(f"--slow-mo={args.slow_mo}")

    if args.mark:
        cmd.append(f"-m {args.mark}")

    if args.test_path:
        cmd.append(args.test_path)
    else:
        cmd.append("tests/")

    if args.workers:
        cmd.append(f"-n {args.workers}")

    if args.html_report:
        cmd.append("--html=./reports/report.html")
        cmd.append("--self-contained-html")

    print(f"Running command: {' '.join(cmd)}")

    result = subprocess.run(cmd)
    return result.returncode

def generate_allure_report():
    """Generate Allure report"""
    if os.path.exists("./reports/allure-results"):
        subprocess.run(["allure", "generate", "./reports/allure-results",
                       "-o", "./reports/allure-report", "--clean"])
        print("Allure report generated: ./reports/allure-report/index.html")

def main():
    parser = argparse.ArgumentParser(description="Run automated tests")
    parser.add_argument("--env", default="dev", help="Test environment")
    parser.add_argument("--browser", default="chromium", help="Browser")
    parser.add_argument("--headless", action="store_true", help="Headless mode")
    parser.add_argument("--slow-mo", type=int, default=100, help="Operation delay")
    parser.add_argument("--mark", help="Run tests with specific marker")
    parser.add_argument("--test-path", help="Specify test path")
    parser.add_argument("--workers", type=int, help="Number of parallel workers")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML report")
    parser.add_argument("--allure", action="store_true", help="Generate Allure report")

    args = parser.parse_args()

    # Create report directories
    Path("./reports").mkdir(exist_ok=True)
    Path("./screenshots").mkdir(exist_ok=True)
    Path("./logs").mkdir(exist_ok=True)
    Path("./traces").mkdir(exist_ok=True)

    # Run tests
    return_code = run_tests(args)

    # Generate report
    if args.allure or args.html_report:
        generate_allure_report()

    sys.exit(return_code)

if __name__ == "__main__":
    main()