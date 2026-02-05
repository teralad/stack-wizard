#include <iostream>
#include <curl/curl.h>
#include <vector>
#include <thread>
#include <chrono>
#include <atomic>

// Callback function for curl to write data
size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    return size * nmemb;
}

// Make a single HTTP request
bool make_request(const std::string& url) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        return false;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

    CURLcode res = curl_easy_perform(curl);
    
    long response_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    
    curl_easy_cleanup(curl);

    return (res == CURLE_OK && response_code == 200);
}

// Run API request benchmark with 50 concurrent requests
void run_benchmark() {
    curl_global_init(CURL_GLOBAL_DEFAULT);
    
    std::string url = "https://jsonplaceholder.typicode.com/posts/1";
    int num_requests = 50;

    // Measure total time for concurrent requests
    auto start_time = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    std::atomic<int> successful(0);

    for (int i = 0; i < num_requests; i++) {
        threads.emplace_back([&url, &successful]() {
            if (make_request(url)) {
                successful++;
            }
        });
    }

    for (auto& thread : threads) {
        thread.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    auto execution_time = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Test: API Requests (50 concurrent)" << std::endl;
    std::cout << "Total requests: " << num_requests << std::endl;
    std::cout << "Successful requests: " << successful.load() << std::endl;
    std::cout << "Execution time: " << execution_time << " ms" << std::endl;

    curl_global_cleanup();
}

int main() {
    run_benchmark();
    return 0;
}
