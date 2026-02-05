using System;
using System.Diagnostics;
using System.Linq;

namespace StackWizard
{
    /// <summary>
    /// Matrix multiplication implementation for performance benchmarking.
    /// Tests with two 100x100 matrices.
    /// </summary>
    public class Matrix
    {
        /// <summary>
        /// Generate a random matrix of given dimensions.
        /// </summary>
        public static double[,] GenerateRandomMatrix(int rows, int cols)
        {
            var random = new Random();
            var matrix = new double[rows, cols];
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    matrix[i, j] = random.NextDouble() * 100;
                }
            }
            return matrix;
        }

        /// <summary>
        /// Multiply two matrices using standard algorithm.
        /// </summary>
        public static double[,] Multiply(double[,] matrixA, double[,] matrixB)
        {
            int rowsA = matrixA.GetLength(0);
            int colsA = matrixA.GetLength(1);
            int colsB = matrixB.GetLength(1);

            var result = new double[rowsA, colsB];

            for (int i = 0; i < rowsA; i++)
            {
                for (int j = 0; j < colsB; j++)
                {
                    double sum = 0;
                    for (int k = 0; k < colsA; k++)
                    {
                        sum += matrixA[i, k] * matrixB[k, j];
                    }
                    result[i, j] = sum;
                }
            }

            return result;
        }

        /// <summary>
        /// Run matrix multiplication benchmark with 100x100 matrices.
        /// </summary>
        public static void RunBenchmark()
        {
            int size = 100;

            // Generate two random matrices
            var matrixA = GenerateRandomMatrix(size, size);
            var matrixB = GenerateRandomMatrix(size, size);

            // Measure multiplication time
            var watch = Stopwatch.StartNew();
            var resultMatrix = Multiply(matrixA, matrixB);
            watch.Stop();

            double executionTime = watch.Elapsed.TotalMilliseconds;

            Console.WriteLine("\n=== Matrix Multiplication Benchmark ===");
            Console.WriteLine($"Matrix size: {size}x{size}");
            Console.WriteLine($"Execution time: {executionTime:F2} ms");
            Console.WriteLine($"Result dimensions: {resultMatrix.GetLength(0)}x{resultMatrix.GetLength(1)}");
        }
    }
}
