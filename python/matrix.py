import random
import time

def matrix_multiply(matrix_a, matrix_b):
    """
    Standard matrix multiplication implementation.
    """
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    cols_b = len(matrix_b[0])
    
    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    # Perform multiplication
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    
    return result

def run_benchmark():
    """
    Run matrix multiplication benchmark with 100x100 matrices.
    """
    size = 100
    
    # Generate two random 100x100 matrices
    matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
    matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]
    
    # Measure multiplication time
    start_time = time.time()
    result = matrix_multiply(matrix_a, matrix_b)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    return {
        'test_name': 'Matrix Multiplication',
        'execution_time_ms': execution_time,
        'matrix_size': f'{size}x{size}',
        'result_sample': result[0][0]  # First element as verification
    }

if __name__ == '__main__':
    result = run_benchmark()
    print(f"Test: {result['test_name']}")
    print(f"Matrix size: {result['matrix_size']}")
    print(f"Execution time: {result['execution_time_ms']:.2f} ms")
    print(f"Result sample (0,0): {result['result_sample']:.6f}")
