/**
 * Recursive Fibonacci implementation.
 */
function fibonacciRecursive(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

/**
 * Iterative Fibonacci implementation.
 */
function fibonacciIterative(n) {
    if (n <= 1) {
        return n;
    }
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}

/**
 * Run Fibonacci benchmarks.
 */
function runBenchmark() {
    const results = [];
    
    // Recursive fibonacci(35)
    const startTimeRecursive = performance.now();
    const resultRecursive = fibonacciRecursive(35);
    const endTimeRecursive = performance.now();
    const executionTimeRecursive = endTimeRecursive - startTimeRecursive;
    
    results.push({
        testName: 'Fibonacci Recursive (n=35)',
        executionTimeMs: executionTimeRecursive,
        result: resultRecursive
    });
    
    // Iterative fibonacci(40)
    const startTimeIterative = performance.now();
    const resultIterative = fibonacciIterative(40);
    const endTimeIterative = performance.now();
    const executionTimeIterative = endTimeIterative - startTimeIterative;
    
    results.push({
        testName: 'Fibonacci Iterative (n=40)',
        executionTimeMs: executionTimeIterative,
        result: resultIterative
    });
    
    return results;
}

if (require.main === module) {
    const results = runBenchmark();
    results.forEach(result => {
        console.log(`Test: ${result.testName}`);
        console.log(`Result: ${result.result}`);
        console.log(`Execution time: ${result.executionTimeMs.toFixed(2)} ms`);
        console.log();
    });
}

module.exports = { runBenchmark };
