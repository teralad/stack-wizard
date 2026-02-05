# API Performance Visualizations

This directory contains scripts and outputs for visualizing API performance comparison across all 7 languages.

## Overview

The visualization system reads JSON results from API performance tests and generates comprehensive comparison charts including:

1. **Throughput Comparison** - Bar chart showing requests per second
2. **Response Time Distribution** - Box plot comparing response time metrics
3. **Request Completion Timeline** - Line graph showing cumulative request completion
4. **Response Time Heatmap** - Heatmap of response time metrics across languages
5. **Success Rate Comparison** - Bar chart showing request success rates
6. **Interactive Dashboard** - HTML dashboard with interactive graphs

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Required packages:
- matplotlib >= 3.5.0
- plotly >= 5.0.0
- pandas >= 1.3.0
- numpy >= 1.21.0

## Usage

### 1. Run API Tests First

Before generating visualizations, you need to run the API tests for all languages to generate the `api_results.json` files:

```bash
# Python
cd ../python
pip install -r requirements.txt
python api_requests.py

# JavaScript
cd ../javascript
node api_requests.js

# Go
cd ../go
go run api_requests.go

# Rust (use --release for accurate performance)
cd ../rust
cargo run --release --bin api_requests

# Java
cd ../java
mvn compile
mvn exec:java -Dexec.mainClass="ApiRequests"

# C++
cd ../cpp
mkdir -p build && cd build
cmake ..
make
./api_requests

# Ruby
cd ../ruby
ruby api_requests.rb
```

### 2. Generate Visualizations

Once all API tests have been run and JSON results are available:

```bash
cd visualizations
python generate_graphs.py
```

This will:
- Load all `api_results.json` files from language directories
- Generate PNG charts in the `graphs/` directory
- Create an interactive HTML dashboard

### 3. View Results

**Static Images:**
- `graphs/throughput_comparison.png`
- `graphs/response_time_distribution.png`
- `graphs/cumulative_requests_timeline.png`
- `graphs/response_time_heatmap.png`
- `graphs/success_rate_comparison.png`

**Interactive Dashboard:**
Open `graphs/api_performance_dashboard.html` in your web browser for interactive visualizations with zoom, pan, and hover tooltips.

## Output Structure

```
visualizations/
├── generate_graphs.py      # Main visualization script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── graphs/                # Output directory
    ├── throughput_comparison.png
    ├── response_time_distribution.png
    ├── cumulative_requests_timeline.png
    ├── response_time_heatmap.png
    ├── success_rate_comparison.png
    └── api_performance_dashboard.html
```

## Metrics Collected

Each language test collects the following metrics:

- **Total Requests**: Number of requests attempted (10,000)
- **Successful/Failed Requests**: Count of successful and failed requests
- **Total Time**: Total execution time in seconds
- **Requests per Second**: Throughput metric
- **Response Times**:
  - Minimum response time
  - Maximum response time
  - Average response time
  - Median response time
  - 95th percentile (P95)
  - 99th percentile (P99)
- **Time Series**: Timestamp and response time for each request

## Troubleshooting

**Issue**: Script reports "No results found"
- **Solution**: Run the API tests for all languages first

**Issue**: Missing results for some languages
- **Solution**: Check that each language's `api_results.json` file exists in its directory

**Issue**: Import errors
- **Solution**: Install required packages: `pip install -r requirements.txt`

**Issue**: Graph generation fails
- **Solution**: Ensure matplotlib backend is properly configured. On headless systems, the script uses 'Agg' backend automatically.

## Customization

To customize the visualizations:

1. **Colors**: Edit the `COLORS` dictionary in `generate_graphs.py`
2. **Graph Size**: Modify `figsize` parameters in individual chart functions
3. **DPI**: Change the `dpi` parameter in `savefig()` calls for higher/lower resolution
4. **Additional Metrics**: Add new visualization functions following the existing pattern

## Notes

- The visualization script automatically handles missing language results
- All graphs use consistent color schemes for easy comparison
- PNG outputs are high-resolution (300 DPI) suitable for documentation
- The interactive dashboard allows zooming and detailed inspection of data
