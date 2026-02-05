import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Strings {
    /**
     * Reverse a string.
     */
    public static String reverseString(String s) {
        return new StringBuilder(s).reverse().toString();
    }

    /**
     * Concatenate strings multiple times.
     */
    public static String concatenateStrings(int iterations) {
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < iterations; i++) {
            result.append(i);
        }
        return result.toString();
    }

    /**
     * Search for pattern in text using regex.
     */
    public static int patternSearch(String text, String patternStr) {
        Pattern pattern = Pattern.compile(patternStr);
        Matcher matcher = pattern.matcher(text);
        int count = 0;
        while (matcher.find()) {
            count++;
        }
        return count;
    }

    /**
     * Run string manipulation benchmarks.
     */
    public static void runBenchmark() {
        // String reversal on 1 million character string
        String largeString = "a".repeat(1000000);
        long startTime = System.nanoTime();
        String reversed = reverseString(largeString);
        long endTime = System.nanoTime();
        long executionTimeReverse = (endTime - startTime) / 1000000;

        System.out.println("Test: String Reversal (1M chars)");
        System.out.println("Execution time: " + executionTimeReverse + " ms");
        System.out.println("String length: " + largeString.length());
        System.out.println();

        // String concatenation (10,000 iterations)
        startTime = System.nanoTime();
        String concatenated = concatenateStrings(10000);
        endTime = System.nanoTime();
        long executionTimeConcat = (endTime - startTime) / 1000000;

        System.out.println("Test: String Concatenation (10K iterations)");
        System.out.println("Execution time: " + executionTimeConcat + " ms");
        System.out.println("Result length: " + concatenated.length());
        System.out.println();

        // Pattern searching
        String text = "Lorem ipsum dolor sit amet ".repeat(10000);
        String pattern = "\\b\\w{5}\\b"; // Find all 5-letter words
        startTime = System.nanoTime();
        int matches = patternSearch(text, pattern);
        endTime = System.nanoTime();
        long executionTimeSearch = (endTime - startTime) / 1000000;

        System.out.println("Test: Pattern Search");
        System.out.println("Execution time: " + executionTimeSearch + " ms");
        System.out.println("Matches found: " + matches);
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
