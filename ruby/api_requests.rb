# Ruby API Request Performance Test
# Uses Net::HTTP with threads for concurrent HTTP requests.
# Collects comprehensive metrics including response times, throughput, and percentiles.

require 'net/http'
require 'uri'
require 'thread'
require 'json'

# Make a single HTTP request with timing
def make_request(url, request_id, start_time)
  request_start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  uri = URI.parse(url)
  
  begin
    response = Net::HTTP.get_response(uri)
    request_end = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    
    {
      id: request_id,
      success: response.code.to_i == 200,
      response_time_ms: ((request_end - request_start) * 1000).round(2),
      timestamp: (request_end - start_time).round(3)
    }
  rescue => e
    request_end = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    {
      id: request_id,
      success: false,
      response_time_ms: ((request_end - request_start) * 1000).round(2),
      timestamp: (request_end - start_time).round(3),
      error: e.message
    }
  end
end

# Calculate percentile from sorted array
def percentile(sorted_data, p)
  return 0.0 if sorted_data.empty?
  index = [(sorted_data.size * p).ceil - 1, 0].max
  index = [index, sorted_data.size - 1].min
  sorted_data[index]
end

# Run API request benchmark with 1,000 concurrent requests
def run_benchmark
  url = "https://jsonplaceholder.typicode.com/posts/1"
  num_requests = 1000

  puts "Starting benchmark: #{num_requests} requests to #{url}"

  # Measure total time for concurrent requests
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)

  threads = []
  results = []
  mutex = Mutex.new

  num_requests.times do |i|
    threads << Thread.new do
      result = make_request(url, i, start_time)
      mutex.synchronize do
        results << result
      end
    end
  end

  threads.each(&:join)

  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  total_time = (end_time - start_time).round(2)

  # Analyze results
  successful_results = results.select { |r| r[:success] }
  failed_results = results.reject { |r| r[:success] }

  successful_count = successful_results.size
  failed_count = failed_results.size

  # Build metrics
  metrics = if successful_results.any?
    response_times = successful_results.map { |r| r[:response_time_ms] }.sort

    sum = response_times.sum
    min_val = response_times.first
    max_val = response_times.last
    avg_val = (sum / response_times.size).round(2)

    {
      language: 'ruby',
      total_requests: num_requests,
      successful_requests: successful_count,
      failed_requests: failed_count,
      total_time_seconds: total_time,
      requests_per_second: (num_requests / total_time).round(2),
      response_times: {
        min_ms: min_val.round(2),
        max_ms: max_val.round(2),
        average_ms: avg_val,
        median_ms: percentile(response_times, 0.5).round(2),
        p95_ms: percentile(response_times, 0.95).round(2),
        p99_ms: percentile(response_times, 0.99).round(2)
      },
      timeseries: successful_results.map do |r|
        {
          timestamp: r[:timestamp],
          response_time_ms: r[:response_time_ms]
        }
      end
    }
  else
    {
      language: 'ruby',
      total_requests: num_requests,
      successful_requests: 0,
      failed_requests: failed_count,
      total_time_seconds: total_time,
      requests_per_second: 0,
      response_times: {},
      timeseries: []
    }
  end

  # Save results to JSON file
  File.write('api_results.json', JSON.pretty_generate(metrics))
  puts "\nResults saved to api_results.json"

  # Print results
  print_results(metrics)
end

def print_results(metrics)
  puts "\n#{'=' * 60}"
  puts "Language: #{metrics[:language].upcase}"
  puts '=' * 60
  puts "Total Requests: #{metrics[:total_requests]}"
  puts "Successful: #{metrics[:successful_requests]}"
  puts "Failed: #{metrics[:failed_requests]}"
  puts "Total Time: #{metrics[:total_time_seconds]}s"
  puts "Requests/sec: #{metrics[:requests_per_second]}"

  if metrics[:response_times].any?
    puts "\nResponse Times (ms):"
    puts "  Min: #{metrics[:response_times][:min_ms]}"
    puts "  Max: #{metrics[:response_times][:max_ms]}"
    puts "  Avg: #{metrics[:response_times][:average_ms]}"
    puts "  Median: #{metrics[:response_times][:median_ms]}"
    puts "  P95: #{metrics[:response_times][:p95_ms]}"
    puts "  P99: #{metrics[:response_times][:p99_ms]}"
  end
  puts "#{'=' * 60}\n"
end

if __FILE__ == $0
  run_benchmark
end
