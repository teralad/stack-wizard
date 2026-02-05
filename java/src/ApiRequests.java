/**
 * Java API Request Performance Test
 * Uses HttpClient with CompletableFuture for efficient concurrent HTTP requests.
 * Collects comprehensive metrics including response times, throughput, and percentiles.
 */

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

public class ApiRequests {
    
    static class RequestResult {
        int id;
        boolean success;
        double responseTimeMs;
        double timestamp;
        String error;
        
        public RequestResult(int id, boolean success, double responseTimeMs, double timestamp) {
            this.id = id;
            this.success = success;
            this.responseTimeMs = responseTimeMs;
            this.timestamp = timestamp;
        }
        
        public RequestResult(int id, boolean success, double responseTimeMs, double timestamp, String error) {
            this(id, success, responseTimeMs, timestamp);
            this.error = error;
        }
    }
    
    static class ResponseTimes {
        double min_ms;
        double max_ms;
        double average_ms;
        double median_ms;
        double p95_ms;
        double p99_ms;
        
        public ResponseTimes(double min, double max, double avg, double median, double p95, double p99) {
            this.min_ms = Math.round(min * 100.0) / 100.0;
            this.max_ms = Math.round(max * 100.0) / 100.0;
            this.average_ms = Math.round(avg * 100.0) / 100.0;
            this.median_ms = Math.round(median * 100.0) / 100.0;
            this.p95_ms = Math.round(p95 * 100.0) / 100.0;
            this.p99_ms = Math.round(p99 * 100.0) / 100.0;
        }
    }
    
    static class TimeseriesPoint {
        double timestamp;
        double response_time_ms;
        
        public TimeseriesPoint(double timestamp, double responseTime) {
            this.timestamp = Math.round(timestamp * 1000.0) / 1000.0;
            this.response_time_ms = Math.round(responseTime * 100.0) / 100.0;
        }
    }
    
    static class Metrics {
        String language;
        int total_requests;
        int successful_requests;
        int failed_requests;
        double total_time_seconds;
        double requests_per_second;
        ResponseTimes response_times;
        List<TimeseriesPoint> timeseries;
        
        public Metrics(String language, int totalRequests, int successfulRequests, int failedRequests,
                      double totalTime, double rps, ResponseTimes responseTimes, List<TimeseriesPoint> timeseries) {
            this.language = language;
            this.total_requests = totalRequests;
            this.successful_requests = successfulRequests;
            this.failed_requests = failedRequests;
            this.total_time_seconds = Math.round(totalTime * 100.0) / 100.0;
            this.requests_per_second = Math.round(rps * 100.0) / 100.0;
            this.response_times = responseTimes;
            this.timeseries = timeseries;
        }
    }

    /**
     * Make a single HTTP request with timing.
     */
    private static CompletableFuture<RequestResult> makeRequest(HttpClient client, String url, int requestId, long startTimeNanos) {
        long requestStart = System.nanoTime();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .timeout(Duration.ofSeconds(10))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .handle((response, throwable) -> {
                    long requestEnd = System.nanoTime();
                    double responseTimeMs = (requestEnd - requestStart) / 1_000_000.0;
                    double timestamp = (requestEnd - startTimeNanos) / 1_000_000_000.0;
                    
                    if (throwable != null) {
                        return new RequestResult(requestId, false, responseTimeMs, timestamp, throwable.getMessage());
                    } else {
                        return new RequestResult(requestId, response.statusCode() == 200, responseTimeMs, timestamp);
                    }
                });
    }
    
    /**
     * Calculate percentile from sorted list.
     */
    private static double percentile(List<Double> sortedData, double p) {
        if (sortedData.isEmpty()) {
            return 0.0;
        }
        int index = (int) Math.ceil(sortedData.size() * p) - 1;
        index = Math.max(0, Math.min(index, sortedData.size() - 1));
        return sortedData.get(index);
    }

    /**
     * Run API request benchmark with 10,000 concurrent requests.
     * Uses HttpClient with CompletableFuture for async operations.
     */
    public static void runBenchmark() {
        String url = "https://jsonplaceholder.typicode.com/posts/1";
        int numRequests = 10000;

        System.out.println("Starting benchmark: " + numRequests + " requests to " + url);

        // Create HTTP client with connection pooling
        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();

        // Measure total time for concurrent requests
        long startTime = System.nanoTime();

        List<CompletableFuture<RequestResult>> futures = new ArrayList<>();
        for (int i = 0; i < numRequests; i++) {
            futures.add(makeRequest(client, url, i, startTime));
        }

        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
        );

        List<RequestResult> results;
        try {
            allFutures.get();
            results = futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
            return;
        }

        long endTime = System.nanoTime();
        double totalTime = (endTime - startTime) / 1_000_000_000.0;

        // Analyze results
        List<RequestResult> successfulResults = results.stream()
                .filter(r -> r.success)
                .collect(Collectors.toList());
        
        int successfulCount = successfulResults.size();
        int failedCount = results.size() - successfulCount;

        // Build metrics
        Metrics metrics;
        
        if (!successfulResults.isEmpty()) {
            List<Double> responseTimes = successfulResults.stream()
                    .map(r -> r.responseTimeMs)
                    .sorted()
                    .collect(Collectors.toList());

            double sum = responseTimes.stream().mapToDouble(Double::doubleValue).sum();
            double minVal = responseTimes.get(0);
            double maxVal = responseTimes.get(responseTimes.size() - 1);
            double avgVal = sum / responseTimes.size();
            double medianVal = percentile(responseTimes, 0.5);
            double p95Val = percentile(responseTimes, 0.95);
            double p99Val = percentile(responseTimes, 0.99);

            ResponseTimes responseTimesMetrics = new ResponseTimes(minVal, maxVal, avgVal, medianVal, p95Val, p99Val);

            List<TimeseriesPoint> timeseries = successfulResults.stream()
                    .map(r -> new TimeseriesPoint(r.timestamp, r.responseTimeMs))
                    .collect(Collectors.toList());

            metrics = new Metrics(
                    "java",
                    numRequests,
                    successfulCount,
                    failedCount,
                    totalTime,
                    numRequests / totalTime,
                    responseTimesMetrics,
                    timeseries
            );
        } else {
            metrics = new Metrics(
                    "java",
                    numRequests,
                    0,
                    failedCount,
                    totalTime,
                    0.0,
                    new ResponseTimes(0, 0, 0, 0, 0, 0),
                    new ArrayList<>()
            );
        }

        // Save results to JSON file
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        String jsonData = gson.toJson(metrics);

        try (FileWriter writer = new FileWriter("api_results.json")) {
            writer.write(jsonData);
            System.out.println("\nResults saved to api_results.json");
        } catch (IOException e) {
            System.err.println("Error writing results file: " + e.getMessage());
        }

        // Print results
        printResults(metrics);
    }

    private static void printResults(Metrics metrics) {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("Language: " + metrics.language.toUpperCase());
        System.out.println("=".repeat(60));
        System.out.println("Total Requests: " + metrics.total_requests);
        System.out.println("Successful: " + metrics.successful_requests);
        System.out.println("Failed: " + metrics.failed_requests);
        System.out.printf("Total Time: %.2fs%n", metrics.total_time_seconds);
        System.out.printf("Requests/sec: %.2f%n", metrics.requests_per_second);

        if (metrics.successful_requests > 0) {
            System.out.println("\nResponse Times (ms):");
            System.out.printf("  Min: %.2f%n", metrics.response_times.min_ms);
            System.out.printf("  Max: %.2f%n", metrics.response_times.max_ms);
            System.out.printf("  Avg: %.2f%n", metrics.response_times.average_ms);
            System.out.printf("  Median: %.2f%n", metrics.response_times.median_ms);
            System.out.printf("  P95: %.2f%n", metrics.response_times.p95_ms);
            System.out.printf("  P99: %.2f%n", metrics.response_times.p99_ms);
        }
        System.out.println("=".repeat(60) + "\n");
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
