/**
 * C++ API Request Performance Test
 * Uses libcurl with threads for concurrent HTTP requests.
 * Collects comprehensive metrics including response times, throughput, and percentiles.
 */

#include <iostream>
#include <curl/curl.h>
#include <vector>
#include <thread>
#include <chrono>
#include <atomic>
#include <mutex>
#include <algorithm>
#include <numeric>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cmath>

struct RequestResult {
    int id;
    bool success;
    double response_time_ms;
    double timestamp;
    std::string error;
};

// Callback function for curl to write data
size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    return size * nmemb;
}

// Make a single HTTP request with timing
RequestResult make_request(const std::string& url, int request_id, 
                          std::chrono::high_resolution_clock::time_point start_time) {
    auto request_start = std::chrono::high_resolution_clock::now();
    
    CURL* curl = curl_easy_init();
    RequestResult result;
    result.id = request_id;
    result.success = false;
    
    if (!curl) {
        auto request_end = std::chrono::high_resolution_clock::now();
        result.response_time_ms = std::chrono::duration<double, std::milli>(request_end - request_start).count();
        result.timestamp = std::chrono::duration<double>(request_end - start_time).count();
        result.error = "Failed to initialize curl";
        return result;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    CURLcode res = curl_easy_perform(curl);
    
    auto request_end = std::chrono::high_resolution_clock::now();
    
    long response_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    curl_easy_cleanup(curl);
    
    result.response_time_ms = std::chrono::duration<double, std::milli>(request_end - request_start).count();
    result.timestamp = std::chrono::duration<double>(request_end - start_time).count();
    result.success = (res == CURLE_OK && response_code == 200);
    
    if (res != CURLE_OK) {
        result.error = curl_easy_strerror(res);
    }

    return result;
}

// Calculate percentile from sorted vector
double percentile(const std::vector<double>& sorted_data, double p) {
    if (sorted_data.empty()) {
        return 0.0;
    }
    size_t index = static_cast<size_t>(std::ceil(sorted_data.size() * p)) - 1;
    index = std::min(index, sorted_data.size() - 1);
    return sorted_data[index];
}

// Helper to round to 2 decimal places
double round2(double value) {
    return std::round(value * 100.0) / 100.0;
}

double round3(double value) {
    return std::round(value * 1000.0) / 1000.0;
}

// Simple JSON string builder (to avoid external dependencies)
std::string build_json(const std::vector<RequestResult>& results, int total_requests,
                       double total_time_seconds) {
    std::vector<RequestResult> successful_results;
    for (const auto& r : results) {
        if (r.success) {
            successful_results.push_back(r);
        }
    }
    
    int successful_count = successful_results.size();
    int failed_count = total_requests - successful_count;
    
    std::ostringstream json;
    json << std::fixed << std::setprecision(2);
    
    json << "{\n";
    json << "  \"language\": \"cpp\",\n";
    json << "  \"total_requests\": " << total_requests << ",\n";
    json << "  \"successful_requests\": " << successful_count << ",\n";
    json << "  \"failed_requests\": " << failed_count << ",\n";
    json << "  \"total_time_seconds\": " << round2(total_time_seconds) << ",\n";
    json << "  \"requests_per_second\": " << round2(total_requests / total_time_seconds) << ",\n";
    
    if (!successful_results.empty()) {
        std::vector<double> response_times;
        for (const auto& r : successful_results) {
            response_times.push_back(r.response_time_ms);
        }
        std::sort(response_times.begin(), response_times.end());
        
        double sum = std::accumulate(response_times.begin(), response_times.end(), 0.0);
        double min_val = response_times.front();
        double max_val = response_times.back();
        double avg_val = sum / response_times.size();
        
        json << "  \"response_times\": {\n";
        json << "    \"min_ms\": " << round2(min_val) << ",\n";
        json << "    \"max_ms\": " << round2(max_val) << ",\n";
        json << "    \"average_ms\": " << round2(avg_val) << ",\n";
        json << "    \"median_ms\": " << round2(percentile(response_times, 0.5)) << ",\n";
        json << "    \"p95_ms\": " << round2(percentile(response_times, 0.95)) << ",\n";
        json << "    \"p99_ms\": " << round2(percentile(response_times, 0.99)) << "\n";
        json << "  },\n";
        
        json << "  \"timeseries\": [\n";
        for (size_t i = 0; i < successful_results.size(); ++i) {
            json << "    {\"timestamp\": " << round3(successful_results[i].timestamp) 
                 << ", \"response_time_ms\": " << round2(successful_results[i].response_time_ms) << "}";
            if (i < successful_results.size() - 1) {
                json << ",";
            }
            json << "\n";
        }
        json << "  ]\n";
    } else {
        json << "  \"response_times\": {},\n";
        json << "  \"timeseries\": []\n";
    }
    
    json << "}\n";
    
    return json.str();
}

void print_results(const std::vector<RequestResult>& results, int total_requests,
                   double total_time_seconds) {
    std::vector<RequestResult> successful_results;
    for (const auto& r : results) {
        if (r.success) {
            successful_results.push_back(r);
        }
    }
    
    int successful_count = successful_results.size();
    int failed_count = total_requests - successful_count;
    
    std::cout << "\n" << std::string(60, '=') << std::endl;
    std::cout << "Language: C++" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    std::cout << "Total Requests: " << total_requests << std::endl;
    std::cout << "Successful: " << successful_count << std::endl;
    std::cout << "Failed: " << failed_count << std::endl;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Total Time: " << total_time_seconds << "s" << std::endl;
    std::cout << "Requests/sec: " << (total_requests / total_time_seconds) << std::endl;
    
    if (!successful_results.empty()) {
        std::vector<double> response_times;
        for (const auto& r : successful_results) {
            response_times.push_back(r.response_time_ms);
        }
        std::sort(response_times.begin(), response_times.end());
        
        double sum = std::accumulate(response_times.begin(), response_times.end(), 0.0);
        double min_val = response_times.front();
        double max_val = response_times.back();
        double avg_val = sum / response_times.size();
        
        std::cout << "\nResponse Times (ms):" << std::endl;
        std::cout << "  Min: " << min_val << std::endl;
        std::cout << "  Max: " << max_val << std::endl;
        std::cout << "  Avg: " << avg_val << std::endl;
        std::cout << "  Median: " << percentile(response_times, 0.5) << std::endl;
        std::cout << "  P95: " << percentile(response_times, 0.95) << std::endl;
        std::cout << "  P99: " << percentile(response_times, 0.99) << std::endl;
    }
    std::cout << std::string(60, '=') << "\n" << std::endl;
}

// Run API request benchmark with 1,000 concurrent requests
void run_benchmark() {
    curl_global_init(CURL_GLOBAL_DEFAULT);
    
    std::string url = "https://jsonplaceholder.typicode.com/posts/1";
    int num_requests = 1000;

    std::cout << "Starting benchmark: " << num_requests << " requests to " << url << std::endl;

    // Measure total time for concurrent requests
    auto start_time = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    std::vector<RequestResult> results;
    std::mutex results_mutex;

    // Create threads for concurrent requests
    for (int i = 0; i < num_requests; i++) {
        threads.emplace_back([&url, i, start_time, &results, &results_mutex]() {
            RequestResult result = make_request(url, i, start_time);
            std::lock_guard<std::mutex> lock(results_mutex);
            results.push_back(result);
        });
    }

    // Wait for all threads to complete
    for (auto& thread : threads) {
        thread.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    double total_time = std::chrono::duration<double>(end_time - start_time).count();

    // Build and save JSON
    std::string json_data = build_json(results, num_requests, total_time);
    
    std::ofstream output_file("api_results.json");
    if (output_file.is_open()) {
        output_file << json_data;
        output_file.close();
        std::cout << "\nResults saved to api_results.json" << std::endl;
    } else {
        std::cerr << "Error: Could not write to api_results.json" << std::endl;
    }

    // Print results
    print_results(results, num_requests, total_time);

    curl_global_cleanup();
}

int main() {
    run_benchmark();
    return 0;
}
