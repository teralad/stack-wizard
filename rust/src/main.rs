mod sorting;
mod fibonacci;
mod matrix;
mod strings;
mod api_requests;

#[tokio::main]
async fn main() {
    println!("{}", "=".repeat(60));
    println!("Rust Performance Benchmarks");
    println!("{}", "=".repeat(60));
    println!();

    // Sorting
    println!("Running Sorting Benchmark...");
    sorting::run_benchmark();
    println!();

    // Fibonacci
    println!("Running Fibonacci Benchmarks...");
    fibonacci::run_benchmark();
    println!();

    // Matrix
    println!("Running Matrix Multiplication Benchmark...");
    matrix::run_benchmark();
    println!();

    // Strings
    println!("Running String Manipulation Benchmarks...");
    strings::run_benchmark();
    println!();

    // API Requests
    println!("Running API Request Benchmark...");
    api_requests::run_benchmark().await;
    println!();

    println!("{}", "=".repeat(60));
    println!("All benchmarks completed!");
    println!("{}", "=".repeat(60));
}
