/**
 * Main program entry point to run all Scala performance benchmarks.
 */
object Main {
  def main(args: Array[String]): Unit = {
    println("\n" + "=" * 60)
    println("Scala Performance Benchmarks")
    println("=" * 60 + "\n")

    // Run all benchmarks
    println("\n=== 1. Sorting (Quicksort) ===")
    Sorting.runBenchmark()

    println("\n=== 2. Fibonacci ===")
    Fibonacci.runBenchmark()

    println("\n=== 3. Matrix Multiplication ===")
    Matrix.runBenchmark()

    println("\n=== 4. String Manipulation ===")
    Strings.runBenchmark()

    println("\n=== 5. API Requests ===")
    val metrics = ApiRequests.runBenchmark()
    ApiRequests.printResults(metrics)

    println("\n" + "=" * 60)
    println("All benchmarks completed!")
    println("=" * 60 + "\n")
  }
}
