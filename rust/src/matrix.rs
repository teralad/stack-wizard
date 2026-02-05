use rand::Rng;
use std::time::Instant;

/// Matrix multiplication implementation
fn matrix_multiply(matrix_a: &Vec<Vec<f64>>, matrix_b: &Vec<Vec<f64>>) -> Vec<Vec<f64>> {
    let rows_a = matrix_a.len();
    let cols_a = matrix_a[0].len();
    let cols_b = matrix_b[0].len();

    // Initialize result matrix with zeros
    let mut result = vec![vec![0.0; cols_b]; rows_a];

    // Perform multiplication
    for i in 0..rows_a {
        for j in 0..cols_b {
            for k in 0..cols_a {
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }

    result
}

/// Run matrix multiplication benchmark with 100x100 matrices
pub fn run_benchmark() {
    let size = 100;
    let mut rng = rand::thread_rng();

    // Generate two random 100x100 matrices
    let matrix_a: Vec<Vec<f64>> = (0..size)
        .map(|_| (0..size).map(|_| rng.gen::<f64>()).collect())
        .collect();
    let matrix_b: Vec<Vec<f64>> = (0..size)
        .map(|_| (0..size).map(|_| rng.gen::<f64>()).collect())
        .collect();

    // Measure multiplication time
    let start_time = Instant::now();
    let result = matrix_multiply(&matrix_a, &matrix_b);
    let execution_time = start_time.elapsed().as_millis();

    println!("Test: Matrix Multiplication");
    println!("Matrix size: {}x{}", size, size);
    println!("Execution time: {} ms", execution_time);
    println!("Result sample (0,0): {:.6}", result[0][0]);
}
