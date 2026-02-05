defmodule Matrix do
  @moduledoc """
  Matrix multiplication implementation for performance benchmarking.
  Tests with two 100x100 matrices.
  """

  @doc """
  Generate a random matrix of given dimensions.
  """
  def generate_random_matrix(rows, cols) do
    Enum.map(1..rows, fn _ ->
      Enum.map(1..cols, fn _ -> :rand.uniform() * 100 end)
    end)
  end

  @doc """
  Multiply two matrices using standard algorithm.
  """
  def multiply(matrix_a, matrix_b) do
    rows_a = length(matrix_a)
    cols_a = length(hd(matrix_a))
    cols_b = length(hd(matrix_b))
    
    # Transpose matrix B for easier column access
    matrix_b_t = transpose(matrix_b)
    
    Enum.map(0..(rows_a - 1), fn i ->
      row_a = Enum.at(matrix_a, i)
      Enum.map(0..(cols_b - 1), fn j ->
        col_b = Enum.at(matrix_b_t, j)
        dot_product(row_a, col_b)
      end)
    end)
  end

  defp transpose(matrix) do
    matrix
    |> Enum.zip()
    |> Enum.map(&Tuple.to_list/1)
  end

  defp dot_product(vec_a, vec_b) do
    Enum.zip(vec_a, vec_b)
    |> Enum.reduce(0, fn {a, b}, acc -> acc + a * b end)
  end

  @doc """
  Run matrix multiplication benchmark with 100x100 matrices.
  """
  def run_benchmark do
    size = 100
    
    # Generate two random matrices
    matrix_a = generate_random_matrix(size, size)
    matrix_b = generate_random_matrix(size, size)
    
    # Measure multiplication time
    {time_micros, result_matrix} = :timer.tc(fn -> multiply(matrix_a, matrix_b) end)
    execution_time = time_micros / 1000  # Convert to milliseconds
    
    # Verify result dimensions
    result_rows = length(result_matrix)
    result_cols = length(hd(result_matrix))
    
    IO.puts("\n=== Matrix Multiplication Benchmark ===")
    IO.puts("Matrix size: #{size}x#{size}")
    IO.puts("Execution time: #{:erlang.float_to_binary(execution_time, decimals: 2)} ms")
    IO.puts("Result dimensions: #{result_rows}x#{result_cols}")
    
    %{
      test_name: "Matrix Multiplication",
      matrix_size: size,
      execution_time_ms: execution_time,
      result_dimensions: {result_rows, result_cols}
    }
  end
end

# Run if this is the main file
if System.argv() |> Enum.member?("--run"), do: Matrix.run_benchmark()
