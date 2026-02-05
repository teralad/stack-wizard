defmodule ApiRequestsTest do
  use ExUnit.Case
  doctest ApiRequests

  setup do
    bypass = Bypass.open()
    {:ok, bypass: bypass}
  end

  describe "make_request/3" do
    test "successfully handles 200 OK response", %{bypass: bypass} do
      Bypass.expect_once(bypass, "GET", "/posts/1", fn conn ->
        Plug.Conn.resp(conn, 200, ~s({"id": 1, "title": "test"}))
      end)

      url = "http://localhost:#{bypass.port}/posts/1"
      start_time = :os.system_time(:millisecond)
      
      result = ApiRequests.make_request(url, 1, start_time)
      
      assert result.success == true
      assert result.id == 1
      assert result.response_time_ms > 0
      assert result.timestamp >= 0
    end

    test "handles non-200 status codes", %{bypass: bypass} do
      Bypass.expect_once(bypass, "GET", "/posts/1", fn conn ->
        Plug.Conn.resp(conn, 404, "Not Found")
      end)

      url = "http://localhost:#{bypass.port}/posts/1"
      start_time = :os.system_time(:millisecond)
      
      result = ApiRequests.make_request(url, 1, start_time)
      
      assert result.success == false
      assert result.id == 1
      assert String.contains?(Map.get(result, :error, ""), "404")
    end

    test "handles network errors", %{bypass: bypass} do
      Bypass.down(bypass)
      
      url = "http://localhost:#{bypass.port}/posts/1"
      start_time = :os.system_time(:millisecond)
      
      result = ApiRequests.make_request(url, 1, start_time)
      
      assert result.success == false
      assert result.id == 1
      assert Map.has_key?(result, :error)
    end
  end

  describe "percentile/2" do
    test "calculates 50th percentile (median)" do
      data = [1.0, 2.0, 3.0, 4.0, 5.0]
      assert ApiRequests.percentile(data, 0.50) == 3.0
    end

    test "calculates 95th percentile" do
      data = Enum.map(1..100, fn x -> x * 1.0 end)
      result = ApiRequests.percentile(data, 0.95)
      assert result >= 94.0 and result <= 96.0
    end

    test "calculates 99th percentile" do
      data = Enum.map(1..100, fn x -> x * 1.0 end)
      result = ApiRequests.percentile(data, 0.99)
      assert result >= 98.0 and result <= 100.0
    end

    test "handles edge case with single element" do
      data = [42.0]
      assert ApiRequests.percentile(data, 0.50) == 42.0
      assert ApiRequests.percentile(data, 0.95) == 42.0
      assert ApiRequests.percentile(data, 0.99) == 42.0
    end
  end

  describe "API metrics validation" do
    test "validates metrics structure with mock server", %{bypass: bypass} do
      # Mock 10 successful requests
      Bypass.stub(bypass, "GET", "/posts/1", fn conn ->
        Plug.Conn.resp(conn, 200, ~s({"id": 1, "title": "test"}))
      end)

      # Simulate a small benchmark
      url = "http://localhost:#{bypass.port}/posts/1"
      num_requests = 10
      start_time = :os.system_time(:millisecond)
      
      results = Enum.map(0..(num_requests - 1), fn i ->
        ApiRequests.make_request(url, i, start_time)
      end)
      
      successful_results = Enum.filter(results, fn r -> r.success end)
      
      # Verify all requests succeeded
      assert length(successful_results) == num_requests
      
      # Verify response times are collected
      response_times = Enum.map(successful_results, fn r -> r.response_time_ms end)
      assert length(response_times) == num_requests
      
      # Verify all response times are positive
      Enum.each(response_times, fn time ->
        assert time > 0
      end)
    end
  end
end
