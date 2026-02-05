#include <iostream>
#include <chrono>

// Recursive Fibonacci implementation
long long fibonacci_recursive(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2);
}

// Iterative Fibonacci implementation
long long fibonacci_iterative(int n) {
    if (n <= 1) {
        return n;
    }

    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Run Fibonacci benchmarks
void run_benchmark() {
    // Recursive fibonacci(35)
    auto start_time = std::chrono::high_resolution_clock::now();
    long long result_recursive = fibonacci_recursive(35);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto execution_time_recursive = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: Fibonacci Recursive (n=35)" << std::endl;
    std::cout << "Result: " << result_recursive << std::endl;
    std::cout << "Execution time: " << execution_time_recursive << " ms" << std::endl;
    std::cout << std::endl;

    // Iterative fibonacci(40)
    start_time = std::chrono::high_resolution_clock::now();
    long long result_iterative = fibonacci_iterative(40);
    end_time = std::chrono::high_resolution_clock::now();
    auto execution_time_iterative = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: Fibonacci Iterative (n=40)" << std::endl;
    std::cout << "Result: " << result_iterative << std::endl;
    std::cout << "Execution time: " << execution_time_iterative << " ms" << std::endl;
}

int main() {
    run_benchmark();
    return 0;
}
