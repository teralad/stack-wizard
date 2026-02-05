"""
Python API Request Performance Test
Uses asyncio and aiohttp for efficient concurrent HTTP requests.
Collects comprehensive metrics including response times, throughput, and percentiles.
"""

import asyncio
import aiohttp
import time
import json
import statistics
from pathlib import Path

async def make_request(session, url, request_id, start_time):
    """
    Make a single HTTP request asynchronously.
    Returns timing data for the request.
    """
    request_start = time.time()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            await response.text()  # Read response body
            request_end = time.time()
            return {
                'id': request_id,
                'success': response.status == 200,
                'response_time_ms': (request_end - request_start) * 1000,
                'timestamp': request_end - start_time
            }
    except Exception as e:
        request_end = time.time()
        return {
            'id': request_id,
            'success': False,
            'response_time_ms': (request_end - request_start) * 1000,
            'timestamp': request_end - start_time,
            'error': str(e)
        }

async def run_benchmark():
    """
    Run API request benchmark with 1,000 concurrent requests.
    Uses aiohttp for async HTTP requests with connection pooling.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"
    num_requests = 1000
    
    print(f"Starting benchmark: {num_requests} requests to {url}")
    
    # Measure total time for concurrent requests
    start_time = time.time()
    
    # Create a connection pool with appropriate limits
    connector = aiohttp.TCPConnector(limit=50, limit_per_host=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [make_request(session, url, i, start_time) for i in range(num_requests)]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    successful_count = len(successful_results)
    failed_count = len(failed_results)
    
    # Extract response times from successful requests
    response_times = [r['response_time_ms'] for r in successful_results]
    
    # Calculate metrics
    if response_times:
        sorted_times = sorted(response_times)
        metrics = {
            'language': 'python',
            'total_requests': num_requests,
            'successful_requests': successful_count,
            'failed_requests': failed_count,
            'total_time_seconds': round(total_time, 2),
            'requests_per_second': round(num_requests / total_time, 2),
            'response_times': {
                'min_ms': round(min(response_times), 2),
                'max_ms': round(max(response_times), 2),
                'average_ms': round(statistics.mean(response_times), 2),
                'median_ms': round(statistics.median(response_times), 2),
                'p95_ms': round(sorted_times[int(len(sorted_times) * 0.95)], 2),
                'p99_ms': round(sorted_times[int(len(sorted_times) * 0.99)], 2)
            },
            'timeseries': [
                {
                    'timestamp': round(r['timestamp'], 3),
                    'response_time_ms': round(r['response_time_ms'], 2)
                }
                for r in successful_results
            ]
        }
    else:
        metrics = {
            'language': 'python',
            'total_requests': num_requests,
            'successful_requests': 0,
            'failed_requests': failed_count,
            'total_time_seconds': round(total_time, 2),
            'requests_per_second': 0,
            'response_times': {},
            'timeseries': []
        }
    
    # Save results to JSON file
    output_file = Path(__file__).parent / 'api_results.json'
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    
    return metrics

def print_results(metrics):
    """Print formatted results to console."""
    print(f"\n{'='*60}")
    print(f"Language: {metrics['language'].upper()}")
    print(f"{'='*60}")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Successful: {metrics['successful_requests']}")
    print(f"Failed: {metrics['failed_requests']}")
    print(f"Total Time: {metrics['total_time_seconds']:.2f}s")
    print(f"Requests/sec: {metrics['requests_per_second']:.2f}")
    
    if metrics['response_times']:
        print(f"\nResponse Times (ms):")
        print(f"  Min: {metrics['response_times']['min_ms']:.2f}")
        print(f"  Max: {metrics['response_times']['max_ms']:.2f}")
        print(f"  Avg: {metrics['response_times']['average_ms']:.2f}")
        print(f"  Median: {metrics['response_times']['median_ms']:.2f}")
        print(f"  P95: {metrics['response_times']['p95_ms']:.2f}")
        print(f"  P99: {metrics['response_times']['p99_ms']:.2f}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    metrics = asyncio.run(run_benchmark())
    print_results(metrics)
