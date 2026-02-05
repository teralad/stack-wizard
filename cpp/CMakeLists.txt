cmake_minimum_required(VERSION 3.10)
project(StackWizardCppBenchmarks)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2")

# Find libcurl
find_package(CURL REQUIRED)

# Sorting benchmark
add_executable(sorting sorting.cpp)

# Fibonacci benchmark
add_executable(fibonacci fibonacci.cpp)

# Matrix benchmark
add_executable(matrix matrix.cpp)

# Strings benchmark
add_executable(strings strings.cpp)

# API requests benchmark
add_executable(api_requests api_requests.cpp)
target_link_libraries(api_requests CURL::libcurl)

# Main runner (informational only)
add_executable(main main.cpp)
