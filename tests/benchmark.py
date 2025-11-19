#!/usr/bin/env python3
"""
📊 Performance Benchmarking Tool
Measures API endpoint performance and generates reports
"""

import statistics
import time
from datetime import datetime
from typing import Dict

import requests

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def benchmark_endpoint(
    url: str, method: str = "GET", data: Dict = None, iterations: int = 10
) -> Dict:
    """Benchmark single endpoint"""
    times = []
    errors = 0

    for _ in range(iterations):
        try:
            start = time.time()

            if method == "GET":
                response = requests.get(url, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=30)

            elapsed = (time.time() - start) * 1000  # Convert to ms

            if response.status_code == 200:
                times.append(elapsed)
            else:
                errors += 1

        except Exception:
            errors += 1

    if not times:
        return {"success": False, "error_rate": 100.0}

    return {
        "success": True,
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "error_rate": (errors / iterations) * 100,
    }


def print_benchmark_result(name: str, result: Dict):
    """Pretty print benchmark result"""
    if not result["success"]:
        print(f"{RED}❌ {name}: FAILED (100% errors){RESET}")
        return

    mean = result["mean"]

    # Determine color based on performance
    if mean < 200:
        color = GREEN
        status = "Excellent"
    elif mean < 500:
        color = GREEN
        status = "Good"
    elif mean < 1000:
        color = YELLOW
        status = "Acceptable"
    else:
        color = RED
        status = "Slow"

    print(f"{color}✓ {name}{RESET}")
    print(
        f"  Mean: {mean:.0f}ms | Median: {result['median']:.0f}ms | "
        f"Min: {result['min']:.0f}ms | Max: {result['max']:.0f}ms"
    )
    print(
        f"  Std Dev: {result['stdev']:.0f}ms | Error Rate: {result['error_rate']:.0f}% | "
        f"Status: {color}{status}{RESET}"
    )
    print()


def run_benchmark(base_url: str, iterations: int = 10):
    """Run comprehensive benchmark"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}📊 NovaHouse Chatbot - Performance Benchmark{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    print(f"Target: {base_url}")
    print(f"Iterations per endpoint: {iterations}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    endpoints = [
        ("Health Check", "GET", "/api/health", None),
        ("Packages", "GET", "/api/packages", None),
        ("FAQ", "GET", "/api/faq", None),
        ("Portfolio", "GET", "/api/portfolio", None),
        ("Reviews", "GET", "/api/reviews", None),
        ("Partners", "GET", "/api/partners", None),
        ("Search", "GET", "/api/search?q=wykończenia", None),
        ("Chat", "POST", "/api/chat", {"message": "Witaj"}),
    ]

    results = {}

    for name, method, endpoint, data in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"Benchmarking: {name}...")
        result = benchmark_endpoint(url, method, data, iterations)
        results[name] = result
        print_benchmark_result(name, result)

    # Summary
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}📈 Summary{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    successful = [r for r in results.values() if r["success"]]
    if successful:
        avg_mean = statistics.mean([r["mean"] for r in successful])
        avg_error_rate = statistics.mean([r["error_rate"] for r in successful])

        print(f"Average Response Time: {avg_mean:.0f}ms")
        print(f"Average Error Rate: {avg_error_rate:.1f}%")

        if avg_mean < 500 and avg_error_rate < 5:
            print(f"\n{GREEN}🎉 Performance: Excellent!{RESET}")
        elif avg_mean < 1000 and avg_error_rate < 10:
            print(f"\n{YELLOW}⚠️  Performance: Acceptable{RESET}")
        else:
            print(f"\n{RED}🚨 Performance: Needs Improvement{RESET}")
    else:
        print(f"{RED}❌ All endpoints failed{RESET}")

    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <base_url> [iterations]")
        print("\nExamples:")
        print("  python benchmark.py https://glass-core-467907-e9.ey.r.appspot.com")
        print("  python benchmark.py http://localhost:8080 20")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    run_benchmark(base_url, iterations)
