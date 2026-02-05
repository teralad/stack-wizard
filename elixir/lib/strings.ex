defmodule Strings do
  @moduledoc """
  String manipulation operations for performance benchmarking.
  Tests string reversal, concatenation, and pattern matching.
  """

  @doc """
  Reverse a string.
  """
  def reverse_string(str) do
    String.reverse(str)
  end

  @doc """
  Concatenate a string n times.
  """
  def concatenate_string(base_str, n) do
    Enum.reduce(1..n, "", fn _, acc -> acc <> base_str end)
  end

  @doc """
  Find 5-letter words in text using pattern matching.
  """
  def find_five_letter_words(text) do
    Regex.scan(~r/\b[a-zA-Z]{5}\b/, text)
    |> Enum.map(fn [word] -> word end)
  end

  @doc """
  Run string manipulation benchmarks.
  """
  def run_benchmark do
    IO.puts("\n=== String Manipulation Benchmarks ===")
    
    # 1. String Reversal (1 million characters)
    long_string = String.duplicate("abcdefghij", 100_000)
    {time_reverse_micros, _reversed} = :timer.tc(fn -> reverse_string(long_string) end)
    time_reverse = time_reverse_micros / 1000
    IO.puts("String Reversal (1M chars): #{:erlang.float_to_binary(time_reverse, decimals: 2)} ms")
    
    # 2. String Concatenation (10,000 iterations)
    {time_concat_micros, _concatenated} = :timer.tc(fn -> concatenate_string("test", 10_000) end)
    time_concat = time_concat_micros / 1000
    IO.puts("String Concatenation (10K iterations): #{:erlang.float_to_binary(time_concat, decimals: 2)} ms")
    
    # 3. Pattern Search (find 5-letter words)
    # Create a large text with many words
    sample_text = "hello world quick brown foxes jumps over fence under table chair grape mango apple berry water glass plate metal stone brick house happy smile dream peace light stars night"
    large_text = String.duplicate(sample_text <> " ", 1000)
    {time_search_micros, matches} = :timer.tc(fn -> find_five_letter_words(large_text) end)
    time_search = time_search_micros / 1000
    IO.puts("Pattern Search: #{:erlang.float_to_binary(time_search, decimals: 2)} ms (#{length(matches)} matches)")
    
    %{
      reversal: %{
        length: String.length(long_string),
        execution_time_ms: time_reverse
      },
      concatenation: %{
        iterations: 10_000,
        execution_time_ms: time_concat
      },
      pattern_search: %{
        matches_found: length(matches),
        execution_time_ms: time_search
      }
    }
  end
end

# Run if this is the main file
if System.argv() |> Enum.member?("--run"), do: Strings.run_benchmark()
