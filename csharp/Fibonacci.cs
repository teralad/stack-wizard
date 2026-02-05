using System;
using System.Diagnostics;

namespace StackWizard
{
    /// <summary>
    /// Fibonacci calculation implementations for performance benchmarking.
    /// Tests recursive (n=35) and iterative (n=40) approaches.
    /// </summary>
    public class Fibonacci
    {
        /// <summary>
        /// Recursive Fibonacci implementation.
        /// </summary>
        public static long FibRecursive(int n)
        {
            if (n <= 1)
                return n;
            return FibRecursive(n - 1) + FibRecursive(n - 2);
        }

        /// <summary>
        /// Iterative Fibonacci implementation.
        /// </summary>
        public static long FibIterative(int n)
        {
            if (n <= 1)
                return n;

            long a = 0, b = 1;
            for (int i = 2; i <= n; i++)
            {
                long temp = a + b;
                a = b;
                b = temp;
            }
            return b;
        }

        /// <summary>
        /// Run Fibonacci benchmarks.
        /// </summary>
        public static void RunBenchmark()
        {
            Console.WriteLine("\n=== Fibonacci Benchmark ===");

            // Recursive approach with n=35
            var watchRecursive = Stopwatch.StartNew();
            long resultRecursive = FibRecursive(35);
            watchRecursive.Stop();
            double timeRecursive = watchRecursive.Elapsed.TotalMilliseconds;

            Console.WriteLine($"Recursive (n=35): {timeRecursive:F2} ms, result = {resultRecursive}");

            // Iterative approach with n=40
            var watchIterative = Stopwatch.StartNew();
            long resultIterative = FibIterative(40);
            watchIterative.Stop();
            double timeIterative = watchIterative.Elapsed.TotalMilliseconds;

            Console.WriteLine($"Iterative (n=40): {timeIterative:F2} ms, result = {resultIterative}");
        }
    }
}
