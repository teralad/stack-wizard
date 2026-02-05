using System;
using System.Collections.Generic;
using System.Linq;

namespace StackWizard
{
    /// <summary>
    /// Quicksort implementation for performance benchmarking.
    /// Tests with 100,000 random integers.
    /// </summary>
    public class Sorting
    {
        /// <summary>
        /// Quicksort algorithm implementation.
        /// </summary>
        public static List<int> Quicksort(List<int> arr)
        {
            if (arr.Count <= 1)
                return arr;

            int pivot = arr[arr.Count / 2];
            var left = arr.Where(x => x < pivot).ToList();
            var middle = arr.Where(x => x == pivot).ToList();
            var right = arr.Where(x => x > pivot).ToList();

            var result = new List<int>();
            result.AddRange(Quicksort(left));
            result.AddRange(middle);
            result.AddRange(Quicksort(right));
            return result;
        }

        /// <summary>
        /// Run sorting benchmark with 100,000 random integers.
        /// </summary>
        public static void RunBenchmark()
        {
            var random = new Random();
            var arr = Enumerable.Range(0, 100000)
                                .Select(_ => random.Next(0, 1000000))
                                .ToList();

            var watch = System.Diagnostics.Stopwatch.StartNew();
            var sortedArr = Quicksort(arr);
            watch.Stop();

            double executionTime = watch.Elapsed.TotalMilliseconds;

            // Verify sorting correctness
            bool isSorted = Enumerable.Range(0, sortedArr.Count - 1)
                                     .All(i => sortedArr[i] <= sortedArr[i + 1]);

            Console.WriteLine("\n=== Sorting (Quicksort) ===");
            Console.WriteLine($"Array size: {arr.Count}");
            Console.WriteLine($"Execution time: {executionTime:F2} ms");
            Console.WriteLine($"Correctly sorted: {isSorted}");
        }
    }
}
