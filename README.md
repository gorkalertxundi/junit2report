# JUnit Report Generator

![PyPI - Version](https://img.shields.io/pypi/v/junit2html) ![License](https://img.shields.io/pypi/l/junit2html) ![Python Version](https://img.shields.io/pypi/pyversions/junit2html) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/junit2html?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=MAGENTA&left_text=total+downloads)](https://pepy.tech/projects/junit2html) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/junit2html?period=monthly&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=last+month+downloads)](https://pepy.tech/projects/junit2html)

**junit2html** is a lightweight, zero-dependency Python tool that converts JUnit XML test reports into human-readable, static HTML dashboards.

Perfect for CI/CD pipelines, local debugging, or sharing test results with stakeholders.

## 🚀 Key Features

* **Simple Conversion:** Turn complex XML into a clean, responsive HTML file in seconds.
* **🎨 Multiple Templates:** Choose from built-in themes (Dark mode, Minimal, etc.) to suit your preferences.
* **CI/CD Ready:** Seamlessly integrates with Jenkins, GitHub Actions, GitLab CI, and CircleCI.
* **Detailed Insights:** View pass/fail rates, execution times, and capture stdout/stderr logs.
* **Dual Mode:** Use it as a CLI tool or import it as a Python library.

## 📦 Installation

Install the package via pip:

```bash
pip install junit2html
```

## 🛠 Usage

**Command Line Interface (CLI)**
Basic conversion (uses default template):
```bash
junit2html report.xml -o output.html
```

Using a specific template:
```bash
junit2html report.xml -o output.html --template dark
```

Setting a custom title:
```bash
junit2html report.xml -o output.html --template legacy --title "Nightly Run"
```

List available templates:
```bash
junit2html --list-templates
```

Generating analytics reports (in addition to the main report):
```bash
junit2html report.xml -o output.html --allow-analytics
```
This generates both `output.html` (main report) and `output-analytics.html` (analytics dashboard with charts and filters).

**Python Library**
You can integrate the generator directly into your Python scripts.

```python
from junit_report_generator import create_report

# Convert with a specific template
create_report(
    source="results.xml", 
    output="dashboard.html", 
    template="dark",
    title="Nightly Run"
)

# or using a string of XML data
with open("results.xml", "r") as f:
    xml_data = f.read()
    html_content = create_report(xml_string=xml_data, template="minimal")
```

## 🎨 Available Templates

The package comes with several pre-built templates to customize your report style.

| Template Name | Description | Best For |
| :--- | :--- | :--- |
| **modern** | (Default) A clean, colorful dashboard with charts and collapsible sections. | General use, stakeholder reports. |
| **dark** | A high-contrast dark theme version of the modern dashboard. | Late-night debugging, dark-mode lovers. |
| **minimal** | A text-heavy, high-density layout with no charts and only minimal inline JavaScript for basic filtering/collapsing. | Large test suites (10k+ tests), slow connections that still allow basic interactivity. |
| **legacy** | A simple table view similar to older Jenkins reports. | Backward compatibility. |
| **analytics** | Advanced analytics dashboard with multi-axis charts, performance insights, and interactive filters. | In-depth performance analysis, identifying bottlenecks. |

### 📸 Template Previews

<table>
  <tr>
    <td width="50%" valign="top">
      <h4 align="center">Modern (Default)</h4>
      <img src="https://github.com/user-attachments/assets/1e01da9f-b310-4537-989f-ec92f2eb81e6" alt="Modern Report" width="100%" />
    </td>
    <td width="50%" valign="top">
      <h4 align="center">Dark</h4>
      <img src="https://github.com/user-attachments/assets/ae7e86d5-beb8-4734-a37f-adb7837da87d" alt="Dark Report" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4 align="center">Minimal</h4>
      <img src="https://github.com/user-attachments/assets/bea75c2b-dcbb-42c4-a2d4-2712be1ce35f" alt="Minimal Report" width="100%" />
    </td>
    <td width="50%" valign="top">
      <h4 align="center">Legacy</h4>
      <img src="https://github.com/user-attachments/assets/ae641be7-4e01-45b1-a3ee-c3b0ccbbb5c2" alt="Legacy Report" width="100%" />
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <h4 align="center">Analytics</h4>
      <img src="https://github.com/user-attachments/assets/4d4c5423-d3b3-4d75-ac39-a2a40f11f554" alt="Analytics Report - Overview" width="100%" />
      <img src="https://github.com/user-attachments/assets/8e2d12dc-b127-4e04-ba0b-3f1bed52339a" alt="Analytics Report - Charts" width="100%" />
      <img src="https://github.com/user-attachments/assets/c740fb80-a619-4233-83cb-801db15ea8e4" alt="Analytics Report - Performance" width="100%" />
      <img src="https://github.com/user-attachments/assets/a1959c16-1913-408e-aaf9-06a9b4561aa5" alt="Analytics Report - Errors" width="100%" />
      <img src="https://github.com/user-attachments/assets/4e114064-885f-4d1b-b419-0c9a15bd2f20" alt="Analytics Report - Top Tests" width="100%" />
    </td>
  </tr>
</table>

## 📊 Example Output
The generated HTML report includes:

- Summary Cards: Total tests, passed, failed, skipped, and total duration.
- Test Cases Table: Sortable list of all test cases with status indicators.
- Failure Details: Expandable sections showing stack traces and error messages.

### Analytics Dashboard (`--allow-analytics`)
The analytics report provides advanced insights:

- **Interactive Charts**: Status distribution, test count by class, execution time by class, failure distribution, and pass rate visualization.
- **Performance Metrics**: Detailed breakdown of test execution by class with averages and statistics.
- **Error Analysis**: Deduplicated error messages with frequency counts and affected tests.
- **Top Tests**: Slowest and fastest tests ranked by execution time.
- **Filterable Sections**: Use "Show top N" filters in Performance by Class and Error Analysis sections to focus on the most relevant data.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gorkalertxundi/junit-html-report-generator.git
   cd junit-html-report-generator
   ```

2. **Install in editable mode**
   ```bash
   pip install -e .
   ```
   This installs the package in development mode, allowing you to make changes to the source code and test them immediately without reinstalling.

3. **Verify the installation**
   ```bash
   # Check that the CLI is available
  junit2html --list-templates
   
   # Verify templates are bundled correctly
   python -c "from junit2html import get_available_templates; print(get_available_templates())"
   ```

### Running Tests

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m unittest discover tests

# Run tests with verbose output
python -m unittest discover tests -v

# Run a specific test
python -m unittest tests.test_parser.TestJUnitParser.test_parse_single_testsuite
```

All tests should pass before submitting a pull request.

### Testing Locally

1. **Generate a test report**
   ```bash
   # Use the provided sample file
  junit2html sample-test-results.xml -o test-report.html
   
   # Try different templates
  junit2html sample-test-results.xml -o dark-report.html --template dark
  junit2html sample-test-results.xml -o minimal-report.html --template minimal
   ```

2. **Test the Python API**
   ```python
   from junit2html import create_report
   
   # Test with file
   create_report(source="sample-test-results.xml", output="api-test.html")
   
   # Test with XML string
   with open("sample-test-results.xml") as f:
       html = create_report(xml_string=f.read(), template="dark")
       print(f"Generated {len(html)} bytes of HTML")
   ```

3. **Test template bundling**
   ```bash
   # Build the package
   python -m build
   
   # Check that templates are included
  tar -tzf dist/junit2html-*.tar.gz | grep templates
   ```

### Adding a New Template

1. Create your template file in `junit2html/templates/yourtemplate.html`
2. Use Jinja2 syntax with these variables:
   - `{{ summary.total }}`, `{{ summary.passed }}`, `{{ summary.failed }}`, etc.
   - `{{ summary.pass_rate }}` for the percentage
   - `{% for test in test_cases %}` to iterate through tests
   - `{{ test.name }}`, `{{ test.status }}`, `{{ test.message }}`, `{{ test.output }}`
3. Test your template: `junit2html sample-test-results.xml --template yourtemplate`
4. The template will automatically appear in `--list-templates`

### Contribution Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and test thoroughly
4. Run the test suite to ensure nothing broke
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request with a clear description of your changes

## 📄 License
Distributed under the MIT License. See LICENSE for more information.