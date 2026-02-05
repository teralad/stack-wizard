#!/bin/bash
# Test runner for all language implementations
# This script runs unit tests for Elixir, C#, and Scala API implementations

set -e  # Exit on error

echo "=================================================="
echo "Running API Implementation Tests"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall success
ALL_TESTS_PASSED=true

echo ""
echo "==== C# Tests ===="
if command -v dotnet &> /dev/null; then
    cd csharp/Tests
    if dotnet test --verbosity minimal; then
        echo -e "${GREEN}✓ C# tests passed${NC}"
    else
        echo -e "${RED}✗ C# tests failed${NC}"
        ALL_TESTS_PASSED=false
    fi
    cd ../..
else
    echo -e "${YELLOW}⊘ .NET SDK not installed, skipping C# tests${NC}"
fi

echo ""
echo "==== Elixir Tests ===="
if command -v mix &> /dev/null; then
    cd elixir
    echo "Installing Elixir dependencies..."
    if ! mix deps.get; then
        echo -e "${RED}✗ Failed to install Elixir dependencies${NC}"
        ALL_TESTS_PASSED=false
    elif mix test; then
        echo -e "${GREEN}✓ Elixir tests passed${NC}"
    else
        echo -e "${RED}✗ Elixir tests failed${NC}"
        ALL_TESTS_PASSED=false
    fi
    cd ..
else
    echo -e "${YELLOW}⊘ Elixir not installed, skipping Elixir tests${NC}"
fi

echo ""
echo "==== Scala Tests ===="
if command -v sbt &> /dev/null; then
    cd scala
    if sbt test; then
        echo -e "${GREEN}✓ Scala tests passed${NC}"
    else
        echo -e "${RED}✗ Scala tests failed${NC}"
        ALL_TESTS_PASSED=false
    fi
    cd ..
else
    echo -e "${YELLOW}⊘ sbt not installed, skipping Scala tests${NC}"
fi

echo ""
echo "=================================================="
if [ "$ALL_TESTS_PASSED" = true ]; then
    echo -e "${GREEN}All available tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
