/**
 * Reverse a string.
 */
function reverseString(s) {
    return s.split('').reverse().join('');
}

/**
 * Concatenate strings multiple times.
 */
function concatenateStrings(iterations) {
    let result = "";
    for (let i = 0; i < iterations; i++) {
        result += i.toString();
    }
    return result;
}

/**
 * Search for pattern in text using regex.
 */
function patternSearch(text, pattern) {
    const regex = new RegExp(pattern, 'g');
    const matches = text.match(regex);
    return matches ? matches.length : 0;
}

/**
 * Run string manipulation benchmarks.
 */
function runBenchmark() {
    const results = [];
    
    // String reversal on 1 million character string
    const largeString = 'a'.repeat(1000000);
    const startTimeReverse = performance.now();
    const reversedStr = reverseString(largeString);
    const endTimeReverse = performance.now();
    const executionTimeReverse = endTimeReverse - startTimeReverse;
    
    results.push({
        testName: 'String Reversal (1M chars)',
        executionTimeMs: executionTimeReverse,
        stringLength: largeString.length
    });
    
    // String concatenation (10,000 iterations)
    const startTimeConcat = performance.now();
    const concatenated = concatenateStrings(10000);
    const endTimeConcat = performance.now();
    const executionTimeConcat = endTimeConcat - startTimeConcat;
    
    results.push({
        testName: 'String Concatenation (10K iterations)',
        executionTimeMs: executionTimeConcat,
        resultLength: concatenated.length
    });
    
    // Pattern searching
    const text = 'Lorem ipsum dolor sit amet '.repeat(10000);
    const pattern = '\\b\\w{5}\\b'; // Find all 5-letter words
    const startTimeSearch = performance.now();
    const matches = patternSearch(text, pattern);
    const endTimeSearch = performance.now();
    const executionTimeSearch = endTimeSearch - startTimeSearch;
    
    results.push({
        testName: 'Pattern Search',
        executionTimeMs: executionTimeSearch,
        matchesFound: matches
    });
    
    return results;
}

if (require.main === module) {
    const results = runBenchmark();
    results.forEach(result => {
        console.log(`Test: ${result.testName}`);
        console.log(`Execution time: ${result.executionTimeMs.toFixed(2)} ms`);
        if (result.stringLength) console.log(`String length: ${result.stringLength}`);
        if (result.resultLength) console.log(`Result length: ${result.resultLength}`);
        if (result.matchesFound !== undefined) console.log(`Matches found: ${result.matchesFound}`);
        console.log();
    });
}

module.exports = { runBenchmark };
