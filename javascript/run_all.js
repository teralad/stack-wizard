#!/usr/bin/env node
/**
 * Run all JavaScript benchmarks.
 */
const sorting = require('./sorting');
const fibonacci = require('./fibonacci');
const matrix = require('./matrix');
const strings = require('./strings');
const apiRequests = require('./api_requests');

async function main() {
    console.log('='.repeat(60));
    console.log('JavaScript Performance Benchmarks');
    console.log('='.repeat(60));
    console.log();
    
    // Sorting
    console.log('Running Sorting Benchmark...');
    const sortingResult = sorting.runBenchmark();
    console.log(`  ${sortingResult.testName}: ${sortingResult.executionTimeMs.toFixed(2)} ms`);
    console.log();
    
    // Fibonacci
    console.log('Running Fibonacci Benchmarks...');
    const fibResults = fibonacci.runBenchmark();
    fibResults.forEach(result => {
        console.log(`  ${result.testName}: ${result.executionTimeMs.toFixed(2)} ms`);
    });
    console.log();
    
    // Matrix
    console.log('Running Matrix Multiplication Benchmark...');
    const matrixResult = matrix.runBenchmark();
    console.log(`  ${matrixResult.testName}: ${matrixResult.executionTimeMs.toFixed(2)} ms`);
    console.log();
    
    // Strings
    console.log('Running String Manipulation Benchmarks...');
    const stringResults = strings.runBenchmark();
    stringResults.forEach(result => {
        console.log(`  ${result.testName}: ${result.executionTimeMs.toFixed(2)} ms`);
    });
    console.log();
    
    // API Requests
    console.log('Running API Request Benchmark...');
    const apiResult = await apiRequests.runBenchmark();
    console.log(`  ${apiResult.testName}: ${apiResult.executionTimeMs.toFixed(2)} ms`);
    console.log(`  Successful: ${apiResult.successfulRequests}/${apiResult.totalRequests}`);
    console.log();
    
    console.log('='.repeat(60));
    console.log('All benchmarks completed!');
    console.log('='.repeat(60));
}

main().catch(console.error);
