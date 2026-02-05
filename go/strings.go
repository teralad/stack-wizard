package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Reverse a string
func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// Concatenate strings multiple times
func concatenateStrings(iterations int) string {
	var builder strings.Builder
	for i := 0; i < iterations; i++ {
		builder.WriteString(strconv.Itoa(i))
	}
	return builder.String()
}

// Search for pattern in text using regex
func patternSearch(text, pattern string) int {
	re := regexp.MustCompile(pattern)
	matches := re.FindAllString(text, -1)
	return len(matches)
}

// RunStringsBenchmark runs string manipulation benchmarks
func RunStringsBenchmark() {
	// String reversal on 1 million character string
	largeString := strings.Repeat("a", 1000000)
	startTime := time.Now()
	reverseString(largeString)
	executionTimeReverse := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: String Reversal (1M chars)\n")
	fmt.Printf("Execution time: %d ms\n", executionTimeReverse)
	fmt.Printf("String length: %d\n", len(largeString))
	fmt.Println()

	// String concatenation (10,000 iterations)
	startTime = time.Now()
	concatenated := concatenateStrings(10000)
	executionTimeConcat := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: String Concatenation (10K iterations)\n")
	fmt.Printf("Execution time: %d ms\n", executionTimeConcat)
	fmt.Printf("Result length: %d\n", len(concatenated))
	fmt.Println()

	// Pattern searching
	text := strings.Repeat("Lorem ipsum dolor sit amet ", 10000)
	pattern := `\b\w{5}\b` // Find all 5-letter words
	startTime = time.Now()
	matches := patternSearch(text, pattern)
	executionTimeSearch := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: Pattern Search\n")
	fmt.Printf("Execution time: %d ms\n", executionTimeSearch)
	fmt.Printf("Matches found: %d\n", matches)
}
