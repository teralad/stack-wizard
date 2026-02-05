package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

// Make a single HTTP request
func makeRequest(url string, requestID int, wg *sync.WaitGroup, results chan<- map[string]interface{}) {
	defer wg.Done()

	resp, err := http.Get(url)
	if err != nil {
		results <- map[string]interface{}{
			"id":      requestID,
			"status":  0,
			"success": false,
		}
		return
	}
	defer resp.Body.Close()

	results <- map[string]interface{}{
		"id":      requestID,
		"status":  resp.StatusCode,
		"success": resp.StatusCode == 200,
	}
}

// RunAPIBenchmark runs API request benchmark with 50 concurrent requests
func RunAPIBenchmark() {
	url := "https://jsonplaceholder.typicode.com/posts/1"
	numRequests := 50

	// Measure total time for concurrent requests
	startTime := time.Now()

	var wg sync.WaitGroup
	results := make(chan map[string]interface{}, numRequests)

	for i := 0; i < numRequests; i++ {
		wg.Add(1)
		go makeRequest(url, i, &wg, results)
	}

	wg.Wait()
	close(results)

	executionTime := time.Since(startTime).Milliseconds()

	// Count successful requests
	successful := 0
	for result := range results {
		if result["success"].(bool) {
			successful++
		}
	}

	fmt.Printf("Test: API Requests (50 concurrent)\n")
	fmt.Printf("Total requests: %d\n", numRequests)
	fmt.Printf("Successful requests: %d\n", successful)
	fmt.Printf("Execution time: %d ms\n", executionTime)
}
