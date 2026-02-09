"""
Command-line interface for JUnit Report Generator
"""

import argparse
import sys
from pathlib import Path
from .parser import parse_junit_xml
from .generator import generate_html, get_available_templates


def main():
    """
    Main entry point for the junit2html command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="Convert JUnit XML test results to HTML dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    junit2html test-results.xml
    junit2html test-results.xml -o my-report.html
    junit2html test-results.xml --template dark --title "Nightly Run"
    junit2html --list-templates
        """
    )
    
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to the JUnit XML file to parse"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="report.html",
        help="Output HTML file path (default: report.html)"
    )
    
    parser.add_argument(
        "--template",
        default="modern",
        help="Template name to use (default: modern)"
    )

    parser.add_argument(
        "--title",
        default="Test Results Report",
        help="Custom title for the report header"
    )
    
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List all available templates and exit"
    )
    
    parser.add_argument(
        "--allow-analytics",
        action="store_true",
        help="Generate an additional analytics report alongside the main report"
    )
    
    args = parser.parse_args()
    
    # Handle --list-templates
    if args.list_templates:
        templates = get_available_templates()
        print("Available templates:")
        for template in templates:
            print(f"  - {template}")
        sys.exit(0)
    
    # Validate source is provided
    if not args.source:
        parser.error("the following arguments are required: source")
    
    # Validate input file exists
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Input file '{args.source}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not source_path.is_file():
        print(f"Error: '{args.source}' is not a file", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Parse the JUnit XML file
        print(f"Parsing {args.source}...")
        report_data = parse_junit_xml(args.source)
        
        # Generate HTML report
        print(f"Generating HTML report using '{args.template}' template...")
        html_content = generate_html(report_data, template_name=args.template, title=args.title)
        
        # Write to output file
        output_path = Path(args.output)
        output_path.write_text(html_content, encoding="utf-8")
        
        # Generate analytics report if flag is set
        if args.allow_analytics:
            print(f"Generating analytics report...")
            analytics_html = generate_html(report_data, template_name="analytics", title=f"{args.title} - Analytics")
            
            # Generate analytics output path (insert -analytics before extension)
            analytics_path = output_path.parent / f"{output_path.stem}-analytics{output_path.suffix}"
            analytics_path.write_text(analytics_html, encoding="utf-8")
        
        # Print summary
        summary = report_data["summary"]
        print(f"\n✓ Report generated successfully: {args.output}")
        if args.allow_analytics:
            print(f"✓ Analytics report generated: {analytics_path.name}")
        print(f"\nTest Summary:")
        print(f"  Total:   {summary['total']}")
        print(f"  Passed:  {summary['passed']}")
        print(f"  Failed:  {summary['failed']}")
        print(f"  Errors:  {summary['errors']}")
        print(f"  Skipped: {summary['skipped']}")
        print(f"  Time:    {summary['time']}s")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

