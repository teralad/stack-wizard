require 'benchmark'

# Reverse a string
def reverse_string(s)
  s.reverse
end

# Concatenate strings multiple times
def concatenate_strings(iterations)
  result = ""
  iterations.times do |i|
    result += i.to_s
  end
  result
end

# Search for pattern in text using regex
def pattern_search(text, pattern)
  text.scan(Regexp.new(pattern)).length
end

# Run string manipulation benchmarks
def run_benchmark
  # String reversal on 1 million character string
  large_string = "a" * 1_000_000
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  reversed = reverse_string(large_string)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time_reverse = ((end_time - start_time) * 1000).round(2)

  puts "Test: String Reversal (1M chars)"
  puts "Execution time: #{execution_time_reverse} ms"
  puts "String length: #{large_string.length}"
  puts

  # String concatenation (10,000 iterations)
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  concatenated = concatenate_strings(10_000)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time_concat = ((end_time - start_time) * 1000).round(2)

  puts "Test: String Concatenation (10K iterations)"
  puts "Execution time: #{execution_time_concat} ms"
  puts "Result length: #{concatenated.length}"
  puts

  # Pattern searching
  text = "Lorem ipsum dolor sit amet " * 10_000
  pattern = '\b\w{5}\b' # Find all 5-letter words
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  matches = pattern_search(text, pattern)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time_search = ((end_time - start_time) * 1000).round(2)

  puts "Test: Pattern Search"
  puts "Execution time: #{execution_time_search} ms"
  puts "Matches found: #{matches}"
end

if __FILE__ == $0
  run_benchmark
end
