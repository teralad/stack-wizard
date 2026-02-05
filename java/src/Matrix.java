import java.util.Random;

public class Matrix {
    /**
     * Matrix multiplication implementation.
     */
    public static double[][] matrixMultiply(double[][] matrixA, double[][] matrixB) {
        int rowsA = matrixA.length;
        int colsA = matrixA[0].length;
        int colsB = matrixB[0].length;

        // Initialize result matrix with zeros
        double[][] result = new double[rowsA][colsB];

        // Perform multiplication
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                for (int k = 0; k < colsA; k++) {
                    result[i][j] += matrixA[i][k] * matrixB[k][j];
                }
            }
        }

        return result;
    }

    /**
     * Run matrix multiplication benchmark with 100x100 matrices.
     */
    public static void runBenchmark() {
        int size = 100;
        Random rand = new Random();

        // Generate two random 100x100 matrices
        double[][] matrixA = new double[size][size];
        double[][] matrixB = new double[size][size];
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                matrixA[i][j] = rand.nextDouble();
                matrixB[i][j] = rand.nextDouble();
            }
        }

        // Measure multiplication time
        long startTime = System.nanoTime();
        double[][] result = matrixMultiply(matrixA, matrixB);
        long endTime = System.nanoTime();
        long executionTime = (endTime - startTime) / 1000000;

        System.out.println("Test: Matrix Multiplication");
        System.out.println("Matrix size: " + size + "x" + size);
        System.out.println("Execution time: " + executionTime + " ms");
        System.out.printf("Result sample (0,0): %.6f%n", result[0][0]);
    }

    public static void main(String[] args) {
        runBenchmark();
    }
}
