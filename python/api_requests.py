import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_request(url, request_id):
    """
    Make a single HTTP request.
    """
    try:
        response = requests.get(url, timeout=10)
        return {
            'id': request_id,
            'status': response.status_code,
            'success': response.status_code == 200
        }
    except Exception as e:
        return {
            'id': request_id,
            'status': 0,
            'success': False,
            'error': str(e)
        }

def run_benchmark():
    """
    Run API request benchmark with 50 concurrent requests.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"
    num_requests = 50
    
    # Measure total time for concurrent requests
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, url, i) for i in range(num_requests)]
        results = [future.result() for future in as_completed(futures)]
    
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Count successful requests
    successful = sum(1 for r in results if r['success'])
    
    return {
        'test_name': 'API Requests (50 concurrent)',
        'execution_time_ms': execution_time,
        'total_requests': num_requests,
        'successful_requests': successful
    }

if __name__ == '__main__':
    result = run_benchmark()
    print(f"Test: {result['test_name']}")
    print(f"Total requests: {result['total_requests']}")
    print(f"Successful requests: {result['successful_requests']}")
    print(f"Execution time: {result['execution_time_ms']:.2f} ms")
