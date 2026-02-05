import time
import re

def reverse_string(s):
    """
    Reverse a string.
    """
    return s[::-1]

def concatenate_strings(iterations):
    """
    Concatenate strings multiple times.
    """
    result = ""
    for i in range(iterations):
        result += str(i)
    return result

def pattern_search(text, pattern):
    """
    Search for pattern in text using regex.
    """
    matches = re.findall(pattern, text)
    return len(matches)

def run_benchmark():
    """
    Run string manipulation benchmarks.
    """
    results = []
    
    # String reversal on 1 million character string
    large_string = "a" * 1000000
    start_time = time.time()
    reversed_str = reverse_string(large_string)
    end_time = time.time()
    execution_time_reverse = (end_time - start_time) * 1000
    
    results.append({
        'test_name': 'String Reversal (1M chars)',
        'execution_time_ms': execution_time_reverse,
        'string_length': len(large_string)
    })
    
    # String concatenation (10,000 iterations)
    start_time = time.time()
    concatenated = concatenate_strings(10000)
    end_time = time.time()
    execution_time_concat = (end_time - start_time) * 1000
    
    results.append({
        'test_name': 'String Concatenation (10K iterations)',
        'execution_time_ms': execution_time_concat,
        'result_length': len(concatenated)
    })
    
    # Pattern searching
    text = "Lorem ipsum dolor sit amet " * 10000
    pattern = r'\b\w{5}\b'  # Find all 5-letter words
    start_time = time.time()
    matches = pattern_search(text, pattern)
    end_time = time.time()
    execution_time_search = (end_time - start_time) * 1000
    
    results.append({
        'test_name': 'Pattern Search',
        'execution_time_ms': execution_time_search,
        'matches_found': matches
    })
    
    return results

if __name__ == '__main__':
    results = run_benchmark()
    for result in results:
        print(f"Test: {result['test_name']}")
        print(f"Execution time: {result['execution_time_ms']:.2f} ms")
        if 'string_length' in result:
            print(f"String length: {result['string_length']}")
        if 'result_length' in result:
            print(f"Result length: {result['result_length']}")
        if 'matches_found' in result:
            print(f"Matches found: {result['matches_found']}")
        print()
