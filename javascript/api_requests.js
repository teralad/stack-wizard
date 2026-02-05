/**
 * JavaScript/Node.js API Request Performance Test
 * Uses native https module with Promise.all for concurrent requests.
 * Collects comprehensive metrics including response times, throughput, and percentiles.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

/**
 * Make a single HTTP request and track timing.
 */
function makeRequest(url, requestId, startTime) {
    const requestStart = performance.now();
    
    return new Promise((resolve) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                const requestEnd = performance.now();
                resolve({
                    id: requestId,
                    success: res.statusCode === 200,
                    response_time_ms: requestEnd - requestStart,
                    timestamp: (requestEnd - startTime) / 1000
                });
            });
        }).on('error', (err) => {
            const requestEnd = performance.now();
            resolve({
                id: requestId,
                success: false,
                response_time_ms: requestEnd - requestStart,
                timestamp: (requestEnd - startTime) / 1000,
                error: err.message
            });
        });
    });
}

/**
 * Calculate percentile from sorted array.
 */
function percentile(arr, p) {
    if (arr.length === 0) return 0;
    const index = Math.ceil(arr.length * p) - 1;
    return arr[Math.max(0, Math.min(index, arr.length - 1))];
}

/**
 * Run API request benchmark with 1,000 concurrent requests.
 * Uses native https module with connection pooling.
 */
async function runBenchmark() {
    const url = "https://jsonplaceholder.typicode.com/posts/1";
    const numRequests = 1000;
    
    console.log(`Starting benchmark: ${numRequests} requests to ${url}`);
    
    // Increase max sockets for better concurrency
    https.globalAgent.maxSockets = 50;
    
    // Measure total time for concurrent requests
    const startTime = performance.now();
    
    const promises = Array.from({ length: numRequests }, (_, i) => 
        makeRequest(url, i, startTime)
    );
    
    const results = await Promise.all(promises);
    
    const endTime = performance.now();
    const totalTime = (endTime - startTime) / 1000; // Convert to seconds
    
    // Analyze results
    const successfulResults = results.filter(r => r.success);
    const failedResults = results.filter(r => !r.success);
    
    const successfulCount = successfulResults.length;
    const failedCount = failedResults.length;
    
    // Extract response times from successful requests
    const responseTimes = successfulResults.map(r => r.response_time_ms);
    
    let metrics;
    
    if (responseTimes.length > 0) {
        const sortedTimes = responseTimes.slice().sort((a, b) => a - b);
        const sum = responseTimes.reduce((acc, val) => acc + val, 0);
        
        metrics = {
            language: 'javascript',
            total_requests: numRequests,
            successful_requests: successfulCount,
            failed_requests: failedCount,
            total_time_seconds: parseFloat(totalTime.toFixed(2)),
            requests_per_second: parseFloat((numRequests / totalTime).toFixed(2)),
            response_times: {
                min_ms: parseFloat(Math.min(...responseTimes).toFixed(2)),
                max_ms: parseFloat(Math.max(...responseTimes).toFixed(2)),
                average_ms: parseFloat((sum / responseTimes.length).toFixed(2)),
                median_ms: parseFloat(percentile(sortedTimes, 0.5).toFixed(2)),
                p95_ms: parseFloat(percentile(sortedTimes, 0.95).toFixed(2)),
                p99_ms: parseFloat(percentile(sortedTimes, 0.99).toFixed(2))
            },
            timeseries: successfulResults.map(r => ({
                timestamp: parseFloat(r.timestamp.toFixed(3)),
                response_time_ms: parseFloat(r.response_time_ms.toFixed(2))
            }))
        };
    } else {
        metrics = {
            language: 'javascript',
            total_requests: numRequests,
            successful_requests: 0,
            failed_requests: failedCount,
            total_time_seconds: parseFloat(totalTime.toFixed(2)),
            requests_per_second: 0,
            response_times: {},
            timeseries: []
        };
    }
    
    // Save results to JSON file
    const outputFile = path.join(__dirname, 'api_results.json');
    fs.writeFileSync(outputFile, JSON.stringify(metrics, null, 2));
    
    console.log(`\nResults saved to ${outputFile}`);
    
    return metrics;
}

/**
 * Print formatted results to console.
 */
function printResults(metrics) {
    console.log('\n' + '='.repeat(60));
    console.log(`Language: ${metrics.language.toUpperCase()}`);
    console.log('='.repeat(60));
    console.log(`Total Requests: ${metrics.total_requests}`);
    console.log(`Successful: ${metrics.successful_requests}`);
    console.log(`Failed: ${metrics.failed_requests}`);
    console.log(`Total Time: ${metrics.total_time_seconds.toFixed(2)}s`);
    console.log(`Requests/sec: ${metrics.requests_per_second.toFixed(2)}`);
    
    if (Object.keys(metrics.response_times).length > 0) {
        console.log('\nResponse Times (ms):');
        console.log(`  Min: ${metrics.response_times.min_ms.toFixed(2)}`);
        console.log(`  Max: ${metrics.response_times.max_ms.toFixed(2)}`);
        console.log(`  Avg: ${metrics.response_times.average_ms.toFixed(2)}`);
        console.log(`  Median: ${metrics.response_times.median_ms.toFixed(2)}`);
        console.log(`  P95: ${metrics.response_times.p95_ms.toFixed(2)}`);
        console.log(`  P99: ${metrics.response_times.p99_ms.toFixed(2)}`);
    }
    console.log('='.repeat(60) + '\n');
}

if (require.main === module) {
    runBenchmark().then(metrics => {
        printResults(metrics);
    }).catch(err => {
        console.error('Benchmark failed:', err);
        process.exit(1);
    });
}

module.exports = { runBenchmark };
