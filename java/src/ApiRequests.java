import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class ApiRequests {
    /**
     * Make a single HTTP request.
     */
    private static CompletableFuture<Boolean> makeRequest(String url, int requestId) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .build();

        return client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> response.statusCode() == 200)
                .exceptionally(ex -> false);
    }

    /**
     * Run API request benchmark with 50 concurrent requests.
     */
    public static void runBenchmark() {
        String url = "https://jsonplaceholder.typicode.com/posts/1";
        int numRequests = 50;

        // Measure total time for concurrent requests
        long startTime = System.nanoTime();

        List<CompletableFuture<Boolean>> futures = new ArrayList<>();
        for (int i = 0; i < numRequests; i++) {
            futures.add(makeRequest(url, i));
        }

        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
        );

        try {
            allFutures.get();
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }

        long endTime = System.nanoTime();
        long executionTime = (endTime - startTime) / 1000000;

        // Count successful requests
        long successful = futures.stream()
                .map(CompletableFuture::join)
                .filter(success -> success)
                .count();

        System.out.println("Test: API Requests (50 concurrent)");
        System.out.println("Total requests: " + numRequests);
        System.out.println("Successful requests: " + successful);
        System.out.println("Execution time: " + executionTime + " ms");
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
