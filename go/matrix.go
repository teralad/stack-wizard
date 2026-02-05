package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Matrix multiplication implementation
func matrixMultiply(matrixA, matrixB [][]float64) [][]float64 {
	rowsA := len(matrixA)
	colsA := len(matrixA[0])
	colsB := len(matrixB[0])

	// Initialize result matrix with zeros
	result := make([][]float64, rowsA)
	for i := range result {
		result[i] = make([]float64, colsB)
	}

	// Perform multiplication
	for i := 0; i < rowsA; i++ {
		for j := 0; j < colsB; j++ {
			for k := 0; k < colsA; k++ {
				result[i][j] += matrixA[i][k] * matrixB[k][j]
			}
		}
	}

	return result
}

// RunMatrixBenchmark runs matrix multiplication benchmark with 100x100 matrices
func RunMatrixBenchmark() {
	size := 100

	// Generate two random 100x100 matrices
	matrixA := make([][]float64, size)
	matrixB := make([][]float64, size)
	for i := 0; i < size; i++ {
		matrixA[i] = make([]float64, size)
		matrixB[i] = make([]float64, size)
		for j := 0; j < size; j++ {
			matrixA[i][j] = rand.Float64()
			matrixB[i][j] = rand.Float64()
		}
	}

	// Measure multiplication time
	startTime := time.Now()
	result := matrixMultiply(matrixA, matrixB)
	executionTime := time.Since(startTime).Milliseconds()

	fmt.Printf("Test: Matrix Multiplication\n")
	fmt.Printf("Matrix size: %dx%d\n", size, size)
	fmt.Printf("Execution time: %d ms\n", executionTime)
	fmt.Printf("Result sample (0,0): %.6f\n", result[0][0])
}
