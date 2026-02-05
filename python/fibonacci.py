import time

def fibonacci_recursive(n):
    """
    Recursive Fibonacci implementation.
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n):
    """
    Iterative Fibonacci implementation.
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def run_benchmark():
    """
    Run Fibonacci benchmarks.
    """
    results = []
    
    # Recursive fibonacci(35)
    start_time = time.time()
    result_recursive = fibonacci_recursive(35)
    end_time = time.time()
    execution_time_recursive = (end_time - start_time) * 1000
    
    results.append({
        'test_name': 'Fibonacci Recursive (n=35)',
        'execution_time_ms': execution_time_recursive,
        'result': result_recursive
    })
    
    # Iterative fibonacci(40)
    start_time = time.time()
    result_iterative = fibonacci_iterative(40)
    end_time = time.time()
    execution_time_iterative = (end_time - start_time) * 1000
    
    results.append({
        'test_name': 'Fibonacci Iterative (n=40)',
        'execution_time_ms': execution_time_iterative,
        'result': result_iterative
    })
    
    return results

if __name__ == '__main__':
    results = run_benchmark()
    for result in results:
        print(f"Test: {result['test_name']}")
        print(f"Result: {result['result']}")
        print(f"Execution time: {result['execution_time_ms']:.2f} ms")
        print()
