import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Sorting {
    /**
     * Quicksort algorithm implementation.
     */
    public static List<Integer> quicksort(List<Integer> arr) {
        if (arr.size() <= 1) {
            return arr;
        }

        int pivot = arr.get(arr.size() / 2);
        List<Integer> left = new ArrayList<>();
        List<Integer> middle = new ArrayList<>();
        List<Integer> right = new ArrayList<>();

        for (int x : arr) {
            if (x < pivot) {
                left.add(x);
            } else if (x == pivot) {
                middle.add(x);
            } else {
                right.add(x);
            }
        }

        List<Integer> result = new ArrayList<>(quicksort(left));
        result.addAll(middle);
        result.addAll(quicksort(right));
        return result;
    }

    /**
     * Verify if array is sorted.
     */
    private static boolean isSorted(List<Integer> arr) {
        for (int i = 0; i < arr.size() - 1; i++) {
            if (arr.get(i) > arr.get(i + 1)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Run sorting benchmark with 100,000 random integers.
     */
    public static void runBenchmark() {
        Random rand = new Random();
        
        // Generate 100,000 random integers
        List<Integer> arr = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            arr.add(rand.nextInt(1000000));
        }

        // Measure sorting time
        long startTime = System.nanoTime();
        List<Integer> sortedArr = quicksort(arr);
        long endTime = System.nanoTime();
        long executionTime = (endTime - startTime) / 1000000; // Convert to milliseconds

        // Verify sorting correctness
        boolean correct = isSorted(sortedArr);

        System.out.println("Test: Sorting (Quicksort)");
        System.out.println("Array size: " + arr.size());
        System.out.println("Execution time: " + executionTime + " ms");
        System.out.println("Correctly sorted: " + correct);
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
