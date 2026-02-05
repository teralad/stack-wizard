use reqwest;
use std::time::Instant;
use tokio;

/// Make a single HTTP request
async fn make_request(url: &str, request_id: usize) -> (usize, bool) {
    match reqwest::get(url).await {
        Ok(response) => (request_id, response.status().is_success()),
        Err(_) => (request_id, false),
    }
}

/// Run API request benchmark with 50 concurrent requests
pub async fn run_benchmark() {
    let url = "https://jsonplaceholder.typicode.com/posts/1";
    let num_requests = 50;

    // Measure total time for concurrent requests
    let start_time = Instant::now();

    let mut handles = vec![];
    for i in 0..num_requests {
        let handle = tokio::spawn(make_request(url, i));
        handles.push(handle);
    }

    let mut successful = 0;
    for handle in handles {
        if let Ok((_, success)) = handle.await {
            if success {
                successful += 1;
            }
        }
    }

    let execution_time = start_time.elapsed().as_millis();

    println!("Test: API Requests (50 concurrent)");
    println!("Total requests: {}", num_requests);
    println!("Successful requests: {}", successful);
    println!("Execution time: {} ms", execution_time);
}
