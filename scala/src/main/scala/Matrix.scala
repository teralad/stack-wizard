import scala.util.Random

/**
 * Matrix multiplication implementation for performance benchmarking.
 * Tests with two 100x100 matrices.
 */
object Matrix {
  type Matrix = Array[Array[Double]]

  /**
   * Generate a random matrix of given dimensions.
   */
  def generateRandomMatrix(rows: Int, cols: Int): Matrix = {
    val random = new Random()
    Array.fill(rows, cols)(random.nextDouble() * 100)
  }

  /**
   * Multiply two matrices using standard algorithm.
   */
  def multiply(matrixA: Matrix, matrixB: Matrix): Matrix = {
    val rowsA = matrixA.length
    val colsA = matrixA(0).length
    val colsB = matrixB(0).length

    val result = Array.ofDim[Double](rowsA, colsB)

    for (i <- 0 until rowsA) {
      for (j <- 0 until colsB) {
        var sum = 0.0
        for (k <- 0 until colsA) {
          sum += matrixA(i)(k) * matrixB(k)(j)
        }
        result(i)(j) = sum
      }
    }

    result
  }

  /**
   * Run matrix multiplication benchmark with 100x100 matrices.
   */
  def runBenchmark(): Unit = {
    val size = 100

    // Generate two random matrices
    val matrixA = generateRandomMatrix(size, size)
    val matrixB = generateRandomMatrix(size, size)

    // Measure multiplication time
    val startTime = System.nanoTime()
    val resultMatrix = multiply(matrixA, matrixB)
    val endTime = System.nanoTime()

    val executionTime = (endTime - startTime) / 1000000.0 // Convert to milliseconds

    println("\n=== Matrix Multiplication Benchmark ===")
    println(s"Matrix size: ${size}x$size")
    println(f"Execution time: $executionTime%.2f ms")
    println(s"Result dimensions: ${resultMatrix.length}x${resultMatrix(0).length}")
  }

  def main(args: Array[String]): Unit = {
    runBenchmark()
  }
}
