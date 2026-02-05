const https = require('https');

/**
 * Make a single HTTP request.
 */
function makeRequest(url, requestId) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                resolve({
                    id: requestId,
                    status: res.statusCode,
                    success: res.statusCode === 200
                });
            });
        }).on('error', (err) => {
            resolve({
                id: requestId,
                status: 0,
                success: false,
                error: err.message
            });
        });
    });
}

/**
 * Run API request benchmark with 50 concurrent requests.
 */
async function runBenchmark() {
    const url = "https://jsonplaceholder.typicode.com/posts/1";
    const numRequests = 50;
    
    // Measure total time for concurrent requests
    const startTime = performance.now();
    
    const promises = Array.from({ length: numRequests }, (_, i) => 
        makeRequest(url, i)
    );
    
    const results = await Promise.all(promises);
    
    const endTime = performance.now();
    const executionTime = endTime - startTime;
    
    // Count successful requests
    const successful = results.filter(r => r.success).length;
    
    return {
        testName: 'API Requests (50 concurrent)',
        executionTimeMs: executionTime,
        totalRequests: numRequests,
        successfulRequests: successful
    };
}

if (require.main === module) {
    runBenchmark().then(result => {
        console.log(`Test: ${result.testName}`);
        console.log(`Total requests: ${result.totalRequests}`);
        console.log(`Successful requests: ${result.successfulRequests}`);
        console.log(`Execution time: ${result.executionTimeMs.toFixed(2)} ms`);
    });
}

module.exports = { runBenchmark };
