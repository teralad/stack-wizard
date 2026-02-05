package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Quicksort algorithm implementation
func quicksort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}

	pivot := arr[len(arr)/2]
	var left, middle, right []int

	for _, x := range arr {
		if x < pivot {
			left = append(left, x)
		} else if x == pivot {
			middle = append(middle, x)
		} else {
			right = append(right, x)
		}
	}

	left = quicksort(left)
	right = quicksort(right)

	result := append(left, middle...)
	result = append(result, right...)
	return result
}

// Verify if array is sorted
func isSorted(arr []int) bool {
	for i := 0; i < len(arr)-1; i++ {
		if arr[i] > arr[i+1] {
			return false
		}
	}
	return true
}

// RunSortingBenchmark runs sorting benchmark with 100,000 random integers
func RunSortingBenchmark() {
	// Generate 100,000 random integers
	arr := make([]int, 100000)
	for i := range arr {
		arr[i] = rand.Intn(1000000)
	}

	// Measure sorting time
	startTime := time.Now()
	sortedArr := quicksort(arr)
	executionTime := time.Since(startTime).Milliseconds()

	// Verify sorting correctness
	correct := isSorted(sortedArr)

	fmt.Printf("Test: Sorting (Quicksort)\n")
	fmt.Printf("Array size: %d\n", len(arr))
	fmt.Printf("Execution time: %d ms\n", executionTime)
	fmt.Printf("Correctly sorted: %v\n", correct)
}
