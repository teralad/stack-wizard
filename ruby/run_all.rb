#!/usr/bin/env ruby

require_relative 'sorting'
require_relative 'fibonacci'
require_relative 'matrix'
require_relative 'strings'
require_relative 'api_requests'

puts "=" * 60
puts "Ruby Performance Benchmarks"
puts "=" * 60
puts

# Sorting
puts "Running Sorting Benchmark..."
load 'sorting.rb'
puts

# Fibonacci
puts "Running Fibonacci Benchmarks..."
load 'fibonacci.rb'
puts

# Matrix
puts "Running Matrix Multiplication Benchmark..."
load 'matrix.rb'
puts

# Strings
puts "Running String Manipulation Benchmarks..."
load 'strings.rb'
puts

# API Requests
puts "Running API Request Benchmark..."
load 'api_requests.rb'
puts

puts "=" * 60
puts "All benchmarks completed!"
puts "=" * 60
