defmodule Fibonacci do
  @moduledoc """
  Fibonacci calculation implementations for performance benchmarking.
  Tests recursive (n=35) and iterative (n=40) approaches.
  """

  @doc """
  Recursive Fibonacci implementation.
  """
  def fib_recursive(0), do: 0
  def fib_recursive(1), do: 1
  def fib_recursive(n) when n > 1 do
    fib_recursive(n - 1) + fib_recursive(n - 2)
  end

  @doc """
  Iterative Fibonacci implementation.
  """
  def fib_iterative(n) when n >= 0 do
    fib_iterative_helper(n, 0, 1)
  end

  defp fib_iterative_helper(0, a, _b), do: a
  defp fib_iterative_helper(n, a, b) when n > 0 do
    fib_iterative_helper(n - 1, b, a + b)
  end

  @doc """
  Run Fibonacci benchmarks.
  """
  def run_benchmark do
    # Recursive approach with n=35
    {time_recursive_micros, result_recursive} = :timer.tc(fn -> fib_recursive(35) end)
    time_recursive = time_recursive_micros / 1000  # Convert to milliseconds
    
    # Iterative approach with n=40
    {time_iterative_micros, result_iterative} = :timer.tc(fn -> fib_iterative(40) end)
    time_iterative = time_iterative_micros / 1000  # Convert to milliseconds
    
    IO.puts("\n=== Fibonacci Benchmark ===")
    IO.puts("Recursive (n=35): #{:erlang.float_to_binary(time_recursive, decimals: 2)} ms, result = #{result_recursive}")
    IO.puts("Iterative (n=40): #{:erlang.float_to_binary(time_iterative, decimals: 2)} ms, result = #{result_iterative}")
    
    %{
      recursive: %{
        n: 35,
        result: result_recursive,
        execution_time_ms: time_recursive
      },
      iterative: %{
        n: 40,
        result: result_iterative,
        execution_time_ms: time_iterative
      }
    }
  end
end

# Run if this is the main file
if System.argv() |> Enum.member?("--run"), do: Fibonacci.run_benchmark()
