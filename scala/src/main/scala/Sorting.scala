import scala.util.Random

/**
 * Quicksort implementation for performance benchmarking.
 * Tests with 100,000 random integers.
 */
object Sorting {
  /**
   * Quicksort algorithm implementation.
   */
  def quicksort(arr: List[Int]): List[Int] = {
    if (arr.length <= 1) arr
    else {
      val pivot = arr(arr.length / 2)
      val (left, rest) = arr.partition(_ < pivot)
      val (middle, right) = rest.partition(_ == pivot)
      quicksort(left) ::: middle ::: quicksort(right)
    }
  }

  /**
   * Run sorting benchmark with 100,000 random integers.
   */
  def runBenchmark(): Unit = {
    val random = new Random()
    val arr = List.fill(100000)(random.nextInt(1000000))

    val startTime = System.nanoTime()
    val sortedArr = quicksort(arr)
    val endTime = System.nanoTime()

    val executionTime = (endTime - startTime) / 1000000.0 // Convert to milliseconds

    // Verify sorting correctness
    val isSorted = sortedArr.sliding(2).forall {
      case List(a, b) => a <= b
      case _ => true
    }

    println("\n=== Sorting (Quicksort) ===")
    println(s"Array size: ${arr.length}")
    println(f"Execution time: $executionTime%.2f ms")
    println(s"Correctly sorted: $isSorted")
  }

  def main(args: Array[String]): Unit = {
    runBenchmark()
  }
}
