# Testing Guide for New Language Implementations

This document provides instructions for testing the newly added Elixir, C#, and Scala implementations.

## Overview

The API request benchmarks for Elixir, C#, and Scala now include comprehensive test frameworks that can verify functionality **without requiring external network access**. These tests use mock HTTP servers to simulate API responses, allowing for reliable and fast testing in any environment.

## Testing Frameworks

### Elixir - Bypass
- **Framework**: ExUnit (built-in testing framework)
- **HTTP Mocking**: Bypass library
- **Purpose**: Mock HTTP endpoints for isolated API testing

### C# - xUnit + WireMock.Net
- **Framework**: xUnit
- **HTTP Mocking**: WireMock.Net
- **Purpose**: Integration testing with simulated HTTP responses

### Scala - ScalaTest + WireMock
- **Framework**: ScalaTest
- **HTTP Mocking**: WireMock JRE8
- **Purpose**: Functional testing with mock HTTP server

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

#### Running Unit Tests

```bash
cd elixir

# Install dependencies (including test dependencies)
mix deps.get

# Run all unit tests
mix test

# Run tests with verbose output
mix test --trace

# Run specific test file
mix test test/api_requests_test.exs
```

#### Running Benchmarks

```bash
cd elixir

# Run all benchmarks
elixir run_all.exs

# Run individual benchmarks
mix run -e "Sorting.run_benchmark()"
mix run -e "Fibonacci.run_benchmark()"
mix run -e "Matrix.run_benchmark()"
mix run -e "Strings.run_benchmark()"
mix run -e "ApiRequests.run_benchmark()"
```

**Test Coverage**:
- HTTP request success handling (200 OK)
- HTTP error handling (404, 500, etc.)
- Network error handling
- Percentile calculations (median, P95, P99)
- Concurrent request processing
- Metrics structure validation

### C#

#### Running Unit Tests

```bash
cd csharp

# Restore dependencies
dotnet restore

# Run all unit tests
cd Tests
dotnet test

# Run tests with detailed output
dotnet test --verbosity detailed

# Run specific test
dotnet test --filter "FullyQualifiedName~ApiRequestsTests.MakeRequest_Returns_Success_For_200_Response"
```

#### Running Benchmarks

```bash
cd csharp

# Build the project
dotnet build

# Run all benchmarks
dotnet run

# The project runs all 5 benchmarks in sequence
```

**Test Coverage**:
- HTTP request success handling (200 OK)
- HTTP error handling (404, 500, etc.)
- Request timeout handling
- Percentile calculations (median, P95, P99)
- Concurrent request processing (100 requests)
- Metrics structure validation

### Scala

#### Running Unit Tests

```bash
cd scala

# Compile the project
sbt compile

# Run all unit tests
sbt test

# Run specific test suite
sbt "testOnly ApiRequestsSpec"

# Run tests with detailed output
sbt "testOnly * -- -oD"
```

#### Running Benchmarks

```bash
cd scala

# Run all benchmarks
sbt run

# Run individual benchmarks
sbt "runMain Sorting"
sbt "runMain Fibonacci"
sbt "runMain Matrix"
sbt "runMain Strings"
sbt "runMain ApiRequests"
```

**Test Coverage**:
- HTTP request success handling (200 OK)
- HTTP error handling (404, 500, etc.)
- Network error handling
- Percentile calculations (median, P95, P99)
- Concurrent request processing (parallel collections)
- Metrics structure validation

## Test Architecture

### Why Mock HTTP Servers?

The API benchmarks make HTTP requests to external services (jsonplaceholder.typicode.com). Testing these APIs poses several challenges:

1. **Network Dependency**: External APIs may be unavailable or rate-limited
2. **Consistency**: External responses can vary, making tests unreliable
3. **Speed**: Network latency slows down test execution
4. **Isolation**: Tests should work in restricted environments (CI/CD, air-gapped systems)

By using mock HTTP servers, we can:
- Test API logic without external dependencies
- Ensure fast, reliable, and repeatable tests
- Simulate various scenarios (errors, timeouts, different status codes)
- Validate metrics calculation and data processing

### Test Implementation Details

#### Elixir - Bypass
Bypass is a lightweight library that creates a real HTTP server on a random port for testing. Tests can configure endpoints and responses programmatically.

```elixir
# Example test structure
setup do
  bypass = Bypass.open()
  {:ok, bypass: bypass}
end

test "handles 200 response", %{bypass: bypass} do
  Bypass.expect_once(bypass, "GET", "/posts/1", fn conn ->
    Plug.Conn.resp(conn, 200, ~s({"id": 1}))
  end)
  
  url = "http://localhost:#{bypass.port}/posts/1"
  result = ApiRequests.make_request(url, 1, start_time)
  
  assert result.success == true
end
```

#### C# - WireMock.Net
WireMock.Net is a flexible library for stubbing and mocking HTTP services. It provides a fluent API for setting up request/response expectations.

```csharp
// Example test structure
var mockServer = WireMockServer.Start();

mockServer
    .Given(Request.Create().WithPath("/posts/1").UsingGet())
    .RespondWith(Response.Create()
        .WithStatusCode(200)
        .WithBody("{\"id\": 1}"));

string url = $"{mockServer.Url}/posts/1";
var response = await httpClient.GetAsync(url);

Assert.True(response.IsSuccessStatusCode);
```

#### Scala - WireMock
WireMock is the original Java library for HTTP mocking, fully compatible with Scala. It provides comprehensive stubbing capabilities.

```scala
// Example test structure
val wireMockServer = new WireMockServer(wireMockConfig().dynamicPort())
wireMockServer.start()

stubFor(get(urlEqualTo("/posts/1"))
  .willReturn(aResponse()
    .withStatus(200)
    .withBody("""{"id": 1}""")))

val url = s"http://localhost:${wireMockServer.port()}/posts/1"
val result = ApiRequests.makeRequest(backend, url, 1, startTime)

result.success shouldBe true
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

### Elixir Tests
- **Error: Mix not found**: Install Elixir and ensure it's in your PATH
- **Dependency errors**: Run `mix deps.get` again
- **Bypass errors**: Ensure Bypass dependency is installed with `mix deps.get`
- **Test failures**: Check that tests are using the mocked server URL, not external URLs
- **Port conflicts**: Bypass uses random ports, so conflicts are unlikely, but ensure no firewall blocking

### C# Tests
- **Framework not found**: Tests require .NET 8.0+ SDK
- **Compilation errors**: Run `dotnet clean` in Tests directory, then `dotnet restore` and `dotnet build`
- **WireMock errors**: Ensure WireMock.Net package is properly restored
- **Test project not found**: Verify Tests/StackWizard.Tests.csproj exists
- **Port conflicts**: WireMock uses dynamic ports, but ensure firewall allows local connections

### Scala Tests
- **sbt errors**: Clear cache with `sbt clean`
- **WireMock errors**: First compilation downloads WireMock JAR, this may take time
- **Test compilation slow**: First test compilation downloads dependencies, subsequent runs are faster
- **ClassNotFoundException**: Run `sbt clean` and `sbt test` again
- **Port conflicts**: WireMock uses dynamic ports automatically

### General Testing Tips

1. **Run tests before benchmarks**: Ensure your implementation is correct before measuring performance
2. **Mock vs Real API**: Use mock tests for development/CI, real API for actual performance benchmarks
3. **Test isolation**: Each test should be independent and not affect others
4. **Parallel execution**: Most test frameworks run tests in parallel by default
5. **Flaky tests**: If tests occasionally fail, check for timing issues or resource cleanup

### Network Dependency Issues

If you still need to run benchmarks with real APIs:
- Ensure internet connectivity
- Check if `jsonplaceholder.typicode.com` is accessible
- Consider rate limiting - space out requests if running benchmarks repeatedly
- Use VPN or proxy if needed for restricted networks
- For CI/CD, consider setting up a local mock API server

## Continuous Integration

### Running Tests in CI/CD

Example GitHub Actions workflow:

```yaml
name: Test API Implementations

on: [push, pull_request]

jobs:
  test-csharp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0.x'
      - name: Run C# tests
        run: |
          cd csharp/Tests
          dotnet test --logger "console;verbosity=detailed"
  
  test-elixir:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: erlef/setup-beam@v1
        with:
          elixir-version: '1.14'
          otp-version: '25'
      - name: Run Elixir tests
        run: |
          cd elixir
          mix deps.get
          mix test
  
  test-scala:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'
      - name: Run Scala tests
        run: |
          cd scala
          sbt test
```

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
