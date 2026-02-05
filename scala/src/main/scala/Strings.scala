import scala.util.matching.Regex

/**
 * String manipulation operations for performance benchmarking.
 * Tests string reversal, concatenation, and pattern matching.
 */
object Strings {
  /**
   * Reverse a string.
   */
  def reverseString(str: String): String = {
    str.reverse
  }

  /**
   * Concatenate a string n times.
   */
  def concatenateString(baseStr: String, n: Int): String = {
    val sb = new StringBuilder()
    for (_ <- 0 until n) {
      sb.append(baseStr)
    }
    sb.toString()
  }

  /**
   * Find 5-letter words in text using pattern matching.
   */
  def findFiveLetterWords(text: String): Int = {
    val pattern: Regex = """\b[a-zA-Z]{5}\b""".r
    pattern.findAllIn(text).length
  }

  /**
   * Run string manipulation benchmarks.
   */
  def runBenchmark(): Unit = {
    println("\n=== String Manipulation Benchmarks ===")

    // 1. String Reversal (1 million characters)
    val longString = "a" * 500000 + "b" * 500000
    val startReverse = System.nanoTime()
    val reversed = reverseString(longString)
    val endReverse = System.nanoTime()
    val timeReverse = (endReverse - startReverse) / 1000000.0
    println(f"String Reversal (1M chars): $timeReverse%.2f ms")

    // 2. String Concatenation (10,000 iterations)
    val startConcat = System.nanoTime()
    val concatenated = concatenateString("test", 10000)
    val endConcat = System.nanoTime()
    val timeConcat = (endConcat - startConcat) / 1000000.0
    println(f"String Concatenation (10K iterations): $timeConcat%.2f ms")

    // 3. Pattern Search (find 5-letter words)
    val sampleText = "hello world quick brown foxes jumps over fence under table chair grape mango apple berry water glass plate metal stone brick house happy smile dream peace light stars night"
    val largeText = (sampleText + " ") * 1000
    val startSearch = System.nanoTime()
    val matchCount = findFiveLetterWords(largeText)
    val endSearch = System.nanoTime()
    val timeSearch = (endSearch - startSearch) / 1000000.0
    println(f"Pattern Search: $timeSearch%.2f ms ($matchCount matches)")
  }

  def main(args: Array[String]): Unit = {
    runBenchmark()
  }
}
