import com.github.tomakehurst.wiremock.WireMockServer
import com.github.tomakehurst.wiremock.client.WireMock._
import com.github.tomakehurst.wiremock.core.WireMockConfiguration._
import org.scalatest.BeforeAndAfterEach
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.matchers.should.Matchers
import sttp.client3._

/**
 * Integration tests for API requests using WireMock to simulate HTTP responses.
 * These tests verify the API request functionality without requiring external network access.
 */
class ApiRequestsSpec extends AnyFunSuite with Matchers with BeforeAndAfterEach {
  
  var wireMockServer: WireMockServer = _
  
  override def beforeEach(): Unit = {
    wireMockServer = new WireMockServer(wireMockConfig().dynamicPort())
    wireMockServer.start()
    configureFor("localhost", wireMockServer.port())
  }
  
  override def afterEach(): Unit = {
    wireMockServer.stop()
  }

  test("makeRequest should return success for 200 OK response") {
    // Arrange
    stubFor(get(urlEqualTo("/posts/1"))
      .willReturn(aResponse()
        .withStatus(200)
        .withBody("""{"id": 1, "title": "test"}""")))

    val url = s"http://localhost:${wireMockServer.port()}/posts/1"
    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()

    // Act
    val result = ApiRequests.makeRequest(backend, url, 1, startTime)
    backend.close()

    // Assert
    result.success shouldBe true
    result.id shouldBe 1
    result.responseTimeMs should be > 0.0
    result.timestamp should be >= 0.0
  }

  test("makeRequest should handle non-200 status codes") {
    // Arrange
    stubFor(get(urlEqualTo("/posts/1"))
      .willReturn(aResponse()
        .withStatus(404)
        .withBody("Not Found")))

    val url = s"http://localhost:${wireMockServer.port()}/posts/1"
    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()

    // Act
    val result = ApiRequests.makeRequest(backend, url, 1, startTime)
    backend.close()

    // Assert
    result.success shouldBe false
    result.id shouldBe 1
  }

  test("makeRequest should handle network errors gracefully") {
    // Arrange - no stub, server will reject
    val url = s"http://localhost:${wireMockServer.port()}/nonexistent"
    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()

    // Act
    val result = ApiRequests.makeRequest(backend, url, 1, startTime)
    backend.close()

    // Assert - should not throw, but should indicate failure
    result.success shouldBe false
    result.id shouldBe 1
  }

  test("percentile should calculate 50th percentile (median) correctly") {
    // Arrange
    val data = List(1.0, 2.0, 3.0, 4.0, 5.0)

    // Act
    val result = ApiRequests.percentile(data, 0.50)

    // Assert
    result shouldBe 3.0
  }

  test("percentile should calculate 95th percentile correctly") {
    // Arrange
    val data = (1 to 100).map(_.toDouble).toList

    // Act
    val result = ApiRequests.percentile(data, 0.95)

    // Assert
    result should (be >= 94.0 and be <= 96.0)
  }

  test("percentile should calculate 99th percentile correctly") {
    // Arrange
    val data = (1 to 100).map(_.toDouble).toList

    // Act
    val result = ApiRequests.percentile(data, 0.99)

    // Assert
    result should (be >= 98.0 and be <= 100.0)
  }

  test("percentile should handle single element list") {
    // Arrange
    val data = List(42.0)

    // Assert
    ApiRequests.percentile(data, 0.50) shouldBe 42.0
    ApiRequests.percentile(data, 0.95) shouldBe 42.0
    ApiRequests.percentile(data, 0.99) shouldBe 42.0
  }

  test("concurrent requests should complete successfully") {
    // Arrange
    stubFor(get(urlEqualTo("/posts/1"))
      .willReturn(aResponse()
        .withStatus(200)
        .withBody("""{"id": 1, "title": "test"}""")))

    val url = s"http://localhost:${wireMockServer.port()}/posts/1"
    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()
    val numRequests = 10

    // Act
    import scala.collection.parallel.CollectionConverters._
    val results = (0 until numRequests).par.map { i =>
      ApiRequests.makeRequest(backend, url, i, startTime)
    }.toList

    backend.close()

    val successfulResults = results.filter(_.success)
    
    // Assert
    successfulResults should have size numRequests
    
    // All response times should be positive
    successfulResults.foreach { result =>
      result.responseTimeMs should be > 0.0
    }
  }

  test("API metrics structure should be valid") {
    // Arrange
    stubFor(get(urlEqualTo("/posts/1"))
      .willReturn(aResponse()
        .withStatus(200)
        .withBody("""{"id": 1, "title": "test"}""")))

    val url = s"http://localhost:${wireMockServer.port()}/posts/1"
    val backend = HttpURLConnectionBackend()
    val startTime = System.currentTimeMillis()
    val numRequests = 10

    // Act
    import scala.collection.parallel.CollectionConverters._
    val results = (0 until numRequests).par.map { i =>
      ApiRequests.makeRequest(backend, url, i, startTime)
    }.toList

    val endTime = System.currentTimeMillis()
    val totalTime = (endTime - startTime) / 1000.0

    backend.close()

    val successfulResults = results.filter(_.success)
    val responseTimes = successfulResults.map(_.responseTimeMs)
    val sortedTimes = responseTimes.sorted

    // Assert - verify we can calculate all required metrics
    successfulResults should have size numRequests
    responseTimes.foreach(_ should be > 0.0)
    
    if (responseTimes.nonEmpty) {
      responseTimes.min should be > 0.0
      responseTimes.max should be > 0.0
      (responseTimes.sum / responseTimes.length) should be > 0.0
      ApiRequests.percentile(sortedTimes, 0.50) should be > 0.0
      ApiRequests.percentile(sortedTimes, 0.95) should be > 0.0
      ApiRequests.percentile(sortedTimes, 0.99) should be > 0.0
    }
  }
}
