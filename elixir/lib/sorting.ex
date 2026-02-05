defmodule Sorting do
  @moduledoc """
  Quicksort implementation for performance benchmarking.
  Tests with 100,000 random integers.
  """

  @doc """
  Quicksort algorithm implementation.
  """
  def quicksort([]), do: []
  def quicksort([pivot | rest]) do
    {left, right} = Enum.split_with(rest, fn x -> x < pivot end)
    quicksort(left) ++ [pivot] ++ quicksort(right)
  end

  @doc """
  Run sorting benchmark with 100,000 random integers.
  """
  def run_benchmark do
    # Generate 100,000 random integers
    arr = Enum.map(1..100_000, fn _ -> :rand.uniform(1_000_000) end)
    
    # Measure sorting time
    {time_micros, sorted_arr} = :timer.tc(fn -> quicksort(arr) end)
    execution_time = time_micros / 1000  # Convert to milliseconds
    
    # Verify sorting correctness
    is_sorted = Enum.chunk_every(sorted_arr, 2, 1, :discard)
                |> Enum.all?(fn [a, b] -> a <= b end)
    
    result = %{
      test_name: "Sorting (Quicksort)",
      execution_time_ms: execution_time,
      size: length(arr),
      correct: is_sorted
    }
    
    IO.puts("Test: #{result.test_name}")
    IO.puts("Array size: #{result.size}")
    IO.puts("Execution time: #{:erlang.float_to_binary(result.execution_time_ms, decimals: 2)} ms")
    IO.puts("Correctly sorted: #{result.correct}")
    
    result
  end
end

# Run if this is the main file
if System.argv() |> Enum.member?("--run"), do: Sorting.run_benchmark()
