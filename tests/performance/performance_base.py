"""
Performance Test Base Class
"""
import time
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import allure
from playwright.sync_api import Page, Response
from utils.logger import logger
from pages.base_page import BasePage


class PerformanceMetrics:
    """Performance metrics collector"""
    
    def __init__(self):
        self.metrics = {
            "navigation_start": 0,
            "navigation_end": 0,
            "dom_content_loaded": 0,
            "load_event_end": 0,
            "first_paint": 0,
            "first_contentful_paint": 0,
            "largest_contentful_paint": 0,
            "first_input_delay": 0,
            "time_to_interactive": 0,
            "total_blocking_time": 0,
            "cumulative_layout_shift": 0,
            "server_response_time": 0,
            "page_load_time": 0,
            "api_response_times": [],
            "resource_load_times": {}
        }
    
    def collect_from_page(self, page: Page) -> Dict[str, Any]:
        """Collect performance metrics from page"""
        try:
            # Get navigation timing
            timing = page.evaluate("""() => {
                const perfData = performance.timing;
                const navStart = perfData.navigationStart;
                
                return {
                    navigationStart: navStart,
                    domContentLoaded: perfData.domContentLoadedEventEnd - navStart,
                    loadEventEnd: perfData.loadEventEnd - navStart,
                    responseStart: perfData.responseStart - navStart,
                    responseEnd: perfData.responseEnd - navStart,
                    domInteractive: perfData.domInteractive - navStart,
                    domComplete: perfData.domComplete - navStart
                };
            }""")
            
            self.metrics.update(timing)
            
            # Get paint timing
            paint_metrics = page.evaluate("""() => {
                const paintEntries = performance.getEntriesByType('paint');
                const metrics = {};
                paintEntries.forEach(entry => {
                    metrics[entry.name] = entry.startTime;
                });
                return metrics;
            }""")
            
            self.metrics["first_paint"] = paint_metrics.get("first-paint", 0)
            self.metrics["first_contentful_paint"] = paint_metrics.get("first-contentful-paint", 0)
            
            # Get Largest Contentful Paint
            lcp = page.evaluate("""() => {
                return new Promise((resolve) => {
                    new PerformanceObserver((entryList) => {
                        const entries = entryList.getEntries();
                        const lastEntry = entries[entries.length - 1];
                        resolve(lastEntry.startTime);
                    }).observe({entryTypes: ['largest-contentful-paint']});
                    
                    setTimeout(() => resolve(0), 3000);
                });
            }""")
            
            self.metrics["largest_contentful_paint"] = lcp
            
            return self.metrics
            
        except Exception as e:
            logger.error(f"Failed to collect performance metrics: {e}")
            return self.metrics
    
    def calculate_load_time(self, start_time: float, end_time: float) -> float:
        """Calculate load time in milliseconds"""
        return (end_time - start_time) * 1000
    
    def add_api_response_time(self, endpoint: str, response_time: float) -> None:
        """Add API response time to metrics"""
        self.metrics["api_response_times"].append({
            "endpoint": endpoint,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_resource_load_time(self, resource_url: str, load_time: float) -> None:
        """Add resource load time to metrics"""
        self.metrics["resource_load_times"][resource_url] = load_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return self.metrics
    
    def is_within_threshold(self, thresholds: Dict[str, float]) -> bool:
        """Check if metrics are within thresholds"""
        results = {}
        
        for metric, threshold in thresholds.items():
            if metric in self.metrics:
                value = self.metrics[metric]
                results[metric] = {
                    "value": value,
                    "threshold": threshold,
                    "passed": value <= threshold
                }
        
        return all(r["passed"] for r in results.values()), results


class PerformanceTestBase:
    """Base class for performance tests"""
    
    def __init__(self, page: Page):
        self.page = page
        self.metrics = PerformanceMetrics()
        self.start_time = None
        self.end_time = None
        self.performance_data = []
    
    @allure.step("Measure page load performance")
    def measure_page_load(self, url: str, wait_for_network_idle: bool = True) -> Dict[str, Any]:
        """Measure page load performance metrics"""
        self.start_time = time.time()
        
        # Navigate to page
        response = self.page.goto(url, wait_until="networkidle" if wait_for_network_idle else "load")
        
        self.end_time = time.time()
        
        # Collect metrics
        self.metrics.collect_from_page(self.page)
        self.metrics.metrics["page_load_time"] = self.metrics.calculate_load_time(
            self.start_time, self.end_time
        )
        self.metrics.metrics["server_response_time"] = response.timing.get("responseEnd", 0) - \
                                                        response.timing.get("requestStart", 0)
        
        # Store performance data
        performance_result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.metrics.to_dict()
        }
        
        self.performance_data.append(performance_result)
        
        # Attach to Allure
        self._attach_metrics_to_allure()
        
        return performance_result
    
    @allure.step("Measure API performance")
    def measure_api_performance(self, api_call, endpoint: str) -> float:
        """Measure API response time"""
        start_time = time.time()
        response = api_call()
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        self.metrics.add_api_response_time(endpoint, response_time)
        
        return response_time
    
    @allure.step("Measure action performance")
    def measure_action_performance(self, action, action_name: str) -> float:
        """Measure performance of a specific action"""
        start_time = time.time()
        result = action()
        end_time = time.time()
        
        action_time = (end_time - start_time) * 1000
        
        self.performance_data.append({
            "action": action_name,
            "time_ms": action_time,
            "timestamp": datetime.now().isoformat()
        })
        
        return action_time, result
    
    @allure.step("Collect resource load times")
    def collect_resource_load_times(self) -> Dict[str, float]:
        """Collect load times for all resources on the page"""
        resources = self.page.evaluate("""() => {
            const resources = performance.getEntriesByType('resource');
            return resources.map(resource => ({
                name: resource.name,
                duration: resource.duration,
                size: resource.transferSize,
                type: resource.initiatorType
            }));
        }""")
        
        for resource in resources:
            self.metrics.add_resource_load_time(resource["name"], resource["duration"])
        
        return resources
    
    @allure.step("Measure rendering performance")
    def measure_rendering_performance(self, selector: str) -> Dict[str, float]:
        """Measure rendering time for specific elements"""
        start_time = time.time()
        
        # Wait for element to appear
        self.page.wait_for_selector(selector, state="visible")
        
        element_appear_time = (time.time() - start_time) * 1000
        
        # Measure element render time
        render_time = self.page.evaluate(f"""
            (selector) => {{
                const element = document.querySelector(selector);
                const start = performance.now();
                element.getBoundingClientRect();
                return performance.now() - start;
            }}
        """, selector)
        
        return {
            "element_appear_time_ms": element_appear_time,
            "element_render_time_ms": render_time
        }
    
    def _attach_metrics_to_allure(self):
        """Attach performance metrics to Allure report"""
        metrics = self.metrics.to_dict()
        
        # Create formatted metrics string
        metrics_text = "### Performance Metrics\n\n"
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if "time" in key or "load" in key:
                    metrics_text += f"- **{key}**: {value:.2f} ms\n"
                else:
                    metrics_text += f"- **{key}**: {value}\n"
        
        allure.attach(metrics_text, name="Performance Metrics", 
                     attachment_type=allure.attachment_type.MARKDOWN)
    
    def assert_performance_threshold(self, thresholds: Dict[str, float]) -> bool:
        """Assert that performance metrics are within thresholds"""
        passed, results = self.metrics.is_within_threshold(thresholds)
        
        # Create assertion report
        report = "### Performance Threshold Check\n\n"
        for metric, data in results.items():
            status = "✅ PASSED" if data["passed"] else "❌ FAILED"
            report += f"- **{metric}**: {data['value']:.2f} ms / {data['threshold']} ms - {status}\n"
        
        allure.attach(report, name="Threshold Results", 
                     attachment_type=allure.attachment_type.MARKDOWN)
        
        assert passed, f"Performance metrics exceeded thresholds: {results}"
        return passed