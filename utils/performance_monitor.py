"""
Performance Monitoring Utilities
"""
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import statistics
from utils.logger import logger


class PerformanceMonitor:
    """Monitor and track performance metrics over time"""
    
    def __init__(self):
        self.metrics_history = []
        self.current_session = None
    
    def start_session(self, session_name: str) -> None:
        """Start a performance monitoring session"""
        self.current_session = {
            "name": session_name,
            "start_time": datetime.now(),
            "metrics": []
        }
        logger.info(f"Started performance session: {session_name}")
    
    def end_session(self) -> Dict[str, Any]:
        """End the current performance session"""
        if self.current_session:
            self.current_session["end_time"] = datetime.now()
            self.current_session["duration"] = (
                self.current_session["end_time"] - self.current_session["start_time"]
            ).total_seconds()
            
            # Calculate statistics
            session_metrics = self.current_session["metrics"]
            if session_metrics:
                response_times = [m.get("response_time", 0) for m in session_metrics]
                self.current_session["statistics"] = {
                    "min": min(response_times),
                    "max": max(response_times),
                    "avg": statistics.mean(response_times),
                    "median": statistics.median(response_times),
                    "p95": self._percentile(response_times, 95),
                    "p99": self._percentile(response_times, 99),
                    "count": len(response_times)
                }
            
            self.metrics_history.append(self.current_session)
            logger.info(f"Ended performance session: {self.current_session['name']}")
            
            return self.current_session
        
        return {}
    
    def record_metric(self, metric_name: str, value: float, unit: str = "ms") -> None:
        """Record a single metric"""
        metric = {
            "name": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.now()
        }
        
        if self.current_session:
            self.current_session["metrics"].append(metric)
        else:
            logger.warning("No active session to record metric")
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def generate_report(self) -> str:
        """Generate performance report"""
        report = "# Performance Monitoring Report\n\n"
        
        for session in self.metrics_history:
            report += f"## Session: {session['name']}\n"
            report += f"- **Start Time**: {session['start_time']}\n"
            report += f"- **End Time**: {session['end_time']}\n"
            report += f"- **Duration**: {session['duration']:.2f} seconds\n"
            
            if "statistics" in session:
                report += "\n### Statistics\n"
                stats = session["statistics"]
                report += f"- **Min Response Time**: {stats['min']:.2f} ms\n"
                report += f"- **Max Response Time**: {stats['max']:.2f} ms\n"
                report += f"- **Average Response Time**: {stats['avg']:.2f} ms\n"
                report += f"- **Median Response Time**: {stats['median']:.2f} ms\n"
                report += f"- **95th Percentile**: {stats['p95']:.2f} ms\n"
                report += f"- **99th Percentile**: {stats['p99']:.2f} ms\n"
                report += f"- **Total Requests**: {stats['count']}\n"
            
            report += "\n---\n\n"
        
        return report


class LoadTestSimulator:
    """Simulate load on the application"""
    
    def __init__(self):
        self.results = []
    
    def simulate_concurrent_users(self, user_count: int, action, *args, **kwargs) -> List[float]:
        """Simulate multiple concurrent users performing an action"""
        import concurrent.futures
        
        def execute_action():
            start_time = time.time()
            result = action(*args, **kwargs)
            end_time = time.time()
            return (end_time - start_time) * 1000, result
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=user_count) as executor:
            futures = [executor.submit(execute_action) for _ in range(user_count)]
            results = [f.result() for f in futures]
        
        response_times = [r[0] for r in results]
        
        load_test_result = {
            "user_count": user_count,
            "response_times": response_times,
            "min": min(response_times),
            "max": max(response_times),
            "avg": statistics.mean(response_times),
            "median": statistics.median(response_times),
            "p95": self._percentile(response_times, 95),
            "p99": self._percentile(response_times, 99),
            "success_count": sum(1 for r in results if r[1] is not None),
            "failure_count": sum(1 for r in results if r[1] is None)
        }
        
        self.results.append(load_test_result)
        return load_test_result
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def generate_load_test_report(self) -> str:
        """Generate load test report"""
        report = "# Load Test Report\n\n"
        
        for result in self.results:
            report += f"## Concurrent Users: {result['user_count']}\n"
            report += f"- **Min Response Time**: {result['min']:.2f} ms\n"
            report += f"- **Max Response Time**: {result['max']:.2f} ms\n"
            report += f"- **Average Response Time**: {result['avg']:.2f} ms\n"
            report += f"- **Median Response Time**: {result['median']:.2f} ms\n"
            report += f"- **95th Percentile**: {result['p95']:.2f} ms\n"
            report += f"- **99th Percentile**: {result['p99']:.2f} ms\n"
            report += f"- **Success Rate**: {result['success_count']}/{result['user_count']} ({result['success_count']/result['user_count']*100:.1f}%)\n"
            report += "\n---\n\n"
        
        return report