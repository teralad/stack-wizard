/**
 * Standard matrix multiplication implementation.
 */
function matrixMultiply(matrixA, matrixB) {
    const rowsA = matrixA.length;
    const colsA = matrixA[0].length;
    const colsB = matrixB[0].length;
    
    // Initialize result matrix with zeros
    const result = Array.from({ length: rowsA }, () => Array(colsB).fill(0));
    
    // Perform multiplication
    for (let i = 0; i < rowsA; i++) {
        for (let j = 0; j < colsB; j++) {
            for (let k = 0; k < colsA; k++) {
                result[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }
    
    return result;
}

/**
 * Run matrix multiplication benchmark with 100x100 matrices.
 */
function runBenchmark() {
    const size = 100;
    
    // Generate two random 100x100 matrices
    const matrixA = Array.from({ length: size }, () => 
        Array.from({ length: size }, () => Math.random())
    );
    const matrixB = Array.from({ length: size }, () => 
        Array.from({ length: size }, () => Math.random())
    );
    
    // Measure multiplication time
    const startTime = performance.now();
    const result = matrixMultiply(matrixA, matrixB);
    const endTime = performance.now();
    
    const executionTime = endTime - startTime;
    
    return {
        testName: 'Matrix Multiplication',
        executionTimeMs: executionTime,
        matrixSize: `${size}x${size}`,
        resultSample: result[0][0]
    };
}

if (require.main === module) {
    const result = runBenchmark();
    console.log(`Test: ${result.testName}`);
    console.log(`Matrix size: ${result.matrixSize}`);
    console.log(`Execution time: ${result.executionTimeMs.toFixed(2)} ms`);
    console.log(`Result sample (0,0): ${result.resultSample.toFixed(6)}`);
}

module.exports = { runBenchmark };
