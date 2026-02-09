"""
Unit tests for JUnit XML parser
"""

import unittest
import tempfile
import os
from junit2report.parser import parse_junit_xml, parse_junit_xml_string


class TestJUnitParser(unittest.TestCase):
    """Test cases for the JUnit XML parser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def create_temp_xml(self, content):
        """Helper to create a temporary XML file"""
        file_path = os.path.join(self.temp_dir, "test.xml")
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def test_parse_single_testsuite(self):
        """Test parsing a single testsuite as root"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
                            <testsuite name="MyTestSuite" tests="3" failures="1" errors="0" skipped="1" time="1.234">
                                <testcase name="test_success" classname="MyTest" time="0.123"></testcase>
                                <testcase name="test_failure" classname="MyTest" time="0.456">
                                    <failure message="Assertion failed">Expected 5 but got 3</failure>
                                </testcase>
                                <testcase name="test_skipped" classname="MyTest" time="0.000">
                                    <skipped message="Not implemented yet"/>
                                </testcase>
                            </testsuite>
                        """
        file_path = self.create_temp_xml(xml_content)
        result = parse_junit_xml(file_path)
        
        # Check summary
        self.assertEqual(result["summary"]["total"], 3)
        self.assertEqual(result["summary"]["passed"], 1)
        self.assertEqual(result["summary"]["failed"], 1)
        self.assertEqual(result["summary"]["errors"], 0)
        self.assertEqual(result["summary"]["skipped"], 1)
        self.assertEqual(result["summary"]["time"], 1.23)
        
        # Check test cases
        self.assertEqual(len(result["test_cases"]), 3)
        
        # Check first test (passed)
        test1 = result["test_cases"][0]
        self.assertEqual(test1["name"], "test_success")
        self.assertEqual(test1["status"], "passed")
        self.assertEqual(test1["classname"], "MyTest")
        
        # Check second test (failed)
        test2 = result["test_cases"][1]
        self.assertEqual(test2["name"], "test_failure")
        self.assertEqual(test2["status"], "failed")
        self.assertEqual(test2["message"], "Assertion failed")
        self.assertIn("Expected 5 but got 3", test2["output"])
        
        # Check third test (skipped)
        test3 = result["test_cases"][2]
        self.assertEqual(test3["name"], "test_skipped")
        self.assertEqual(test3["status"], "skipped")
    
    def test_parse_multiple_testsuites(self):
        """Test parsing multiple testsuites"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
                        <testsuites>
                            <testsuite name="Suite1" tests="2" failures="0" errors="0" skipped="0" time="0.5">
                                <testcase name="test1" classname="Class1" time="0.2"></testcase>
                                <testcase name="test2" classname="Class1" time="0.3"></testcase>
                            </testsuite>
                            <testsuite name="Suite2" tests="1" failures="0" errors="1" skipped="0" time="0.1">
                                <testcase name="test3" classname="Class2" time="0.1">
                                    <error message="RuntimeError">Something went wrong</error>
                                </testcase>
                            </testsuite>
                        </testsuites>
                        """
        file_path = self.create_temp_xml(xml_content)
        result = parse_junit_xml(file_path)
        
        # Check summary
        self.assertEqual(result["summary"]["total"], 3)
        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["failed"], 0)
        self.assertEqual(result["summary"]["errors"], 1)
        self.assertEqual(result["summary"]["skipped"], 0)
        self.assertEqual(result["summary"]["time"], 0.6)
        
        # Check test cases
        self.assertEqual(len(result["test_cases"]), 3)
        
        # Check error test
        error_test = result["test_cases"][2]
        self.assertEqual(error_test["status"], "error")
        self.assertEqual(error_test["message"], "RuntimeError")
    
    def test_parse_with_system_output(self):
        """Test parsing test cases with system output"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
                        <testsuite name="OutputTest" tests="1" failures="0" errors="0" skipped="0" time="0.1">
                            <testcase name="test_with_output" classname="OutputTest" time="0.1">
                                <system-out>Standard output message</system-out>
                                <system-err>Error output message</system-err>
                            </testcase>
                        </testsuite>
                        """
        file_path = self.create_temp_xml(xml_content)
        result = parse_junit_xml(file_path)
        
        test = result["test_cases"][0]
        self.assertIn("Standard output message", test["output"])
        self.assertIn("Error output message", test["output"])
        self.assertIn("[stderr]", test["output"])
    
    def test_parse_xml_string(self):
        """Test parsing XML from string instead of file"""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
                    <testsuite name="StringTest" tests="2" failures="0" errors="0" skipped="0" time="0.5">
                        <testcase name="test_a" classname="StringTest" time="0.2"></testcase>
                        <testcase name="test_b" classname="StringTest" time="0.3"></testcase>
                    </testsuite>
                    """
        result = parse_junit_xml_string(xml_string)
        
        # Check summary
        self.assertEqual(result["summary"]["total"], 2)
        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["failed"], 0)
        
        # Check test cases
        self.assertEqual(len(result["test_cases"]), 2)
        self.assertEqual(result["test_cases"][0]["name"], "test_a")
        self.assertEqual(result["test_cases"][1]["name"], "test_b")


if __name__ == "__main__":
    unittest.main()

