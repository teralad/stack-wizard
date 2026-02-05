package main

import (
	"fmt"
	"time"
)

// Recursive Fibonacci implementation
func fibonacciRecursive(n int) int {
	if n <= 1 {
		return n
	}
	return fibonacciRecursive(n-1) + fibonacciRecursive(n-2)
}

// Iterative Fibonacci implementation
func fibonacciIterative(n int) int {
	if n <= 1 {
		return n
	}

	a, b := 0, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}

// RunFibonacciBenchmark runs Fibonacci benchmarks
func RunFibonacciBenchmark() {
	// Recursive fibonacci(35)
	startTime := time.Now()
	resultRecursive := fibonacciRecursive(35)
	executionTimeRecursive := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: Fibonacci Recursive (n=35)\n")
	fmt.Printf("Result: %d\n", resultRecursive)
	fmt.Printf("Execution time: %d ms\n", executionTimeRecursive)
	fmt.Println()

	// Iterative fibonacci(40)
	startTime = time.Now()
	resultIterative := fibonacciIterative(40)
	executionTimeIterative := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: Fibonacci Iterative (n=40)\n")
	fmt.Printf("Result: %d\n", resultIterative)
	fmt.Printf("Execution time: %d ms\n", executionTimeIterative)
}
