import sttp.client3._
import scala.concurrent.{Await, Future, ExecutionContext}
import scala.concurrent.duration._
import java.io.PrintWriter
import scala.util.{Try, Success, Failure}

/**
 * API Request Performance Test for Scala.
 * Uses sttp client with Futures for efficient concurrent HTTP requests.
 * Collects comprehensive metrics including response times, throughput, and percentiles.
 */
object ApiRequests {
  implicit val ec: ExecutionContext = ExecutionContext.global

  case class RequestResult(
    id: Int,
    success: Boolean,
    responseTimeMs: Double,
    timestamp: Double,
    error: Option[String] = None
  )

  case class ResponseTimes(
    min_ms: Double,
    max_ms: Double,
    average_ms: Double,
    median_ms: Double,
    p95_ms: Double,
    p99_ms: Double
  )

  case class TimeseriesPoint(
    timestamp: Double,
    response_time_ms: Double
  )

  case class ApiMetrics(
    language: String,
    total_requests: Int,
    successful_requests: Int,
    failed_requests: Int,
    total_time_seconds: Double,
    requests_per_second: Double,
    response_times: Option[ResponseTimes],
    timeseries: List[TimeseriesPoint]
  )

  /**
   * Make a single HTTP request asynchronously.
   */
  def makeRequest(backend: SttpBackend[Identity, Any], url: String, requestId: Int, startTime: Long): RequestResult = {
    val requestStart = System.currentTimeMillis()
    
    try {
      val request = basicRequest
        .get(uri"$url")
        .readTimeout(10.seconds)
      
      val response = request.send(backend)
      val requestEnd = System.currentTimeMillis()
      
      RequestResult(
        id = requestId,
        success = response.code.code == 200,
        responseTimeMs = (requestEnd - requestStart).toDouble,
        timestamp = (requestEnd - startTime) / 1000.0
      )
    } catch {
      case e: Exception =>
        val requestEnd = System.currentTimeMillis()
        RequestResult(
          id = requestId,
          success = false,
          responseTimeMs = (requestEnd - requestStart).toDouble,
          timestamp = (requestEnd - startTime) / 1000.0,
          error = Some(e.getMessage)
        )
    }
  }

  /**
   * Calculate percentile from sorted list.
   */
  def percentile(sortedList: List[Double], p: Double): Double = {
    val index = math.max(0, math.min((sortedList.length * p).toInt - 1, sortedList.length - 1))
    sortedList(index)
  }

  /**
   * Run API request benchmark with 10,000 concurrent requests.
   */
  def runBenchmark(): ApiMetrics = {
    val url = "https://jsonplaceholder.typicode.com/posts/1"
    val numRequests = 10000

    println(s"Starting benchmark: $numRequests requests to $url")

    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()

    // Make concurrent requests using parallel collections
    import scala.collection.parallel.CollectionConverters._
    val results = (0 until numRequests).par.map { i =>
      makeRequest(backend, url, i, startTime)
    }.toList

    val endTime = System.currentTimeMillis()
    val totalTime = (endTime - startTime) / 1000.0 // Convert to seconds

    backend.close()

    // Analyze results
    val successfulResults = results.filter(_.success)
    val failedResults = results.filter(!_.success)

    val successfulCount = successfulResults.length
    val failedCount = failedResults.length

    // Extract and sort response times
    val responseTimes = successfulResults.map(_.responseTimeMs)
    val sortedTimes = responseTimes.sorted

    // Create metrics
    val metrics = if (responseTimes.nonEmpty) {
      ApiMetrics(
        language = "scala",
        total_requests = numRequests,
        successful_requests = successfulCount,
        failed_requests = failedCount,
        total_time_seconds = BigDecimal(totalTime).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
        requests_per_second = BigDecimal(numRequests / totalTime).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
        response_times = Some(ResponseTimes(
          min_ms = BigDecimal(responseTimes.min).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
          max_ms = BigDecimal(responseTimes.max).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
          average_ms = BigDecimal(responseTimes.sum / responseTimes.length).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
          median_ms = BigDecimal(percentile(sortedTimes, 0.50)).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
          p95_ms = BigDecimal(percentile(sortedTimes, 0.95)).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
          p99_ms = BigDecimal(percentile(sortedTimes, 0.99)).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble
        )),
        timeseries = successfulResults.map(r =>
          TimeseriesPoint(
            timestamp = BigDecimal(r.timestamp).setScale(3, BigDecimal.RoundingMode.HALF_UP).toDouble,
            response_time_ms = BigDecimal(r.responseTimeMs).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble
          )
        )
      )
    } else {
      ApiMetrics(
        language = "scala",
        total_requests = numRequests,
        successful_requests = 0,
        failed_requests = failedCount,
        total_time_seconds = BigDecimal(totalTime).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble,
        requests_per_second = 0.0,
        response_times = None,
        timeseries = List.empty
      )
    }

    // Save results to JSON file
    val outputFile = "api_results.json"
    saveToJson(metrics, outputFile)

    println(s"\nResults saved to $outputFile")

    metrics
  }

  /**
   * Save metrics to JSON file.
   */
  def saveToJson(metrics: ApiMetrics, filename: String): Unit = {
    import ujson._

    val json = Obj(
      "language" -> metrics.language,
      "total_requests" -> metrics.total_requests,
      "successful_requests" -> metrics.successful_requests,
      "failed_requests" -> metrics.failed_requests,
      "total_time_seconds" -> metrics.total_time_seconds,
      "requests_per_second" -> metrics.requests_per_second,
      "response_times" -> (metrics.response_times match {
        case Some(rt) => Obj(
          "min_ms" -> rt.min_ms,
          "max_ms" -> rt.max_ms,
          "average_ms" -> rt.average_ms,
          "median_ms" -> rt.median_ms,
          "p95_ms" -> rt.p95_ms,
          "p99_ms" -> rt.p99_ms
        )
        case None => Obj()
      }),
      "timeseries" -> Arr(
        metrics.timeseries.map(ts =>
          Obj(
            "timestamp" -> ts.timestamp,
            "response_time_ms" -> ts.response_time_ms
          )
        ): _*
      )
    )

    val writer = new PrintWriter(filename)
    writer.write(ujson.write(json, indent = 2))
    writer.close()
  }

  /**
   * Print formatted results to console.
   */
  def printResults(metrics: ApiMetrics): Unit = {
    println("\n" + "=" * 60)
    println(s"Language: ${metrics.language.toUpperCase}")
    println("=" * 60)
    println(s"Total Requests: ${metrics.total_requests}")
    println(s"Successful: ${metrics.successful_requests}")
    println(s"Failed: ${metrics.failed_requests}")
    println(f"Total Time: ${metrics.total_time_seconds}%.2fs")
    println(f"Requests/sec: ${metrics.requests_per_second}%.2f")

    metrics.response_times.foreach { rt =>
      println("\nResponse Times (ms):")
      println(f"  Min: ${rt.min_ms}%.2f")
      println(f"  Max: ${rt.max_ms}%.2f")
      println(f"  Avg: ${rt.average_ms}%.2f")
      println(f"  Median: ${rt.median_ms}%.2f")
      println(f"  P95: ${rt.p95_ms}%.2f")
      println(f"  P99: ${rt.p99_ms}%.2f")
    }

    println("=" * 60 + "\n")
  }

  def main(args: Array[String]): Unit = {
    val metrics = runBenchmark()
    printResults(metrics)
  }
}
