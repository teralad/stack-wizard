#!/usr/bin/env elixir

# Run all Elixir performance benchmarks

Mix.install([
  {:httpoison, "~> 2.0"},
  {:jason, "~> 1.4"}
])

# Load all benchmark modules
Code.require_file("lib/sorting.ex", __DIR__)
Code.require_file("lib/fibonacci.ex", __DIR__)
Code.require_file("lib/matrix.ex", __DIR__)
Code.require_file("lib/strings.ex", __DIR__)
Code.require_file("lib/api_requests.ex", __DIR__)

IO.puts("\n" <> String.duplicate("=", 60))
IO.puts("Elixir Performance Benchmarks")
IO.puts(String.duplicate("=", 60) <> "\n")

# Run all benchmarks
IO.puts("\n=== 1. Sorting (Quicksort) ===")
Sorting.run_benchmark()

IO.puts("\n=== 2. Fibonacci ===")
Fibonacci.run_benchmark()

IO.puts("\n=== 3. Matrix Multiplication ===")
Matrix.run_benchmark()

IO.puts("\n=== 4. String Manipulation ===")
Strings.run_benchmark()

IO.puts("\n=== 5. API Requests ===")
metrics = ApiRequests.run_benchmark()
ApiRequests.print_results(metrics)

IO.puts("\n" <> String.duplicate("=", 60))
IO.puts("All benchmarks completed!")
IO.puts(String.duplicate("=", 60) <> "\n")
