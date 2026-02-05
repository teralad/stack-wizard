public class Fibonacci {
    /**
     * Recursive Fibonacci implementation.
     */
    public static long fibonacciRecursive(int n) {
        if (n <= 1) {
            return n;
        }
        return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
    }

    /**
     * Iterative Fibonacci implementation.
     */
    public static long fibonacciIterative(int n) {
        if (n <= 1) {
            return n;
        }

        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    /**
     * Run Fibonacci benchmarks.
     */
    public static void runBenchmark() {
        // Recursive fibonacci(35)
        long startTime = System.nanoTime();
        long resultRecursive = fibonacciRecursive(35);
        long endTime = System.nanoTime();
        long executionTimeRecursive = (endTime - startTime) / 1000000;

        System.out.println("Test: Fibonacci Recursive (n=35)");
        System.out.println("Result: " + resultRecursive);
        System.out.println("Execution time: " + executionTimeRecursive + " ms");
        System.out.println();

        // Iterative fibonacci(40)
        startTime = System.nanoTime();
        long resultIterative = fibonacciIterative(40);
        endTime = System.nanoTime();
        long executionTimeIterative = (endTime - startTime) / 1000000;

        System.out.println("Test: Fibonacci Iterative (n=40)");
        System.out.println("Result: " + resultIterative);
        System.out.println("Execution time: " + executionTimeIterative + " ms");
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
