require 'benchmark'

# Matrix multiplication implementation
def matrix_multiply(matrix_a, matrix_b)
  rows_a = matrix_a.length
  cols_a = matrix_a[0].length
  cols_b = matrix_b[0].length

  # Initialize result matrix with zeros
  result = Array.new(rows_a) { Array.new(cols_b, 0.0) }

  # Perform multiplication
  (0...rows_a).each do |i|
    (0...cols_b).each do |j|
      (0...cols_a).each do |k|
        result[i][j] += matrix_a[i][k] * matrix_b[k][j]
      end
    end
  end

  result
end

# Run matrix multiplication benchmark with 100x100 matrices
def run_benchmark
  size = 100

  # Generate two random 100x100 matrices
  matrix_a = Array.new(size) { Array.new(size) { rand } }
  matrix_b = Array.new(size) { Array.new(size) { rand } }

  # Measure multiplication time
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  result = matrix_multiply(matrix_a, matrix_b)
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  execution_time = ((end_time - start_time) * 1000).round(2)

  puts "Test: Matrix Multiplication"
  puts "Matrix size: #{size}x#{size}"
  puts "Execution time: #{execution_time} ms"
  puts "Result sample (0,0): #{result[0][0].round(6)}"
end

if __FILE__ == $0
  run_benchmark
end
