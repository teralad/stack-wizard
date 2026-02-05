using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using WireMock.RequestBuilders;
using WireMock.ResponseBuilders;
using WireMock.Server;
using Xunit;

namespace StackWizard.Tests
{
    /// <summary>
    /// Integration tests for API requests using WireMock to simulate HTTP responses.
    /// These tests verify the API request functionality without requiring external network access.
    /// </summary>
    public class ApiRequestsTests : IDisposable
    {
        private readonly WireMockServer _mockServer;
        private readonly HttpClient _httpClient;

        public ApiRequestsTests()
        {
            // Start WireMock server
            _mockServer = WireMockServer.Start();
            _httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };
        }

        public void Dispose()
        {
            _mockServer?.Stop();
            _httpClient?.Dispose();
        }

        [Fact]
        public async Task MakeRequest_Returns_Success_For_200_Response()
        {
            // Arrange
            _mockServer
                .Given(Request.Create().WithPath("/posts/1").UsingGet())
                .RespondWith(Response.Create()
                    .WithStatusCode(200)
                    .WithBody("{\"id\": 1, \"title\": \"test\"}"));

            string url = $"{_mockServer.Url}/posts/1";
            var totalWatch = Stopwatch.StartNew();

            // Act
            var response = await _httpClient.GetAsync(url);
            var responseTime = totalWatch.Elapsed.TotalMilliseconds;

            // Assert
            Assert.True(response.IsSuccessStatusCode);
            Assert.Equal(200, (int)response.StatusCode);
            Assert.True(responseTime > 0);
        }

        [Fact]
        public async Task MakeRequest_Handles_Non_200_Status_Code()
        {
            // Arrange
            _mockServer
                .Given(Request.Create().WithPath("/posts/1").UsingGet())
                .RespondWith(Response.Create()
                    .WithStatusCode(404)
                    .WithBody("Not Found"));

            string url = $"{_mockServer.Url}/posts/1";

            // Act
            var response = await _httpClient.GetAsync(url);

            // Assert
            Assert.False(response.IsSuccessStatusCode);
            Assert.Equal(404, (int)response.StatusCode);
        }

        [Fact]
        public async Task MakeRequest_Handles_Timeout()
        {
            // Arrange
            _mockServer
                .Given(Request.Create().WithPath("/posts/1").UsingGet())
                .RespondWith(Response.Create()
                    .WithStatusCode(200)
                    .WithDelay(TimeSpan.FromSeconds(2))
                    .WithBody("{\"id\": 1}"));

            string url = $"{_mockServer.Url}/posts/1";
            var shortTimeoutClient = new HttpClient { Timeout = TimeSpan.FromMilliseconds(100) };

            // Act & Assert
            await Assert.ThrowsAnyAsync<TaskCanceledException>(async () =>
            {
                await shortTimeoutClient.GetAsync(url);
            });

            shortTimeoutClient.Dispose();
        }

        [Fact]
        public async Task ConcurrentRequests_Complete_Successfully()
        {
            // Arrange
            _mockServer
                .Given(Request.Create().WithPath("/posts/1").UsingGet())
                .RespondWith(Response.Create()
                    .WithStatusCode(200)
                    .WithBody("{\"id\": 1, \"title\": \"test\"}"));

            string url = $"{_mockServer.Url}/posts/1";
            int numRequests = 100;

            // Act
            var tasks = Enumerable.Range(0, numRequests)
                .Select(_ => _httpClient.GetAsync(url))
                .ToArray();

            var responses = await Task.WhenAll(tasks);

            // Assert
            Assert.Equal(numRequests, responses.Length);
            Assert.All(responses, response => Assert.True(response.IsSuccessStatusCode));
        }

        [Fact]
        public void Percentile_Calculates_Median_Correctly()
        {
            // Arrange
            var data = new List<double> { 1.0, 2.0, 3.0, 4.0, 5.0 };

            // Act
            double result = CalculatePercentile(data, 0.50);

            // Assert
            Assert.Equal(3.0, result);
        }

        [Fact]
        public void Percentile_Calculates_95th_Correctly()
        {
            // Arrange
            var data = Enumerable.Range(1, 100).Select(x => (double)x).ToList();

            // Act
            double result = CalculatePercentile(data, 0.95);

            // Assert
            Assert.InRange(result, 94.0, 96.0);
        }

        [Fact]
        public void Percentile_Calculates_99th_Correctly()
        {
            // Arrange
            var data = Enumerable.Range(1, 100).Select(x => (double)x).ToList();

            // Act
            double result = CalculatePercentile(data, 0.99);

            // Assert
            Assert.InRange(result, 98.0, 100.0);
        }

        [Fact]
        public void Percentile_Handles_Single_Element()
        {
            // Arrange
            var data = new List<double> { 42.0 };

            // Act & Assert
            Assert.Equal(42.0, CalculatePercentile(data, 0.50));
            Assert.Equal(42.0, CalculatePercentile(data, 0.95));
            Assert.Equal(42.0, CalculatePercentile(data, 0.99));
        }

        [Fact]
        public async Task ApiMetrics_Structure_Is_Valid()
        {
            // Arrange
            _mockServer
                .Given(Request.Create().WithPath("/posts/1").UsingGet())
                .RespondWith(Response.Create()
                    .WithStatusCode(200)
                    .WithBody("{\"id\": 1, \"title\": \"test\"}"));

            string url = $"{_mockServer.Url}/posts/1";
            int numRequests = 10;
            var totalWatch = Stopwatch.StartNew();

            // Act
            var tasks = Enumerable.Range(0, numRequests)
                .Select(i => MakeRequestWithTimingAsync(url, i, totalWatch))
                .ToArray();

            var results = await Task.WhenAll(tasks);
            totalWatch.Stop();

            var successfulResults = results.Where(r => r.Success).ToList();
            var responseTimes = successfulResults.Select(r => r.ResponseTimeMs).ToList();

            // Assert
            Assert.Equal(numRequests, successfulResults.Count);
            Assert.All(responseTimes, time => Assert.True(time > 0));
            
            // Verify we can calculate all required metrics
            if (responseTimes.Any())
            {
                var sortedTimes = responseTimes.OrderBy(t => t).ToList();
                Assert.True(responseTimes.Min() > 0);
                Assert.True(responseTimes.Max() > 0);
                Assert.True(responseTimes.Average() > 0);
                Assert.True(CalculatePercentile(sortedTimes, 0.50) > 0);
                Assert.True(CalculatePercentile(sortedTimes, 0.95) > 0);
                Assert.True(CalculatePercentile(sortedTimes, 0.99) > 0);
            }
        }

        // Helper methods that mirror the functionality in ApiRequests
        private async Task<RequestResult> MakeRequestWithTimingAsync(string url, int requestId, Stopwatch totalWatch)
        {
            var requestWatch = Stopwatch.StartNew();
            try
            {
                var response = await _httpClient.GetAsync(url);
                requestWatch.Stop();

                return new RequestResult
                {
                    Id = requestId,
                    Success = response.IsSuccessStatusCode,
                    ResponseTimeMs = requestWatch.Elapsed.TotalMilliseconds,
                    Timestamp = totalWatch.Elapsed.TotalSeconds
                };
            }
            catch (Exception ex)
            {
                requestWatch.Stop();
                return new RequestResult
                {
                    Id = requestId,
                    Success = false,
                    ResponseTimeMs = requestWatch.Elapsed.TotalMilliseconds,
                    Timestamp = totalWatch.Elapsed.TotalSeconds,
                    Error = ex.Message
                };
            }
        }

        private double CalculatePercentile(List<double> sortedList, double percentile)
        {
            int index = (int)Math.Ceiling(sortedList.Count * percentile) - 1;
            index = Math.Max(0, Math.Min(index, sortedList.Count - 1));
            return sortedList[index];
        }

        private class RequestResult
        {
            public int Id { get; set; }
            public bool Success { get; set; }
            public double ResponseTimeMs { get; set; }
            public double Timestamp { get; set; }
            public string? Error { get; set; }
        }
    }
}
