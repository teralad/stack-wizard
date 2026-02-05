#!/usr/bin/env ruby

puts "=" * 60
puts "Ruby Performance Benchmarks"
puts "=" * 60
puts

# Sorting
puts "Running Sorting Benchmark..."
system("ruby sorting.rb")
puts

# Fibonacci
puts "Running Fibonacci Benchmarks..."
system("ruby fibonacci.rb")
puts

# Matrix
puts "Running Matrix Multiplication Benchmark..."
system("ruby matrix.rb")
puts

# Strings
puts "Running String Manipulation Benchmarks..."
system("ruby strings.rb")
puts

# API Requests
puts "Running API Request Benchmark..."
system("ruby api_requests.rb")
puts

puts "=" * 60
puts "All benchmarks completed!"
puts "=" * 60


