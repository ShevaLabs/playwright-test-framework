import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import allure

class ReportGenerator:
    """Generate test reports in various formats"""
    
    def __init__(self, report_dir: str = "./reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)
    
    @allure.step("Generate JSON report")
    def generate_json_report(self, test_results: Dict[str, Any]) -> str:
        """Generate JSON format test report"""
        report_file = self.report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "results": test_results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return str(report_file)
    
    @allure.step("Generate JUnit XML report")
    def generate_junit_report(self, test_results: Dict[str, Any]) -> str:
        """Generate JUnit XML format test report"""
        report_file = self.report_dir / f"junit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        
        # Build JUnit XML structure
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
    <testsuite name="Playwright Tests" tests="{total}" failures="{failures}" errors="{errors}" skipped="{skipped}" time="{time}">
""".format(
            total=test_results.get("total", 0),
            failures=test_results.get("failed", 0),
            errors=test_results.get("errors", 0),
            skipped=test_results.get("skipped", 0),
            time=test_results.get("duration", 0)
        )
        
        # Add test cases
        for test in test_results.get("tests", []):
            xml_content += f"""
        <testcase name="{test['name']}" classname="{test['class']}" time="{test['duration']}">"""
            
            if test.get("status") == "failed":
                xml_content += f"""
            <failure message="{test.get('error_message', 'Test failed')}">
                {test.get('traceback', '')}
            </failure>"""
            elif test.get("status") == "skipped":
                xml_content += """
            <skipped />"""
            
            xml_content += """
        </testcase>"""
        
        xml_content += """
    </testsuite>
</testsuites>"""
        
        with open(report_file, 'w') as f:
            f.write(xml_content)
        
        return str(report_file)
    
    @allure.step("Generate performance report")
    def generate_performance_report(self, performance_data: List[Dict[str, Any]]) -> str:
        """Generate performance test report"""
        report_file = self.report_dir / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                .metric-good { color: green; }
                .metric-bad { color: red; }
            </style>
        </head>
        <body>
            <h1>Performance Test Report</h1>
            <p>Generated: {timestamp}</p>
            <table>
                <tr>
                    <th>Test Name</th>
                    <th>Response Time (ms)</th>
                    <th>Status</th>
                </tr>
        """.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for data in performance_data:
            status_class = "metric-good" if data.get("response_time", 0) < data.get("threshold", 1000) else "metric-bad"
            html_content += f"""
                <tr>
                    <td>{data.get('test_name', 'N/A')}</td>
                    <td>{data.get('response_time', 0)}</td>
                    <td class="{status_class}">{data.get('status', 'N/A')}</td>
                </tr>"""
        
        html_content += """
            </table>
        </body>
        </html>"""
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        return str(report_file)