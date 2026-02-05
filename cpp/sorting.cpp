#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>

// Quicksort algorithm implementation
std::vector<int> quicksort(std::vector<int> arr) {
    if (arr.size() <= 1) {
        return arr;
    }

    int pivot = arr[arr.size() / 2];
    std::vector<int> left, middle, right;

    for (int x : arr) {
        if (x < pivot) {
            left.push_back(x);
        } else if (x == pivot) {
            middle.push_back(x);
        } else {
            right.push_back(x);
        }
    }

    std::vector<int> sorted_left = quicksort(left);
    std::vector<int> sorted_right = quicksort(right);

    std::vector<int> result = sorted_left;
    result.insert(result.end(), middle.begin(), middle.end());
    result.insert(result.end(), sorted_right.begin(), sorted_right.end());

    return result;
}

// Verify if array is sorted
bool is_sorted(const std::vector<int>& arr) {
    for (size_t i = 0; i < arr.size() - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return false;
        }
    }
    return true;
}

// Run sorting benchmark with 100,000 random integers
void run_benchmark() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 999999);

    // Generate 100,000 random integers
    std::vector<int> arr(100000);
    for (int& val : arr) {
        val = dis(gen);
    }

    // Measure sorting time
    auto start_time = std::chrono::high_resolution_clock::now();
    std::vector<int> sorted_arr = quicksort(arr);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto execution_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    // Verify sorting correctness
    bool correct = is_sorted(sorted_arr);

    std::cout << "Test: Sorting (Quicksort)" << std::endl;
    std::cout << "Array size: " << arr.size() << std::endl;
    std::cout << "Execution time: " << execution_time << " ms" << std::endl;
    std::cout << "Correctly sorted: " << (correct ? "true" : "false") << std::endl;
}

int main() {
    run_benchmark();
    return 0;
}
