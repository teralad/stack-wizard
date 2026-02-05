public class Main {
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("Java Performance Benchmarks");
        System.out.println("=".repeat(60));
        System.out.println();

        // Sorting
        System.out.println("Running Sorting Benchmark...");
        Sorting.runBenchmark();
        System.out.println();

        // Fibonacci
        System.out.println("Running Fibonacci Benchmarks...");
        Fibonacci.runBenchmark();
        System.out.println();

        // Matrix
        System.out.println("Running Matrix Multiplication Benchmark...");
        Matrix.runBenchmark();
        System.out.println();

        // Strings
        System.out.println("Running String Manipulation Benchmarks...");
        Strings.runBenchmark();
        System.out.println();

        // API Requests
        System.out.println("Running API Request Benchmark...");
        ApiRequests.runBenchmark();
        System.out.println();

        System.out.println("=".repeat(60));
        System.out.println("All benchmarks completed!");
        System.out.println("=".repeat(60));
    }
}
