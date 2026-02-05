/**
 * Fibonacci calculation implementations for performance benchmarking.
 * Tests recursive (n=35) and iterative (n=40) approaches.
 */
object Fibonacci {
  /**
   * Recursive Fibonacci implementation.
   */
  def fibRecursive(n: Int): Long = {
    if (n <= 1) n
    else fibRecursive(n - 1) + fibRecursive(n - 2)
  }

  /**
   * Iterative Fibonacci implementation.
   */
  def fibIterative(n: Int): Long = {
    if (n <= 1) return n

    var a = 0L
    var b = 1L
    for (_ <- 2 to n) {
      val temp = a + b
      a = b
      b = temp
    }
    b
  }

  /**
   * Run Fibonacci benchmarks.
   */
  def runBenchmark(): Unit = {
    println("\n=== Fibonacci Benchmark ===")

    // Recursive approach with n=35
    val startRecursive = System.nanoTime()
    val resultRecursive = fibRecursive(35)
    val endRecursive = System.nanoTime()
    val timeRecursive = (endRecursive - startRecursive) / 1000000.0

    println(f"Recursive (n=35): $timeRecursive%.2f ms, result = $resultRecursive")

    // Iterative approach with n=40
    val startIterative = System.nanoTime()
    val resultIterative = fibIterative(40)
    val endIterative = System.nanoTime()
    val timeIterative = (endIterative - startIterative) / 1000000.0

    println(f"Iterative (n=40): $timeIterative%.2f ms, result = $resultIterative")
  }

  def main(args: Array[String]): Unit = {
    runBenchmark()
  }
}
