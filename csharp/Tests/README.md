# C# API Tests

This directory contains unit and integration tests for the C# API request implementation.

## Test Framework

- **Testing Framework**: xUnit
- **HTTP Mocking**: WireMock.Net
- **Test Runner**: dotnet test

## Running Tests

```bash
# From the csharp directory
cd Tests

# Restore dependencies
dotnet restore

# Run all tests
dotnet test

# Run with verbose output
dotnet test --verbosity detailed

# Run specific test
dotnet test --filter "FullyQualifiedName~MakeRequest_Returns_Success_For_200_Response"
```

## Test Coverage

The test suite covers:

1. **Success Cases**
   - HTTP 200 OK responses
   - Response time measurement
   - Timestamp tracking

2. **Error Handling**
   - Non-200 HTTP status codes (404, 500, etc.)
   - Network timeouts
   - Connection failures

3. **Concurrency**
   - Multiple simultaneous requests (100 concurrent)
   - Proper request completion
   - Result aggregation

4. **Metrics Calculation**
   - Percentile calculations (median, P95, P99)
   - Response time statistics
   - Request success/failure counting

5. **Data Validation**
   - Metrics structure correctness
   - JSON serialization compatibility
   - Time series data collection

## Test Architecture

Tests use WireMock.Net to create a local HTTP server that simulates the jsonplaceholder API. This allows:
- Fast test execution (no network latency)
- Reliable tests (no external dependencies)
- Consistent results (controlled responses)
- Offline testing (no internet required)

Each test:
1. Starts a WireMock server on a dynamic port
2. Configures expected requests and responses
3. Executes the code under test
4. Validates results
5. Cleans up the server

## Dependencies

Test-specific dependencies (defined in StackWizard.Tests.csproj):
- `xunit` - Test framework
- `xunit.runner.visualstudio` - Visual Studio test runner
- `Microsoft.NET.Test.Sdk` - Test SDK
- `WireMock.Net` - HTTP mocking library
- `coverlet.collector` - Code coverage collector

## CI/CD Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run C# Tests
  run: |
    cd csharp/Tests
    dotnet test --logger "trx;LogFileName=test-results.trx"
```

## Adding New Tests

To add new test cases:

1. Create a new test method in `ApiRequestsTests.cs`
2. Add the `[Fact]` attribute
3. Follow the Arrange-Act-Assert pattern
4. Use WireMock to mock HTTP responses
5. Run tests to verify

Example:

```csharp
[Fact]
public async Task NewTest_Description()
{
    // Arrange
    _mockServer
        .Given(Request.Create().WithPath("/endpoint").UsingGet())
        .RespondWith(Response.Create()
            .WithStatusCode(200)
            .WithBody("{\"data\": \"value\"}"));

    // Act
    var result = await SomeMethod();

    // Assert
    Assert.True(result.Success);
}
```
