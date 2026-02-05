#!/bin/bash
# Run all performance benchmarks across all languages

set -e

echo "========================================"
echo "Running All Performance Benchmarks"
echo "========================================"
echo ""

# Python
echo "=== Python Benchmarks ==="
cd python
pip3 install -q requests 2>/dev/null || true
python3 run_all.py
cd ..
echo ""

# JavaScript
echo "=== JavaScript Benchmarks ==="
cd javascript
node run_all.js
cd ..
echo ""

# Go
echo "=== Go Benchmarks ==="
cd go
go run .
cd ..
echo ""

# Rust (release mode for performance)
echo "=== Rust Benchmarks ==="
cd rust
cargo run --release --quiet 2>/dev/null || cargo run --release
cd ..
echo ""

# Java
echo "=== Java Benchmarks ==="
cd java
javac src/*.java 2>/dev/null || true
java -cp src Main
cd ..
echo ""

# C++
echo "=== C++ Benchmarks ==="
cd cpp
echo "Compiling C++ benchmarks..."
g++ -std=c++17 -O2 sorting.cpp -o sorting
g++ -std=c++17 -O2 fibonacci.cpp -o fibonacci
g++ -std=c++17 -O2 matrix.cpp -o matrix
g++ -std=c++17 -O2 strings.cpp -o strings
g++ -std=c++17 -O2 api_requests.cpp -o api_requests -lcurl 2>/dev/null || echo "Skipping api_requests (libcurl not found)"

echo "Running C++ benchmarks..."
./sorting
echo ""
./fibonacci
echo ""
./matrix
echo ""
./strings
echo ""
if [ -f ./api_requests ]; then
  ./api_requests
fi

# Clean up
rm -f sorting fibonacci matrix strings api_requests
cd ..
echo ""

# Ruby
echo "=== Ruby Benchmarks ==="
cd ruby
ruby run_all.rb
cd ..
echo ""

echo "========================================"
echo "All Benchmarks Completed!"
echo "========================================"
