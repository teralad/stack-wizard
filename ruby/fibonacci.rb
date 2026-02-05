require 'benchmark'

# Recursive Fibonacci implementation
def fibonacci_recursive(n)
  return n if n <= 1
  fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
end

# Iterative Fibonacci implementation
def fibonacci_iterative(n)
  return n if n <= 1

  a, b = 0, 1
  (2..n).each do
    a, b = b, a + b
  end
  b
end

# Run Fibonacci benchmarks
def run_benchmark
  results = []

  # Recursive fibonacci(35)
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  result_recursive = fibonacci_recursive(35)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time_recursive = ((end_time - start_time) * 1000).round(2)

  puts "Test: Fibonacci Recursive (n=35)"
  puts "Result: #{result_recursive}"
  puts "Execution time: #{execution_time_recursive} ms"
  puts

  # Iterative fibonacci(40)
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  result_iterative = fibonacci_iterative(40)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time_iterative = ((end_time - start_time) * 1000).round(2)

  puts "Test: Fibonacci Iterative (n=40)"
  puts "Result: #{result_iterative}"
  puts "Execution time: #{execution_time_iterative} ms"
end

if __FILE__ == $0
  run_benchmark
end
