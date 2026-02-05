import random
import time

def quicksort(arr):
    """
    Quicksort algorithm implementation.
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

def run_benchmark():
    """
    Run sorting benchmark with 100,000 random integers.
    """
    # Generate 100,000 random integers
    arr = [random.randint(0, 1000000) for _ in range(100000)]
    
    # Measure sorting time
    start_time = time.time()
    sorted_arr = quicksort(arr)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Verify sorting correctness
    is_sorted = all(sorted_arr[i] <= sorted_arr[i+1] for i in range(len(sorted_arr)-1))
    
    return {
        'test_name': 'Sorting (Quicksort)',
        'execution_time_ms': execution_time,
        'size': len(arr),
        'correct': is_sorted
    }

if __name__ == '__main__':
    result = run_benchmark()
    print(f"Test: {result['test_name']}")
    print(f"Array size: {result['size']}")
    print(f"Execution time: {result['execution_time_ms']:.2f} ms")
    print(f"Correctly sorted: {result['correct']}")
