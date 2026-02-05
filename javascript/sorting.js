/**
 * Quicksort algorithm implementation.
 */
function quicksort(arr) {
    if (arr.length <= 1) {
        return arr;
    }
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quicksort(left), ...middle, ...quicksort(right)];
}

/**
 * Run sorting benchmark with 100,000 random integers.
 */
function runBenchmark() {
    // Generate 100,000 random integers
    const arr = Array.from({ length: 100000 }, () => Math.floor(Math.random() * 1000000));
    
    // Measure sorting time
    const startTime = performance.now();
    const sortedArr = quicksort(arr);
    const endTime = performance.now();
    
    const executionTime = endTime - startTime;
    
    // Verify sorting correctness
    const isSorted = sortedArr.every((val, i, arr) => i === 0 || arr[i - 1] <= val);
    
    return {
        testName: 'Sorting (Quicksort)',
        executionTimeMs: executionTime,
        size: arr.length,
        correct: isSorted
    };
}

if (require.main === module) {
    const result = runBenchmark();
    console.log(`Test: ${result.testName}`);
    console.log(`Array size: ${result.size}`);
    console.log(`Execution time: ${result.executionTimeMs.toFixed(2)} ms`);
    console.log(`Correctly sorted: ${result.correct}`);
}

module.exports = { runBenchmark };
