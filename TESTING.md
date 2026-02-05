# Testing Guide for New Language Implementations

This document provides instructions for testing the newly added Elixir, C#, and Scala implementations.

## Prerequisites

### Elixir
- Elixir 1.14 or higher
- Mix (comes with Elixir)
- Install with: 
  - macOS: `brew install elixir`
  - Ubuntu/Debian: `sudo apt-get install elixir`
  - Windows: Download from https://elixir-lang.org/install.html

### C#
- .NET SDK 8.0 or higher (tested with .NET 8.0)
- Install from: https://dotnet.microsoft.com/download
- Verify installation: `dotnet --version`

### Scala
- Scala 2.13 or higher
- sbt (Scala Build Tool)
- Install with:
  - macOS: `brew install sbt`
  - Ubuntu/Debian: See https://www.scala-sbt.org/download.html
  - Windows: Download from https://www.scala-sbt.org/download.html

## Running Tests

### Elixir

```bash
cd elixir

# Install dependencies
mix deps.get

# Run all benchmarks
elixir run_all.exs

# Run individual tests
mix run -e "Sorting.run_benchmark()"
mix run -e "Fibonacci.run_benchmark()"
mix run -e "Matrix.run_benchmark()"
mix run -e "Strings.run_benchmark()"
mix run -e "ApiRequests.run_benchmark()"
```

### C#

```bash
cd csharp

# Restore dependencies
dotnet restore

# Build the project
dotnet build

# Run all benchmarks
dotnet run

# The project runs all 5 benchmarks in sequence
```

### Scala

```bash
cd scala

# Compile the project
sbt compile

# Run all benchmarks
sbt run

# Run individual tests
sbt "runMain Sorting"
sbt "runMain Fibonacci"
sbt "runMain Matrix"
sbt "runMain Strings"
sbt "runMain ApiRequests"
```

## Expected Output

Each implementation should:
1. Display timing results for each benchmark
2. Generate an `api_results.json` file after running the API test
3. Show correct results (e.g., sorted arrays, correct Fibonacci numbers)

### Sample Output (C# Sorting)

```
=== Sorting (Quicksort) ===
Array size: 100000
Execution time: 164.98 ms
Correctly sorted: True
```

### Sample API Results JSON

```json
{
  "language": "csharp",
  "total_requests": 10000,
  "successful_requests": 10000,
  "failed_requests": 0,
  "total_time_seconds": 14.87,
  "requests_per_second": 672.45,
  "response_times": {
    "min_ms": 38.92,
    "max_ms": 498.33,
    "average_ms": 92.15,
    "median_ms": 88.44,
    "p95_ms": 158.21,
    "p99_ms": 195.66
  },
  "timeseries": [...]
}
```

## Verification

### 1. Functionality Tests
- **Sorting**: Array should be correctly sorted (ascending order)
- **Fibonacci**: Results should match known values (fib(35) = 9227465, fib(40) = 102334155)
- **Matrix**: Result should be 100x100 matrix
- **Strings**: Should find expected number of 5-letter words
- **API**: Should generate valid JSON with all required fields

### 2. Performance Benchmarks
Run multiple times and compare:
- Compiled languages (C#, Scala) should have similar performance to Java
- Elixir should show good concurrency performance for API tests
- All implementations should complete without errors

### 3. JSON Schema Validation
The `api_results.json` file must include:
- `language`: string
- `total_requests`: integer
- `successful_requests`: integer
- `failed_requests`: integer
- `total_time_seconds`: float
- `requests_per_second`: float
- `response_times`: object with min_ms, max_ms, average_ms, median_ms, p95_ms, p99_ms
- `timeseries`: array of {timestamp, response_time_ms} objects

## Integration with Visualizations

After running API tests for all languages:

```bash
cd visualizations
pip install -r requirements.txt
python generate_graphs.py
```

This will:
- Read `api_results.json` from all 10 language directories
- Generate comparison graphs in `visualizations/graphs/`
- Create an interactive HTML dashboard

## Troubleshooting

### Elixir
- **Error: Mix not found**: Install Elixir and ensure it's in your PATH
- **Dependency errors**: Run `mix deps.get` again
- **HTTPoison errors**: Check network connectivity

### C#
- **Framework not found**: Requires .NET 8.0+ (modify `StackWizard.csproj` `<TargetFramework>` to match your version if needed)
- **Compilation errors**: Run `dotnet clean` then `dotnet build`
- **Multiple entry points**: Ensure only `Program.cs` has a `Main` method

### Scala
- **sbt errors**: Clear cache with `sbt clean`
- **Compilation slow**: First compilation downloads dependencies, subsequent builds are faster
- **Runtime errors**: Check Scala version compatibility

## Performance Notes

### API Request Tests
- **10,000 requests**: New languages implement enhanced version with 10K requests
- **1,000 requests**: Original 7 languages use 1K requests
- Network conditions affect results; run multiple times for consistency
- Consider local API mock for reproducible testing

### Expected Relative Performance
- **Fastest**: Rust, C++, Go, C#, Scala
- **Mid-range**: Java, JavaScript
- **Slower**: Python, Ruby, Elixir (for CPU-bound tasks)
- **API/Concurrency**: Elixir excels, C# and Scala also perform well

## CI/CD Integration

For automated testing:

```bash
# Install all runtimes
# Run tests for each language
# Collect metrics
# Generate visualizations
# Compare results
```

See `run_all_benchmarks.sh` for reference.
