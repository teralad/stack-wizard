using System;
using System.Threading.Tasks;

namespace StackWizard
{
    /// <summary>
    /// Main program entry point to run all C# performance benchmarks.
    /// </summary>
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("\n" + new string('=', 60));
            Console.WriteLine("C# Performance Benchmarks");
            Console.WriteLine(new string('=', 60) + "\n");

            // Run all benchmarks
            Console.WriteLine("\n=== 1. Sorting (Quicksort) ===");
            Sorting.RunBenchmark();

            Console.WriteLine("\n=== 2. Fibonacci ===");
            Fibonacci.RunBenchmark();

            Console.WriteLine("\n=== 3. Matrix Multiplication ===");
            Matrix.RunBenchmark();

            Console.WriteLine("\n=== 4. String Manipulation ===");
            Strings.RunBenchmark();

            Console.WriteLine("\n=== 5. API Requests ===");
            var metrics = await ApiRequests.RunBenchmarkAsync();
            ApiRequests.PrintResults(metrics);

            Console.WriteLine("\n" + new string('=', 60));
            Console.WriteLine("All benchmarks completed!");
            Console.WriteLine(new string('=', 60) + "\n");
        }
    }
}
