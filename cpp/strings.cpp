#include <iostream>
#include <string>
#include <regex>
#include <chrono>
#include <algorithm>

// Reverse a string
std::string reverse_string(const std::string& s) {
    std::string reversed = s;
    std::reverse(reversed.begin(), reversed.end());
    return reversed;
}

// Concatenate strings multiple times
std::string concatenate_strings(int iterations) {
    std::string result;
    for (int i = 0; i < iterations; i++) {
        result += std::to_string(i);
    }
    return result;
}

// Search for pattern in text using regex
int pattern_search(const std::string& text, const std::string& pattern) {
    std::regex re(pattern);
    auto words_begin = std::sregex_iterator(text.begin(), text.end(), re);
    auto words_end = std::sregex_iterator();
    return std::distance(words_begin, words_end);
}

// Run string manipulation benchmarks
void run_benchmark() {
    // String reversal on 1 million character string
    std::string large_string(1000000, 'a');
    auto start_time = std::chrono::high_resolution_clock::now();
    std::string reversed = reverse_string(large_string);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto execution_time_reverse = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: String Reversal (1M chars)" << std::endl;
    std::cout << "Execution time: " << execution_time_reverse << " ms" << std::endl;
    std::cout << "String length: " << large_string.length() << std::endl;
    std::cout << std::endl;

    // String concatenation (10,000 iterations)
    start_time = std::chrono::high_resolution_clock::now();
    std::string concatenated = concatenate_strings(10000);
    end_time = std::chrono::high_resolution_clock::now();
    auto execution_time_concat = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: String Concatenation (10K iterations)" << std::endl;
    std::cout << "Execution time: " << execution_time_concat << " ms" << std::endl;
    std::cout << "Result length: " << concatenated.length() << std::endl;
    std::cout << std::endl;

    // Pattern searching
    std::string text;
    for (int i = 0; i < 10000; i++) {
        text += "Lorem ipsum dolor sit amet ";
    }
    std::string pattern = R"(\b\w{5}\b)"; // Find all 5-letter words
    start_time = std::chrono::high_resolution_clock::now();
    int matches = pattern_search(text, pattern);
    end_time = std::chrono::high_resolution_clock::now();
    auto execution_time_search = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: Pattern Search" << std::endl;
    std::cout << "Execution time: " << execution_time_search << " ms" << std::endl;
    std::cout << "Matches found: " << matches << std::endl;
}

int main() {
    run_benchmark();
    return 0;
}
