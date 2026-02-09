"""
JUnit XML Parser - Extracts test results from JUnit XML format
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any
from io import StringIO


def parse_junit_xml(file_path: str) -> Dict[str, Any]:
    """
    Parse a JUnit XML file and extract test results.
    
    Handles both <testsuites> (multiple suites) and <testsuite> (single suite)
    as root elements.
    
    Args:
        file_path: Path to the JUnit XML file
        
    Returns:
        Dictionary containing:
        - summary: Dict with total, passed, failed, errors, skipped, time
        - test_cases: List of test case dictionaries
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return _parse_xml_element(root)


def parse_junit_xml_string(xml_string: str) -> Dict[str, Any]:
    """
    Parse JUnit XML from a string and extract test results.
    
    Handles both <testsuites> (multiple suites) and <testsuite> (single suite)
    as root elements.
    
    Args:
        xml_string: XML content as string
        
    Returns:
        Dictionary containing:
        - summary: Dict with total, passed, failed, errors, skipped, time
        - test_cases: List of test case dictionaries
    """
    root = ET.fromstring(xml_string)
    return _parse_xml_element(root)


def _parse_xml_element(root: ET.Element) -> Dict[str, Any]:
    """
    Internal function to parse an XML element (root) into test results.
    
    Args:
        root: The root XML element
        
    Returns:
        Dictionary containing summary and test_cases
    """
    # Initialize counters
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0
    test_cases = []
    
    # Determine if root is testsuites or testsuite
    if root.tag == "testsuites":
        testsuites = root.findall("testsuite")
    elif root.tag == "testsuite":
        testsuites = [root]
    else:
        raise ValueError(f"Unknown root element: {root.tag}. Expected 'testsuites' or 'testsuite'")
    
    # Process each test suite
    for testsuite in testsuites:
        suite_name = testsuite.get("name", "Unknown Suite")
        
        # Extract suite-level attributes
        suite_tests = int(testsuite.get("tests", 0))
        suite_failures = int(testsuite.get("failures", 0))
        suite_errors = int(testsuite.get("errors", 0))
        suite_skipped = int(testsuite.get("skipped", 0))
        suite_time = float(testsuite.get("time", 0.0))
        
        # Update totals
        total_tests += suite_tests
        total_failures += suite_failures
        total_errors += suite_errors
        total_skipped += suite_skipped
        total_time += suite_time
        
        # Process test cases
        for testcase in testsuite.findall("testcase"):
            case_name = testcase.get("name", "Unknown Test")
            class_name = testcase.get("classname", suite_name)
            time_taken = float(testcase.get("time", 0.0))
            
            # Determine test status
            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped = testcase.find("skipped")
            
            if failure is not None:
                status = "failed"
                message = failure.get("message", "Test failed")
                output = failure.text or ""
            elif error is not None:
                status = "error"
                message = error.get("message", "Test error")
                output = error.text or ""
            elif skipped is not None:
                status = "skipped"
                message = skipped.get("message", "Test skipped")
                output = skipped.text or ""
            else:
                status = "passed"
                message = ""
                output = ""
            
            # Extract system-out and system-err
            system_out = testcase.find("system-out")
            system_err = testcase.find("system-err")
            
            if system_out is not None and system_out.text:
                output += "\n" + system_out.text
            if system_err is not None and system_err.text:
                output += "\n[stderr]\n" + system_err.text
            
            test_cases.append({
                "name": case_name,
                "classname": class_name,
                "status": status,
                "time": time_taken,
                "message": message.strip(),
                "output": output.strip(),
            })
    
    # Calculate passed tests
    total_passed = total_tests - total_failures - total_errors - total_skipped
    
    return {
        "summary": {
            "total": total_tests,
            "passed": total_passed,
            "failed": total_failures,
            "errors": total_errors,
            "skipped": total_skipped,
            "time": round(total_time, 2),
        },
        "test_cases": test_cases,
    }
