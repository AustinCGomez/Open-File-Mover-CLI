#!/usr/bin/env python3
"""
Test runner script for File Mover CLI
Runs all tests and generates a comprehensive report
"""

import unittest
import sys
import io
from contextlib import redirect_stdout, redirect_stderr


def run_tests_with_report():
    """Run all tests and generate a detailed report."""
    
    print("=" * 70)
    print("FILE MOVER CLI - TEST SUITE")
    print("=" * 70)
    print()
    
    # Discover and load all test cases
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Create a test runner with high verbosity
    stream = io.StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    # Run the tests
    print("Running tests...")
    print("-" * 50)
    
    # Capture both stdout and stderr
    with redirect_stdout(stream), redirect_stderr(stream):
        result = runner.run(suite)
    
    # Get the test output
    test_output = stream.getvalue()
    
    # Print summary
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print()
    
    # Print detailed results
    if result.failures:
        print("FAILURES:")
        print("=" * 50)
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print("-" * 30)
            print(traceback)
            print()
    
    if result.errors:
        print("ERRORS:")
        print("=" * 50)
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print("-" * 30)
            print(traceback)
            print()
    
    # Print test output (individual test results)
    print("DETAILED TEST OUTPUT:")
    print("=" * 50)
    print(test_output)
    
    # Overall result
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        return 1


if __name__ == '__main__':
    exit_code = run_tests_with_report()
    sys.exit(exit_code)