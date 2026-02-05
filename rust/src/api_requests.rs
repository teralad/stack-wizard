/// Rust API Request Performance Test
/// Uses reqwest with tokio async runtime for efficient concurrent HTTP requests.
/// Collects comprehensive metrics including response times, throughput, and percentiles.

use reqwest;
use serde::Serialize;
use std::fs::File;
use std::io::Write;
use std::time::{Duration, Instant};
use tokio;

#[derive(Debug, Serialize)]
struct RequestResult {
    id: usize,
    success: bool,
    response_time_ms: f64,
    timestamp: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
}

#[derive(Debug, Serialize)]
struct ResponseTimes {
    min_ms: f64,
    max_ms: f64,
    average_ms: f64,
    median_ms: f64,
    p95_ms: f64,
    p99_ms: f64,
}

#[derive(Debug, Serialize)]
struct TimeseriesPoint {
    timestamp: f64,
    response_time_ms: f64,
}

#[derive(Debug, Serialize)]
struct Metrics {
    language: String,
    total_requests: usize,
    successful_requests: usize,
    failed_requests: usize,
    total_time_seconds: f64,
    requests_per_second: f64,
    response_times: ResponseTimes,
    timeseries: Vec<TimeseriesPoint>,
}

/// Make a single HTTP request with timing
async fn make_request(
    client: &reqwest::Client,
    url: &str,
    request_id: usize,
    start_time: Instant,
) -> RequestResult {
    let request_start = Instant::now();
    
    match client.get(url).send().await {
        Ok(response) => {
            let success = response.status().is_success();
            // Read the body to complete the request
            let _ = response.text().await;
            let request_end = Instant::now();
            
            RequestResult {
                id: request_id,
                success,
                response_time_ms: request_end.duration_since(request_start).as_secs_f64() * 1000.0,
                timestamp: request_end.duration_since(start_time).as_secs_f64(),
                error: None,
            }
        }
        Err(e) => {
            let request_end = Instant::now();
            RequestResult {
                id: request_id,
                success: false,
                response_time_ms: request_end.duration_since(request_start).as_secs_f64() * 1000.0,
                timestamp: request_end.duration_since(start_time).as_secs_f64(),
                error: Some(e.to_string()),
            }
        }
    }
}

/// Calculate percentile from sorted vector
fn percentile(sorted_data: &[f64], p: f64) -> f64 {
    if sorted_data.is_empty() {
        return 0.0;
    }
    let index = ((sorted_data.len() as f64 * p).ceil() as usize).saturating_sub(1);
    sorted_data[index.min(sorted_data.len() - 1)]
}

/// Run API request benchmark with 1,000 concurrent requests
pub async fn run_benchmark() {
    let url = "https://jsonplaceholder.typicode.com/posts/1";
    let num_requests = 1000;

    println!("Starting benchmark: {} requests to {}", num_requests, url);

    // Create HTTP client with connection pooling
    let client = reqwest::Client::builder()
        .pool_max_idle_per_host(50)
        .timeout(Duration::from_secs(10))
        .build()
        .expect("Failed to create HTTP client");

    // Measure total time for concurrent requests
    let start_time = Instant::now();

    let mut handles = Vec::with_capacity(num_requests);
    for i in 0..num_requests {
        let client_clone = client.clone();
        let url_str = url.to_string();
        let handle = tokio::spawn(async move {
            make_request(&client_clone, &url_str, i, start_time).await
        });
        handles.push(handle);
    }

    let mut results = Vec::with_capacity(num_requests);
    for handle in handles {
        if let Ok(result) = handle.await {
            results.push(result);
        }
    }

    let end_time = Instant::now();
    let total_time = end_time.duration_since(start_time).as_secs_f64();

    // Analyze results
    let successful_results: Vec<&RequestResult> = results.iter().filter(|r| r.success).collect();
    let successful_count = successful_results.len();
    let failed_count = results.len() - successful_count;

    let mut response_times: Vec<f64> = successful_results
        .iter()
        .map(|r| r.response_time_ms)
        .collect();

    // Build metrics
    let metrics = if !response_times.is_empty() {
        response_times.sort_by(|a, b| a.partial_cmp(b).unwrap());

        let sum: f64 = response_times.iter().sum();
        let min_val = response_times[0];
        let max_val = response_times[response_times.len() - 1];

        let response_times_metrics = ResponseTimes {
            min_ms: (min_val * 100.0).round() / 100.0,
            max_ms: (max_val * 100.0).round() / 100.0,
            average_ms: ((sum / response_times.len() as f64) * 100.0).round() / 100.0,
            median_ms: (percentile(&response_times, 0.5) * 100.0).round() / 100.0,
            p95_ms: (percentile(&response_times, 0.95) * 100.0).round() / 100.0,
            p99_ms: (percentile(&response_times, 0.99) * 100.0).round() / 100.0,
        };

        let timeseries: Vec<TimeseriesPoint> = successful_results
            .iter()
            .map(|r| TimeseriesPoint {
                timestamp: (r.timestamp * 1000.0).round() / 1000.0,
                response_time_ms: (r.response_time_ms * 100.0).round() / 100.0,
            })
            .collect();

        Metrics {
            language: "rust".to_string(),
            total_requests: num_requests,
            successful_requests: successful_count,
            failed_requests: failed_count,
            total_time_seconds: (total_time * 100.0).round() / 100.0,
            requests_per_second: ((num_requests as f64 / total_time) * 100.0).round() / 100.0,
            response_times: response_times_metrics,
            timeseries,
        }
    } else {
        Metrics {
            language: "rust".to_string(),
            total_requests: num_requests,
            successful_requests: 0,
            failed_requests: failed_count,
            total_time_seconds: (total_time * 100.0).round() / 100.0,
            requests_per_second: 0.0,
            response_times: ResponseTimes {
                min_ms: 0.0,
                max_ms: 0.0,
                average_ms: 0.0,
                median_ms: 0.0,
                p95_ms: 0.0,
                p99_ms: 0.0,
            },
            timeseries: Vec::new(),
        }
    };

    // Save results to JSON file
    let output_file = "api_results.json";
    let json_data = serde_json::to_string_pretty(&metrics).expect("Failed to serialize JSON");

    let mut file = File::create(output_file).expect("Failed to create output file");
    file.write_all(json_data.as_bytes())
        .expect("Failed to write to output file");

    println!("\nResults saved to {}", output_file);

    // Print results
    print_results(&metrics);
}

fn print_results(metrics: &Metrics) {
    println!("\n{}", "=".repeat(60));
    println!("Language: {}", metrics.language.to_uppercase());
    println!("{}", "=".repeat(60));
    println!("Total Requests: {}", metrics.total_requests);
    println!("Successful: {}", metrics.successful_requests);
    println!("Failed: {}", metrics.failed_requests);
    println!("Total Time: {:.2}s", metrics.total_time_seconds);
    println!("Requests/sec: {:.2}", metrics.requests_per_second);

    if metrics.successful_requests > 0 {
        println!("\nResponse Times (ms):");
        println!("  Min: {:.2}", metrics.response_times.min_ms);
        println!("  Max: {:.2}", metrics.response_times.max_ms);
        println!("  Avg: {:.2}", metrics.response_times.average_ms);
        println!("  Median: {:.2}", metrics.response_times.median_ms);
        println!("  P95: {:.2}", metrics.response_times.p95_ms);
        println!("  P99: {:.2}", metrics.response_times.p99_ms);
    }
    println!("{}\n", "=".repeat(60));
}
