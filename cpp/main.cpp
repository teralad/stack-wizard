#include <iostream>
#include <string>

// Forward declarations
void run_sorting_benchmark();
void run_fibonacci_benchmark();
void run_matrix_benchmark();
void run_strings_benchmark();
void run_api_benchmark();

int main() {
    std::string separator(60, '=');
    
    std::cout << separator << std::endl;
    std::cout << "C++ Performance Benchmarks" << std::endl;
    std::cout << separator << std::endl;
    std::cout << std::endl;

    std::cout << "Note: This is a combined runner. For individual tests, compile and run:" << std::endl;
    std::cout << "  - sorting.cpp" << std::endl;
    std::cout << "  - fibonacci.cpp" << std::endl;
    std::cout << "  - matrix.cpp" << std::endl;
    std::cout << "  - strings.cpp" << std::endl;
    std::cout << "  - api_requests.cpp" << std::endl;
    std::cout << std::endl;

    std::cout << separator << std::endl;
    std::cout << "Please compile and run each benchmark individually." << std::endl;
    std::cout << "See README.md for compilation instructions." << std::endl;
    std::cout << separator << std::endl;

    return 0;
}
