package main

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Go Performance Benchmarks")
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println()

	// Sorting
	fmt.Println("Running Sorting Benchmark...")
	RunSortingBenchmark()
	fmt.Println()

	// Fibonacci
	fmt.Println("Running Fibonacci Benchmarks...")
	RunFibonacciBenchmark()
	fmt.Println()

	// Matrix
	fmt.Println("Running Matrix Multiplication Benchmark...")
	RunMatrixBenchmark()
	fmt.Println()

	// Strings
	fmt.Println("Running String Manipulation Benchmarks...")
	RunStringsBenchmark()
	fmt.Println()

	// API Requests
	fmt.Println("Running API Request Benchmark...")
	RunAPIBenchmark()
	fmt.Println()

	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("All benchmarks completed!")
	fmt.Println(strings.Repeat("=", 60))
}
