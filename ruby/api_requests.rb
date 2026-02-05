require 'net/http'
require 'uri'
require 'benchmark'
require 'thread'

# Make a single HTTP request
def make_request(url, request_id)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  {
    id: request_id,
    status: response.code.to_i,
    success: response.code.to_i == 200
  }
rescue => e
  {
    id: request_id,
    status: 0,
    success: false,
    error: e.message
  }
end

# Run API request benchmark with 50 concurrent requests
def run_benchmark
  url = "https://jsonplaceholder.typicode.com/posts/1"
  num_requests = 50

  # Measure total time for concurrent requests
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)

  threads = []
  results = []
  mutex = Mutex.new

  num_requests.times do |i|
    threads << Thread.new do
      result = make_request(url, i)
      mutex.synchronize do
        results << result
      end
    end
  end

  threads.each(&:join)

  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time = ((end_time - start_time) * 1000).round(2)

  # Count successful requests
  successful = results.count { |r| r[:success] }

  puts "Test: API Requests (50 concurrent)"
  puts "Total requests: #{num_requests}"
  puts "Successful requests: #{successful}"
  puts "Execution time: #{execution_time} ms"
end

if __FILE__ == $0
  run_benchmark
end
