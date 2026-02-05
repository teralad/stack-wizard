#!/usr/bin/env python3
"""
Run all Python benchmarks.
"""
import sorting
import fibonacci
import matrix
import strings
import api_requests

def main():
    print("=" * 60)
    print("Python Performance Benchmarks")
    print("=" * 60)
    print()
    
    # Sorting
    print("Running Sorting Benchmark...")
    result = sorting.run_benchmark()
    print(f"  {result['test_name']}: {result['execution_time_ms']:.2f} ms")
    print()
    
    # Fibonacci
    print("Running Fibonacci Benchmarks...")
    results = fibonacci.run_benchmark()
    for result in results:
        print(f"  {result['test_name']}: {result['execution_time_ms']:.2f} ms")
    print()
    
    # Matrix
    print("Running Matrix Multiplication Benchmark...")
    result = matrix.run_benchmark()
    print(f"  {result['test_name']}: {result['execution_time_ms']:.2f} ms")
    print()
    
    # Strings
    print("Running String Manipulation Benchmarks...")
    results = strings.run_benchmark()
    for result in results:
        print(f"  {result['test_name']}: {result['execution_time_ms']:.2f} ms")
    print()
    
    # API Requests
    print("Running API Request Benchmark...")
    result = api_requests.run_benchmark()
    print(f"  {result['test_name']}: {result['execution_time_ms']:.2f} ms")
    print(f"  Successful: {result['successful_requests']}/{result['total_requests']}")
    print()
    
    print("=" * 60)
    print("All benchmarks completed!")
    print("=" * 60)

if __name__ == '__main__':
    main()
