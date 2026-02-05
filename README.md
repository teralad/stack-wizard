# Stack Wizard - Multi-Language Performance Comparison Suite

A comprehensive performance benchmarking suite that implements identical algorithms across 7 programming languages: **Python**, **JavaScript (Node.js)**, **Go**, **Rust**, **Java**, **C++**, and **Ruby**.

## 📋 Overview

This project benchmarks the same 5 performance-critical operations across all languages to provide a fair comparison of runtime performance. Each implementation uses standard library features and similar optimization levels to ensure fairness.

## 🧪 Benchmark Tests

### 1. Sorting Algorithm (Quicksort)
- **Algorithm**: Quicksort implementation
- **Dataset**: 100,000 random integers
- **Metric**: Time to sort the entire array

### 2. Fibonacci Calculation
- **Recursive**: Calculate fibonacci(35)
- **Iterative**: Calculate fibonacci(40)
- **Metric**: Execution time for each approach

### 3. Matrix Multiplication
- **Algorithm**: Standard matrix multiplication
- **Dataset**: Two 100x100 matrices with random values
- **Metric**: Time to multiply matrices

### 4. String Manipulation
- **String Reversal**: Reverse a 1 million character string
- **String Concatenation**: 10,000 iterations
- **Pattern Search**: Find 5-letter words in large text using regex
- **Metric**: Time for each operation

### 5. API Requests
- **Operation**: 50 concurrent HTTP GET requests
- **Endpoint**: JSONPlaceholder API (https://jsonplaceholder.typicode.com/posts/1)
- **Metric**: Total time and success rate

## 📊 Performance Comparison Tables

> **Note**: The following are example results. Run the benchmarks on your own system for actual measurements.

### Sorting (Quicksort - 100K integers)
| Language   | Execution Time | Relative Speed |
|------------|----------------|----------------|
| Rust       | ~50 ms         | 1.0x (fastest) |
| C++        | ~60 ms         | 1.2x           |
| Go         | ~120 ms        | 2.4x           |
| Java       | ~150 ms        | 3.0x           |
| JavaScript | ~200 ms        | 4.0x           |
| Python     | ~450 ms        | 9.0x           |
| Ruby       | ~800 ms        | 16.0x          |

### Fibonacci Recursive (n=35)
| Language   | Execution Time | Relative Speed |
|------------|----------------|----------------|
| C++        | ~40 ms         | 1.0x (fastest) |
| Rust       | ~45 ms         | 1.1x           |
| Go         | ~50 ms         | 1.25x          |
| Java       | ~55 ms         | 1.4x           |
| JavaScript | ~150 ms        | 3.8x           |
| Python     | ~3500 ms       | 87.5x          |
| Ruby       | ~7000 ms       | 175.0x         |

### Fibonacci Iterative (n=40)
| Language   | Execution Time | Relative Speed |
|------------|----------------|----------------|
| Rust       | <1 ms          | 1.0x (fastest) |
| C++        | <1 ms          | 1.0x           |
| Go         | <1 ms          | 1.0x           |
| Java       | <1 ms          | 1.0x           |
| JavaScript | <1 ms          | 1.0x           |
| Python     | <1 ms          | 1.0x           |
| Ruby       | <1 ms          | 1.0x           |

### Matrix Multiplication (100x100)
| Language   | Execution Time | Relative Speed |
|------------|----------------|----------------|
| Rust       | ~15 ms         | 1.0x (fastest) |
| C++        | ~18 ms         | 1.2x           |
| Go         | ~25 ms         | 1.7x           |
| Java       | ~30 ms         | 2.0x           |
| JavaScript | ~40 ms         | 2.7x           |
| Python     | ~250 ms        | 16.7x          |
| Ruby       | ~400 ms        | 26.7x          |

### String Operations
| Language   | Reversal (1M) | Concatenation (10K) | Pattern Search |
|------------|---------------|---------------------|----------------|
| Rust       | ~5 ms         | ~1 ms               | ~20 ms         |
| C++        | ~8 ms         | ~2 ms               | ~25 ms         |
| Go         | ~10 ms        | ~5 ms               | ~30 ms         |
| Java       | ~12 ms        | ~3 ms               | ~35 ms         |
| JavaScript | ~15 ms        | ~100 ms             | ~40 ms         |
| Python     | ~20 ms        | ~300 ms             | ~50 ms         |
| Ruby       | ~25 ms        | ~500 ms             | ~60 ms         |

### API Requests (50 concurrent)
| Language   | Execution Time | Success Rate |
|------------|----------------|--------------|
| Go         | ~200 ms        | 100%         |
| Rust       | ~250 ms        | 100%         |
| JavaScript | ~300 ms        | 100%         |
| Java       | ~350 ms        | 100%         |
| C++        | ~400 ms        | 100%         |
| Python     | ~500 ms        | 100%         |
| Ruby       | ~600 ms        | 100%         |

## 🚀 Setup Instructions

### Python
```bash
cd python
pip install -r requirements.txt
python run_all.py
```

**Individual tests:**
```bash
python sorting.py
python fibonacci.py
python matrix.py
python strings.py
python api_requests.py
```

### JavaScript (Node.js)
```bash
cd javascript
npm install  # No dependencies, but creates package-lock
node run_all.js
```

**Individual tests:**
```bash
node sorting.js
node fibonacci.js
node matrix.js
node strings.js
node api_requests.js
```

### Go
```bash
cd go
go mod download
go run main.go
```

**Individual tests:**
```bash
go run sorting.go
go run fibonacci.go
go run matrix.go
go run strings.go
go run api_requests.go
```

### Rust
```bash
cd rust
cargo build --release
cargo run --release
```

**Note**: Always use `--release` flag for accurate performance measurements.

### Java
```bash
cd java
mvn compile
mvn exec:java -Dexec.mainClass="Main"
```

**Individual tests:**
```bash
mvn exec:java -Dexec.mainClass="Sorting"
mvn exec:java -Dexec.mainClass="Fibonacci"
mvn exec:java -Dexec.mainClass="Matrix"
mvn exec:java -Dexec.mainClass="Strings"
mvn exec:java -Dexec.mainClass="ApiRequests"
```

### C++
```bash
cd cpp
mkdir build && cd build
cmake ..
make
```

**Run individual tests:**
```bash
./sorting
./fibonacci
./matrix
./strings
./api_requests
```

**Note**: Requires libcurl for API requests: `sudo apt-get install libcurl4-openssl-dev` (Ubuntu/Debian)

### Ruby
```bash
cd ruby
bundle install  # No gems needed, but good practice
ruby run_all.rb
```

**Individual tests:**
```bash
ruby sorting.rb
ruby fibonacci.rb
ruby matrix.rb
ruby strings.rb
ruby api_requests.rb
```

## 📦 Dependencies

### Python
- `requests` - For HTTP requests

### JavaScript
- Standard library only (built-in `https` module)

### Go
- Standard library only

### Rust
- `rand` - Random number generation
- `regex` - Regular expressions
- `reqwest` - HTTP client
- `tokio` - Async runtime

### Java
- JDK 11+ (uses built-in HTTP client from Java 11)
- Maven for build management

### C++
- C++17 compiler (gcc/clang)
- libcurl - For HTTP requests
- CMake for build management

### Ruby
- Standard library only

## 🎯 Key Findings

### General Observations

1. **Compiled Languages Dominate**: Rust, C++, and Go consistently outperform interpreted languages
2. **JIT Advantage**: Java's JIT compilation provides competitive performance after warmup
3. **Python/Ruby Trade-off**: Slower execution but faster development and cleaner syntax
4. **String Operations**: Language-specific optimizations vary significantly
5. **Concurrency**: Go excels in concurrent operations due to goroutines
6. **Memory Safety**: Rust provides C++ performance with memory safety guarantees

### Language-Specific Notes

- **Rust**: Fastest overall, excellent memory management, steep learning curve
- **C++**: Very fast, requires manual memory management, more complex
- **Go**: Great balance of performance and simplicity, excellent for concurrent tasks
- **Java**: Strong performance with JIT, verbose syntax, large ecosystem
- **JavaScript**: Surprisingly fast for an interpreted language, V8 engine optimizations
- **Python**: Slowest but most readable, vast library ecosystem
- **Ruby**: Similar to Python in performance, elegant syntax

## ⚙️ Fair Comparison Practices

To ensure fair comparisons:

1. **Standard Libraries**: Used built-in features where possible
2. **Optimization Levels**:
   - Rust: `--release` flag (optimization level 3)
   - C++: `-O2` optimization flag
   - Go: Default optimizations
   - Java: JIT warmup included in measurements
   - JavaScript: V8 engine default optimizations
   - Python: Default interpreter
   - Ruby: Default interpreter

3. **Same Algorithms**: Identical logic across all implementations
4. **Same Data**: Identical test datasets and parameters
5. **Timing**: Measured actual execution time, excluding initialization

## 💻 System Specifications

For reproducible results, run benchmarks on your own hardware. Example specs:

```
Processor: Intel Core i7-9700K @ 3.60GHz (8 cores)
RAM: 32GB DDR4
OS: Ubuntu 22.04 LTS
Python: 3.10.12
Node.js: v18.17.0
Go: 1.21.0
Rust: 1.73.0
Java: OpenJDK 17.0.8
GCC: 11.4.0
Ruby: 3.1.2
```

## 🔧 Running All Benchmarks

To run all benchmarks sequentially, you can use this bash script:

```bash
#!/bin/bash

echo "Running all benchmarks..."

echo -e "\n=== Python ==="
cd python && python3 run_all.py && cd ..

echo -e "\n=== JavaScript ==="
cd javascript && node run_all.js && cd ..

echo -e "\n=== Go ==="
cd go && go run main.go && cd ..

echo -e "\n=== Rust ==="
cd rust && cargo run --release && cd ..

echo -e "\n=== Java ==="
cd java && mvn -q exec:java -Dexec.mainClass="Main" && cd ..

echo -e "\n=== C++ ==="
cd cpp/build && ./sorting && ./fibonacci && ./matrix && ./strings && ./api_requests && cd ../..

echo -e "\n=== Ruby ==="
cd ruby && ruby run_all.rb && cd ..

echo -e "\nAll benchmarks completed!"
```

Save as `run_all_languages.sh` and execute with `bash run_all_languages.sh`

## 📝 Notes

- **Warmup**: Some languages (especially Java) benefit from JIT warmup. Results may vary on first run.
- **Network**: API benchmark results depend on network conditions and API rate limiting.
- **Hardware**: Performance varies significantly based on CPU, RAM, and system load.
- **Randomness**: Tests using random data may show slight variations between runs.

## 🤝 Contributing

Feel free to contribute by:
- Adding more benchmark tests
- Optimizing implementations (while keeping them comparable)
- Adding more languages
- Improving documentation
- Reporting issues or results from your system

## 📄 License

MIT License - Feel free to use this for learning and comparison purposes.

## 🔗 Useful Links

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Node.js Performance Best Practices](https://nodejs.org/en/docs/guides/simple-profiling/)
- [Go Performance](https://go.dev/doc/effective_go#performance)
- [Rust Performance Book](https://nnethercote.github.io/perf-book/)
- [Java Performance Tuning](https://docs.oracle.com/javase/8/docs/technotes/guides/vm/performance-enhancements-7.html)
- [C++ Optimization](https://en.cppreference.com/w/cpp/compiler_support/17)
- [Ruby Performance](https://www.speedshop.co/2015/07/29/scaling-ruby-apps-to-1000-rpm.html)

---

**Created for educational and benchmarking purposes. Results may vary based on implementation details, compiler versions, and hardware.**