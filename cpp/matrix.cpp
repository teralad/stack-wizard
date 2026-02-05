#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <iomanip>

// Matrix multiplication implementation
std::vector<std::vector<double>> matrix_multiply(
    const std::vector<std::vector<double>>& matrix_a,
    const std::vector<std::vector<double>>& matrix_b) {
    
    size_t rows_a = matrix_a.size();
    size_t cols_a = matrix_a[0].size();
    size_t cols_b = matrix_b[0].size();

    // Initialize result matrix with zeros
    std::vector<std::vector<double>> result(rows_a, std::vector<double>(cols_b, 0.0));

    // Perform multiplication
    for (size_t i = 0; i < rows_a; i++) {
        for (size_t j = 0; j < cols_b; j++) {
            for (size_t k = 0; k < cols_a; k++) {
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }

    return result;
}

// Run matrix multiplication benchmark with 100x100 matrices
void run_benchmark() {
    const int size = 100;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    // Generate two random 100x100 matrices
    std::vector<std::vector<double>> matrix_a(size, std::vector<double>(size));
    std::vector<std::vector<double>> matrix_b(size, std::vector<double>(size));
    
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            matrix_a[i][j] = dis(gen);
            matrix_b[i][j] = dis(gen);
        }
    }

    // Measure multiplication time
    auto start_time = std::chrono::high_resolution_clock::now();
    auto result = matrix_multiply(matrix_a, matrix_b);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto execution_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: Matrix Multiplication" << std::endl;
    std::cout << "Matrix size: " << size << "x" << size << std::endl;
    std::cout << "Execution time: " << execution_time << " ms" << std::endl;
    std::cout << "Result sample (0,0): " << std::fixed << std::setprecision(6) << result[0][0] << std::endl;
}

int main() {
    run_benchmark();
    return 0;
}
