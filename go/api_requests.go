package main

import (
	"encoding/json"
	"fmt"
	"io"
	"math"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"sync"
	"time"
)

// RequestResult holds the result of a single request
type RequestResult struct {
	ID             int     `json:"id"`
	Success        bool    `json:"success"`
	ResponseTimeMs float64 `json:"response_time_ms"`
	Timestamp      float64 `json:"timestamp"`
	Error          string  `json:"error,omitempty"`
}

// Metrics holds all benchmark metrics
type Metrics struct {
	Language           string                   `json:"language"`
	TotalRequests      int                      `json:"total_requests"`
	SuccessfulRequests int                      `json:"successful_requests"`
	FailedRequests     int                      `json:"failed_requests"`
	TotalTimeSeconds   float64                  `json:"total_time_seconds"`
	RequestsPerSecond  float64                  `json:"requests_per_second"`
	ResponseTimes      map[string]float64       `json:"response_times"`
	Timeseries         []map[string]float64     `json:"timeseries"`
}

// Make a single HTTP request with timing
func makeRequest(client *http.Client, url string, requestID int, startTime time.Time, results chan<- RequestResult, wg *sync.WaitGroup) {
	defer wg.Done()

	requestStart := time.Now()
	resp, err := client.Get(url)
	requestEnd := time.Now()

	result := RequestResult{
		ID:             requestID,
		ResponseTimeMs: float64(requestEnd.Sub(requestStart).Microseconds()) / 1000.0,
		Timestamp:      requestEnd.Sub(startTime).Seconds(),
	}

	if err != nil {
		result.Success = false
		result.Error = err.Error()
	} else {
		defer resp.Body.Close()
		io.ReadAll(resp.Body) // Read and discard body
		result.Success = resp.StatusCode == 200
	}

	results <- result
}

// Calculate percentile from sorted slice
func percentile(sortedData []float64, p float64) float64 {
	if len(sortedData) == 0 {
		return 0
	}
	index := int(math.Ceil(float64(len(sortedData)) * p)) - 1
	if index < 0 {
		index = 0
	}
	if index >= len(sortedData) {
		index = len(sortedData) - 1
	}
	return sortedData[index]
}

// RunAPIBenchmark runs API request benchmark with 1,000 concurrent requests
func RunAPIBenchmark() {
	url := "https://jsonplaceholder.typicode.com/posts/1"
	numRequests := 1000

	fmt.Printf("Starting benchmark: %d requests to %s\n", numRequests, url)

	// Create HTTP client with connection pooling
	client := &http.Client{
		Transport: &http.Transport{
			MaxIdleConnsPerHost: 50,
			MaxConnsPerHost:     50,
		},
		Timeout: 10 * time.Second,
	}

	// Measure total time for concurrent requests
	startTime := time.Now()

	var wg sync.WaitGroup
	results := make(chan RequestResult, numRequests)

	for i := 0; i < numRequests; i++ {
		wg.Add(1)
		go makeRequest(client, url, i, startTime, results, &wg)
	}

	wg.Wait()
	close(results)

	endTime := time.Now()
	totalTime := endTime.Sub(startTime).Seconds()

	// Analyze results
	var allResults []RequestResult
	var successfulResults []RequestResult
	var responseTimes []float64

	for result := range results {
		allResults = append(allResults, result)
		if result.Success {
			successfulResults = append(successfulResults, result)
			responseTimes = append(responseTimes, result.ResponseTimeMs)
		}
	}

	successfulCount := len(successfulResults)
	failedCount := len(allResults) - successfulCount

	// Calculate metrics
	metrics := Metrics{
		Language:           "go",
		TotalRequests:      numRequests,
		SuccessfulRequests: successfulCount,
		FailedRequests:     failedCount,
		TotalTimeSeconds:   math.Round(totalTime*100) / 100,
		RequestsPerSecond:  math.Round(float64(numRequests)/totalTime*100) / 100,
		ResponseTimes:      make(map[string]float64),
		Timeseries:         make([]map[string]float64, 0),
	}

	if len(responseTimes) > 0 {
		sort.Float64s(responseTimes)

		sum := 0.0
		minVal := responseTimes[0]
		maxVal := responseTimes[len(responseTimes)-1]
		for _, rt := range responseTimes {
			sum += rt
		}

		metrics.ResponseTimes = map[string]float64{
			"min_ms":     math.Round(minVal*100) / 100,
			"max_ms":     math.Round(maxVal*100) / 100,
			"average_ms": math.Round((sum/float64(len(responseTimes)))*100) / 100,
			"median_ms":  math.Round(percentile(responseTimes, 0.5)*100) / 100,
			"p95_ms":     math.Round(percentile(responseTimes, 0.95)*100) / 100,
			"p99_ms":     math.Round(percentile(responseTimes, 0.99)*100) / 100,
		}

		// Build timeseries data
		for _, result := range successfulResults {
			metrics.Timeseries = append(metrics.Timeseries, map[string]float64{
				"timestamp":        math.Round(result.Timestamp*1000) / 1000,
				"response_time_ms": math.Round(result.ResponseTimeMs*100) / 100,
			})
		}
	}

	// Save results to JSON file
	execPath, _ := os.Executable()
	execDir := filepath.Dir(execPath)
	outputFile := filepath.Join(execDir, "api_results.json")

	// If running with 'go run', use current directory
	if _, err := os.Stat(execDir + "/api_requests.go"); os.IsNotExist(err) {
		outputFile = "api_results.json"
	}

	jsonData, err := json.MarshalIndent(metrics, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling JSON: %v\n", err)
		return
	}

	err = os.WriteFile(outputFile, jsonData, 0644)
	if err != nil {
		fmt.Printf("Error writing file: %v\n", err)
		return
	}

	fmt.Printf("\nResults saved to %s\n", outputFile)

	// Print results
	printResults(metrics)
}

func printResults(metrics Metrics) {
	fmt.Println("\n" + string(make([]byte, 60)))
	for i := range make([]byte, 60) {
		fmt.Print("=")
	}
	fmt.Printf("\nLanguage: %s\n", "GO")
	for i := range make([]byte, 60) {
		fmt.Print("=")
	}
	fmt.Printf("\nTotal Requests: %d\n", metrics.TotalRequests)
	fmt.Printf("Successful: %d\n", metrics.SuccessfulRequests)
	fmt.Printf("Failed: %d\n", metrics.FailedRequests)
	fmt.Printf("Total Time: %.2fs\n", metrics.TotalTimeSeconds)
	fmt.Printf("Requests/sec: %.2f\n", metrics.RequestsPerSecond)

	if len(metrics.ResponseTimes) > 0 {
		fmt.Println("\nResponse Times (ms):")
		fmt.Printf("  Min: %.2f\n", metrics.ResponseTimes["min_ms"])
		fmt.Printf("  Max: %.2f\n", metrics.ResponseTimes["max_ms"])
		fmt.Printf("  Avg: %.2f\n", metrics.ResponseTimes["average_ms"])
		fmt.Printf("  Median: %.2f\n", metrics.ResponseTimes["median_ms"])
		fmt.Printf("  P95: %.2f\n", metrics.ResponseTimes["p95_ms"])
		fmt.Printf("  P99: %.2f\n", metrics.ResponseTimes["p99_ms"])
	}
	for i := range make([]byte, 60) {
		fmt.Print("=")
	}
	fmt.Println()
}

func main() {
	RunAPIBenchmark()
}
