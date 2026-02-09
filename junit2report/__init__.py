"""
JUnit Report Generator - Convert JUnit XML test results to HTML dashboards
"""

from .parser import parse_junit_xml, parse_junit_xml_string
from .generator import generate_html, get_available_templates
from pathlib import Path

__version__ = "1.0.0"
__all__ = ["parse_junit_xml", "parse_junit_xml_string", "generate_html", "get_available_templates", "create_report"]


def create_report(source=None, output=None, template="modern", xml_string=None, title="Test Results Report"):
    """
    Create an HTML report from JUnit XML test results.
    
    This is a convenience function that combines parsing and HTML generation.
    You can provide either a file path via 'source' or XML content via 'xml_string'.
    
    Args:
        source: Path to the JUnit XML file (optional if xml_string is provided)
        output: Path to save the HTML report (optional, returns HTML string if not provided)
        template: Template name to use (default: "modern")
        xml_string: XML content as string (optional if source is provided)
        title: Custom report title to display in templates (default: "Test Results Report")
        
    Returns:
        HTML content as string (if output is None), or None (if output path is provided)
        
    Example:
        # From file
        create_report(source="results.xml", output="report.html", template="dark", title="Nightly Run")
        
        # From XML string
        with open("results.xml", "r") as f:
            xml_data = f.read()
            html_content = create_report(xml_string=xml_data, template="minimal")
    """
    if source is None and xml_string is None:
        raise ValueError("Either 'source' or 'xml_string' must be provided")
    
    if source is not None and xml_string is not None:
        raise ValueError("Provide only one of 'source' or 'xml_string', not both")
    
    # Parse the XML
    if xml_string is not None:
        report_data = parse_junit_xml_string(xml_string)
    else:
        report_data = parse_junit_xml(source)
    
    # Generate HTML
    html_content = generate_html(report_data, template_name=template, title=title)
    
    # Write to file or return content
    if output is not None:
        Path(output).write_text(html_content, encoding="utf-8")
        return None
    else:
        return html_content
