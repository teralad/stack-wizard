require 'benchmark'

# Quicksort algorithm implementation
def quicksort(arr)
  return arr if arr.length <= 1

  pivot = arr[arr.length / 2]
  left = arr.select { |x| x < pivot }
  middle = arr.select { |x| x == pivot }
  right = arr.select { |x| x > pivot }

  quicksort(left) + middle + quicksort(right)
end

# Verify if array is sorted
def sorted?(arr)
  (0...arr.length - 1).all? { |i| arr[i] <= arr[i + 1] }
end

# Run sorting benchmark with 100,000 random integers
def run_benchmark
  # Generate 100,000 random integers
  arr = Array.new(100_000) { rand(1_000_000) }

  # Measure sorting time
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  sorted_arr = quicksort(arr)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time = ((end_time - start_time) * 1000).round(2)

  # Verify sorting correctness
  correct = sorted?(sorted_arr)

  puts "Test: Sorting (Quicksort)"
  puts "Array size: #{arr.length}"
  puts "Execution time: #{execution_time} ms"
  puts "Correctly sorted: #{correct}"
end

if __FILE__ == $0
  run_benchmark
end
