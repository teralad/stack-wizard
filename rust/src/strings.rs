use regex::Regex;
use std::time::Instant;

/// Reverse a string
fn reverse_string(s: &str) -> String {
    s.chars().rev().collect()
}

/// Concatenate strings multiple times
fn concatenate_strings(iterations: usize) -> String {
    let mut result = String::new();
    for i in 0..iterations {
        result.push_str(&i.to_string());
    }
    result
}

/// Search for pattern in text using regex
fn pattern_search(text: &str, pattern: &str) -> usize {
    let re = Regex::new(pattern).unwrap();
    re.find_iter(text).count()
}

/// Run string manipulation benchmarks
pub fn run_benchmark() {
    // String reversal on 1 million character string
    let large_string = "a".repeat(1000000);
    let start_time = Instant::now();
    let _reversed = reverse_string(&large_string);
    let execution_time_reverse = start_time.elapsed().as_millis();

    println!("Test: String Reversal (1M chars)");
    println!("Execution time: {} ms", execution_time_reverse);
    println!("String length: {}", large_string.len());
    println!();

    // String concatenation (10,000 iterations)
    let start_time = Instant::now();
    let concatenated = concatenate_strings(10000);
    let execution_time_concat = start_time.elapsed().as_millis();

    println!("Test: String Concatenation (10K iterations)");
    println!("Execution time: {} ms", execution_time_concat);
    println!("Result length: {}", concatenated.len());
    println!();

    // Pattern searching
    let text = "Lorem ipsum dolor sit amet ".repeat(10000);
    let pattern = r"\b\w{5}\b"; // Find all 5-letter words
    let start_time = Instant::now();
    let matches = pattern_search(&text, pattern);
    let execution_time_search = start_time.elapsed().as_millis();

    println!("Test: Pattern Search");
    println!("Execution time: {} ms", execution_time_search);
    println!("Matches found: {}", matches);
}
