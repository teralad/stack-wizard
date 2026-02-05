use std::time::Instant;

/// Recursive Fibonacci implementation
fn fibonacci_recursive(n: u32) -> u64 {
    if n <= 1 {
        return n as u64;
    }
    fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
}

/// Iterative Fibonacci implementation
fn fibonacci_iterative(n: u32) -> u64 {
    if n <= 1 {
        return n as u64;
    }

    let mut a: u64 = 0;
    let mut b: u64 = 1;
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    b
}

/// Run Fibonacci benchmarks
pub fn run_benchmark() {
    // Recursive fibonacci(35)
    let start_time = Instant::now();
    let result_recursive = fibonacci_recursive(35);
    let execution_time_recursive = start_time.elapsed().as_millis();

    println!("Test: Fibonacci Recursive (n=35)");
    println!("Result: {}", result_recursive);
    println!("Execution time: {} ms", execution_time_recursive);
    println!();

    // Iterative fibonacci(40)
    let start_time = Instant::now();
    let result_iterative = fibonacci_iterative(40);
    let execution_time_iterative = start_time.elapsed().as_millis();

    println!("Test: Fibonacci Iterative (n=40)");
    println!("Result: {}", result_iterative);
    println!("Execution time: {} ms", execution_time_iterative);
}
