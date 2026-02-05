defmodule ApiRequests do
  @moduledoc """
  API Request Performance Test for Elixir.
  Uses Task.async_stream for efficient concurrent HTTP requests.
  Collects comprehensive metrics including response times, throughput, and percentiles.
  """

  @doc """
  Make a single HTTP request and return timing data.
  """
  def make_request(url, request_id, start_time) do
    request_start = :os.system_time(:millisecond)
    
    result = case HTTPoison.get(url, [], recv_timeout: 10_000, timeout: 10_000) do
      {:ok, %HTTPoison.Response{status_code: 200, body: _body}} ->
        request_end = :os.system_time(:millisecond)
        %{
          id: request_id,
          success: true,
          response_time_ms: request_end - request_start,
          timestamp: (request_end - start_time) / 1000.0
        }
      
      {:ok, %HTTPoison.Response{status_code: status}} ->
        request_end = :os.system_time(:millisecond)
        %{
          id: request_id,
          success: false,
          response_time_ms: request_end - request_start,
          timestamp: (request_end - start_time) / 1000.0,
          error: "HTTP #{status}"
        }
      
      {:error, reason} ->
        request_end = :os.system_time(:millisecond)
        %{
          id: request_id,
          success: false,
          response_time_ms: request_end - request_start,
          timestamp: (request_end - start_time) / 1000.0,
          error: inspect(reason)
        }
    end
    
    result
  end

  @doc """
  Calculate percentile from sorted list.
  """
  def percentile(sorted_list, p) do
    index = round(length(sorted_list) * p) - 1
    index = max(0, min(index, length(sorted_list) - 1))
    Enum.at(sorted_list, index)
  end

  @doc """
  Run API request benchmark with 10,000 concurrent requests.
  """
  def run_benchmark do
    url = "https://jsonplaceholder.typicode.com/posts/1"
    num_requests = 1_000
    
    IO.puts("Starting benchmark: #{num_requests} requests to #{url}")
    
    # Start HTTPoison application
    HTTPoison.start()
    
    # Measure total time
    start_time = :os.system_time(:millisecond)
    
    # Make concurrent requests using Task.async_stream
    results = 0..(num_requests - 1)
              |> Task.async_stream(
                fn i -> make_request(url, i, start_time) end,
                max_concurrency: 100,
                timeout: 15_000
              )
              |> Enum.map(fn {:ok, result} -> result end)
    
    end_time = :os.system_time(:millisecond)
    total_time = (end_time - start_time) / 1000.0  # Convert to seconds
    
    # Analyze results
    successful_results = Enum.filter(results, fn r -> r.success end)
    failed_results = Enum.filter(results, fn r -> !r.success end)
    
    successful_count = length(successful_results)
    failed_count = length(failed_results)
    
    # Extract and sort response times
    response_times = Enum.map(successful_results, fn r -> r.response_time_ms * 1.0 end)
    sorted_times = Enum.sort(response_times)
    
    # Calculate metrics
    metrics = if length(response_times) > 0 do
      %{
        language: "elixir",
        total_requests: num_requests,
        successful_requests: successful_count,
        failed_requests: failed_count,
        total_time_seconds: Float.round(total_time, 2),
        requests_per_second: Float.round(num_requests / total_time, 2),
        response_times: %{
          min_ms: Float.round(Enum.min(response_times), 2),
          max_ms: Float.round(Enum.max(response_times), 2),
          average_ms: Float.round(Enum.sum(response_times) / length(response_times), 2),
          median_ms: Float.round(percentile(sorted_times, 0.50), 2),
          p95_ms: Float.round(percentile(sorted_times, 0.95), 2),
          p99_ms: Float.round(percentile(sorted_times, 0.99), 2)
        },
        timeseries: Enum.map(successful_results, fn r ->
          %{
            timestamp: Float.round(r.timestamp, 3),
            response_time_ms: Float.round(r.response_time_ms * 1.0, 2)
          }
        end)
      }
    else
      %{
        language: "elixir",
        total_requests: num_requests,
        successful_requests: 0,
        failed_requests: failed_count,
        total_time_seconds: Float.round(total_time, 2),
        requests_per_second: 0,
        response_times: %{},
        timeseries: []
      }
    end
    
    # Save results to JSON file
    output_file = "api_results.json"
    json_data = Jason.encode!(metrics, pretty: true)
    File.write!(output_file, json_data)
    
    IO.puts("\nResults saved to #{output_file}")
    
    metrics
  end

  @doc """
  Print formatted results to console.
  """
  def print_results(metrics) do
    IO.puts("\n#{"=" |> String.duplicate(60)}")
    IO.puts("Language: #{String.upcase(metrics.language)}")
    IO.puts("#{"=" |> String.duplicate(60)}")
    IO.puts("Total Requests: #{metrics.total_requests}")
    IO.puts("Successful: #{metrics.successful_requests}")
    IO.puts("Failed: #{metrics.failed_requests}")
    IO.puts("Total Time: #{metrics.total_time_seconds}s")
    IO.puts("Requests/sec: #{metrics.requests_per_second}")
    
    if map_size(metrics.response_times) > 0 do
      rt = metrics.response_times
      IO.puts("\nResponse Times (ms):")
      IO.puts("  Min: #{rt.min_ms}")
      IO.puts("  Max: #{rt.max_ms}")
      IO.puts("  Avg: #{rt.average_ms}")
      IO.puts("  Median: #{rt.median_ms}")
      IO.puts("  P95: #{rt.p95_ms}")
      IO.puts("  P99: #{rt.p99_ms}")
    end
    
    IO.puts("#{"=" |> String.duplicate(60)}\n")
  end
end

# Run if this is the main file
if System.argv() |> Enum.member?("--run") do
  metrics = ApiRequests.run_benchmark()
  ApiRequests.print_results(metrics)
end
