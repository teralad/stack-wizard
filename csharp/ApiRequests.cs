using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.IO;

namespace StackWizard
{
    /// <summary>
    /// API Request Performance Test for C#.
    /// Uses HttpClient with async/await for efficient concurrent HTTP requests.
    /// Collects comprehensive metrics including response times, throughput, and percentiles.
    /// </summary>
    public class ApiRequests
    {
        private static readonly HttpClient httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };

        /// <summary>
        /// Result of a single API request.
        /// </summary>
        public class RequestResult
        {
            public int Id { get; set; }
            public bool Success { get; set; }
            public double ResponseTimeMs { get; set; }
            public double Timestamp { get; set; }
            public string? Error { get; set; }
        }

        /// <summary>
        /// Comprehensive API performance metrics.
        /// </summary>
        public class ApiMetrics
        {
            [JsonProperty("language")]
            public string Language { get; set; } = "csharp";

            [JsonProperty("total_requests")]
            public int TotalRequests { get; set; }

            [JsonProperty("successful_requests")]
            public int SuccessfulRequests { get; set; }

            [JsonProperty("failed_requests")]
            public int FailedRequests { get; set; }

            [JsonProperty("total_time_seconds")]
            public double TotalTimeSeconds { get; set; }

            [JsonProperty("requests_per_second")]
            public double RequestsPerSecond { get; set; }

            [JsonProperty("response_times")]
            public ResponseTimes? ResponseTimesData { get; set; }

            [JsonProperty("timeseries")]
            public List<TimeseriesPoint> Timeseries { get; set; } = new List<TimeseriesPoint>();
        }

        public class ResponseTimes
        {
            [JsonProperty("min_ms")]
            public double MinMs { get; set; }

            [JsonProperty("max_ms")]
            public double MaxMs { get; set; }

            [JsonProperty("average_ms")]
            public double AverageMs { get; set; }

            [JsonProperty("median_ms")]
            public double MedianMs { get; set; }

            [JsonProperty("p95_ms")]
            public double P95Ms { get; set; }

            [JsonProperty("p99_ms")]
            public double P99Ms { get; set; }
        }

        public class TimeseriesPoint
        {
            [JsonProperty("timestamp")]
            public double Timestamp { get; set; }

            [JsonProperty("response_time_ms")]
            public double ResponseTimeMs { get; set; }
        }

        /// <summary>
        /// Make a single HTTP request asynchronously.
        /// </summary>
        private static async Task<RequestResult> MakeRequestAsync(string url, int requestId, Stopwatch totalWatch)
        {
            var requestWatch = Stopwatch.StartNew();
            try
            {
                var response = await httpClient.GetAsync(url);
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

        /// <summary>
        /// Calculate percentile from sorted list.
        /// </summary>
        private static double Percentile(List<double> sortedList, double percentile)
        {
            int index = (int)Math.Ceiling(sortedList.Count * percentile) - 1;
            index = Math.Max(0, Math.Min(index, sortedList.Count - 1));
            return sortedList[index];
        }

        /// <summary>
        /// Run API request benchmark with 10,000 concurrent requests.
        /// </summary>
        public static async Task<ApiMetrics> RunBenchmarkAsync()
        {
            string url = "https://jsonplaceholder.typicode.com/posts/1";
            int numRequests = 1000;

            Console.WriteLine($"Starting benchmark: {numRequests} requests to {url}");

            var totalWatch = Stopwatch.StartNew();

            // Make concurrent requests using Task.WhenAll
            var tasks = Enumerable.Range(0, numRequests)
                                 .Select(i => MakeRequestAsync(url, i, totalWatch))
                                 .ToArray();

            var results = await Task.WhenAll(tasks);

            totalWatch.Stop();
            double totalTime = totalWatch.Elapsed.TotalSeconds;

            // Analyze results
            var successfulResults = results.Where(r => r.Success).ToList();
            var failedResults = results.Where(r => !r.Success).ToList();

            int successfulCount = successfulResults.Count;
            int failedCount = failedResults.Count;

            // Extract and sort response times
            var responseTimes = successfulResults.Select(r => r.ResponseTimeMs).ToList();
            var sortedTimes = responseTimes.OrderBy(t => t).ToList();

            // Create metrics
            var metrics = new ApiMetrics
            {
                TotalRequests = numRequests,
                SuccessfulRequests = successfulCount,
                FailedRequests = failedCount,
                TotalTimeSeconds = Math.Round(totalTime, 2),
                RequestsPerSecond = Math.Round(numRequests / totalTime, 2)
            };

            if (responseTimes.Count > 0)
            {
                metrics.ResponseTimesData = new ResponseTimes
                {
                    MinMs = Math.Round(responseTimes.Min(), 2),
                    MaxMs = Math.Round(responseTimes.Max(), 2),
                    AverageMs = Math.Round(responseTimes.Average(), 2),
                    MedianMs = Math.Round(Percentile(sortedTimes, 0.50), 2),
                    P95Ms = Math.Round(Percentile(sortedTimes, 0.95), 2),
                    P99Ms = Math.Round(Percentile(sortedTimes, 0.99), 2)
                };

                metrics.Timeseries = successfulResults.Select(r => new TimeseriesPoint
                {
                    Timestamp = Math.Round(r.Timestamp, 3),
                    ResponseTimeMs = Math.Round(r.ResponseTimeMs, 2)
                }).ToList();
            }

            // Save results to JSON file
            string outputFile = "api_results.json";
            string jsonData = JsonConvert.SerializeObject(metrics, Formatting.Indented);
            File.WriteAllText(outputFile, jsonData);

            Console.WriteLine($"\nResults saved to {outputFile}");

            return metrics;
        }

        /// <summary>
        /// Print formatted results to console.
        /// </summary>
        public static void PrintResults(ApiMetrics metrics)
        {
            Console.WriteLine("\n" + new string('=', 60));
            Console.WriteLine($"Language: {metrics.Language.ToUpper()}");
            Console.WriteLine(new string('=', 60));
            Console.WriteLine($"Total Requests: {metrics.TotalRequests}");
            Console.WriteLine($"Successful: {metrics.SuccessfulRequests}");
            Console.WriteLine($"Failed: {metrics.FailedRequests}");
            Console.WriteLine($"Total Time: {metrics.TotalTimeSeconds:F2}s");
            Console.WriteLine($"Requests/sec: {metrics.RequestsPerSecond:F2}");

            if (metrics.ResponseTimesData != null)
            {
                var rt = metrics.ResponseTimesData;
                Console.WriteLine("\nResponse Times (ms):");
                Console.WriteLine($"  Min: {rt.MinMs:F2}");
                Console.WriteLine($"  Max: {rt.MaxMs:F2}");
                Console.WriteLine($"  Avg: {rt.AverageMs:F2}");
                Console.WriteLine($"  Median: {rt.MedianMs:F2}");
                Console.WriteLine($"  P95: {rt.P95Ms:F2}");
                Console.WriteLine($"  P99: {rt.P99Ms:F2}");
            }

            Console.WriteLine(new string('=', 60) + "\n");
        }
    }
}
