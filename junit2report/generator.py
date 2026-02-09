"""
HTML Report Generator - Renders test results using Jinja2 templates
"""

from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict, Any, List
import os


def get_available_templates() -> List[str]:
    """
    Get a list of available template names.
    
    Returns:
        List of template names (without .html extension)
    """
    env = Environment(
        loader=PackageLoader("junit_html_report_generator", "templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    
    # Get all template names and remove .html extension
    templates = env.list_templates()
    return [t.replace(".html", "") for t in templates if t.endswith(".html") and not t.startswith("__")]


def generate_html(report_data: Dict[str, Any], template_name: str = "modern", title: str = "Test Results Report") -> str:
    """
    Generate an HTML report from parsed JUnit data.
    
    Args:
        report_data: Dictionary containing 'summary' and 'test_cases'
        template_name: Name of the template to use (without .html extension)
        
    Returns:
        Rendered HTML string
        
    Raises:
        jinja2.TemplateNotFound: If the template doesn't exist
    """
    # Set up Jinja2 environment with PackageLoader to load templates from the package
    env = Environment(
        loader=PackageLoader("junit_html_report_generator", "templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    
    # Load the template
    template = env.get_template(f"{template_name}.html")
    
    # Calculate pass rate
    summary = report_data["summary"]
    if summary["total"] > 0:
        pass_rate = (summary["passed"] / summary["total"]) * 100
    else:
        pass_rate = 0.0
    
    # Add pass_rate to summary
    summary["pass_rate"] = round(pass_rate, 1)
    
    # Render the template
    html_content = template.render(
        summary=summary,
        test_cases=report_data["test_cases"],
        title=title
    )
    
    return html_content
