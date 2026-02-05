#!/usr/bin/env python3
"""
API Performance Visualization Generator

This script reads API performance test results from all language implementations
and generates comprehensive comparison visualizations including:
- Throughput comparison (bar chart)
- Response time distribution (box plot)
- Cumulative requests timeline (line graph)
- Response time heatmap
- Success rate comparison (bar chart)
- Interactive dashboard (HTML)
"""

import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Language directories to search for results
LANGUAGES = ['python', 'javascript', 'go', 'rust', 'java', 'cpp', 'ruby']

# Color palette for consistent visualization
COLORS = {
    'python': '#3776ab',
    'javascript': '#f7df1e',
    'go': '#00add8',
    'rust': '#ce422b',
    'java': '#007396',
    'cpp': '#00599c',
    'ruby': '#cc342d'
}

def load_results():
    """Load API results from all language directories."""
    results = {}
    repo_root = Path(__file__).parent.parent
    
    for lang in LANGUAGES:
        results_file = repo_root / lang / 'api_results.json'
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                    results[lang] = data
                    print(f"✓ Loaded results for {lang}")
            except Exception as e:
                print(f"✗ Error loading {lang} results: {e}")
        else:
            print(f"✗ Results not found for {lang}: {results_file}")
    
    if not results:
        print("\n❌ No results found! Please run the API tests first.")
        sys.exit(1)
    
    return results

def create_throughput_comparison(results, output_dir):
    """Create bar chart comparing throughput (requests per second)."""
    languages = []
    throughputs = []
    colors_list = []
    
    for lang, data in sorted(results.items(), key=lambda x: x[1]['requests_per_second'], reverse=True):
        languages.append(lang.upper())
        throughputs.append(data['requests_per_second'])
        colors_list.append(COLORS.get(lang, '#888888'))
    
    # Matplotlib version
    plt.figure(figsize=(12, 6))
    bars = plt.bar(languages, throughputs, color=colors_list, edgecolor='black', linewidth=1.2)
    plt.xlabel('Language', fontsize=14, fontweight='bold')
    plt.ylabel('Requests per Second', fontsize=14, fontweight='bold')
    plt.title('API Performance: Throughput Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'throughput_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated throughput_comparison.png")

def create_response_time_distribution(results, output_dir):
    """Create box plot comparing response time distributions."""
    data_for_plot = []
    labels = []
    colors_list = []
    
    for lang, data in sorted(results.items()):
        if data.get('response_times') and data['successful_requests'] > 0:
            rt = data['response_times']
            # Create box plot data points
            data_for_plot.append([
                rt['min_ms'],
                rt['median_ms'] - (rt['median_ms'] - rt['min_ms']) / 2,  # Q1 approximation
                rt['median_ms'],
                rt['p95_ms'],
                rt['p99_ms'],
                rt['max_ms']
            ])
            labels.append(lang.upper())
            colors_list.append(COLORS.get(lang, '#888888'))
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create box plot
    positions = range(len(labels))
    bp = ax.boxplot(data_for_plot, positions=positions, labels=labels,
                     patch_artist=True, widths=0.6,
                     showfliers=True, notch=True)
    
    # Color the boxes
    for patch, color in zip(bp['boxes'], colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_xlabel('Language', fontsize=14, fontweight='bold')
    ax.set_ylabel('Response Time (ms)', fontsize=14, fontweight='bold')
    ax.set_title('API Performance: Response Time Distribution', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'response_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated response_time_distribution.png")

def create_cumulative_requests_timeline(results, output_dir):
    """Create line graph showing cumulative requests completed over time."""
    plt.figure(figsize=(14, 8))
    
    for lang, data in sorted(results.items()):
        if data.get('timeseries') and len(data['timeseries']) > 0:
            timeseries = sorted(data['timeseries'], key=lambda x: x['timestamp'])
            timestamps = [point['timestamp'] for point in timeseries]
            cumulative = list(range(1, len(timestamps) + 1))
            
            plt.plot(timestamps, cumulative, label=lang.upper(), 
                    color=COLORS.get(lang, '#888888'), linewidth=2, alpha=0.8)
    
    plt.xlabel('Time (seconds)', fontsize=14, fontweight='bold')
    plt.ylabel('Cumulative Requests Completed', fontsize=14, fontweight='bold')
    plt.title('API Performance: Request Completion Timeline', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='lower right', fontsize=11, framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_dir / 'cumulative_requests_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated cumulative_requests_timeline.png")

def create_response_time_heatmap(results, output_dir):
    """Create heatmap comparing response time metrics across languages."""
    languages = []
    metrics_data = {
        'Min': [],
        'Avg': [],
        'Median': [],
        'P95': [],
        'P99': [],
        'Max': []
    }
    
    for lang, data in sorted(results.items()):
        if data.get('response_times') and data['successful_requests'] > 0:
            rt = data['response_times']
            languages.append(lang.upper())
            metrics_data['Min'].append(rt['min_ms'])
            metrics_data['Avg'].append(rt['average_ms'])
            metrics_data['Median'].append(rt['median_ms'])
            metrics_data['P95'].append(rt['p95_ms'])
            metrics_data['P99'].append(rt['p99_ms'])
            metrics_data['Max'].append(rt['max_ms'])
    
    # Create matrix for heatmap
    matrix = np.array([metrics_data[key] for key in metrics_data.keys()])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(languages)))
    ax.set_yticks(np.arange(len(metrics_data)))
    ax.set_xticklabels(languages)
    ax.set_yticklabels(metrics_data.keys())
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    for i in range(len(metrics_data)):
        for j in range(len(languages)):
            text = ax.text(j, i, f'{matrix[i, j]:.1f}',
                          ha="center", va="center", color="black", fontweight='bold', fontsize=10)
    
    ax.set_title('API Performance: Response Time Heatmap (ms)', fontsize=16, fontweight='bold', pad=20)
    plt.colorbar(im, ax=ax, label='Response Time (ms)')
    plt.tight_layout()
    plt.savefig(output_dir / 'response_time_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated response_time_heatmap.png")

def create_success_rate_comparison(results, output_dir):
    """Create bar chart comparing success rates."""
    languages = []
    success_rates = []
    colors_list = []
    
    for lang, data in sorted(results.items()):
        languages.append(lang.upper())
        rate = (data['successful_requests'] / data['total_requests']) * 100
        success_rates.append(rate)
        colors_list.append(COLORS.get(lang, '#888888'))
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(languages, success_rates, color=colors_list, edgecolor='black', linewidth=1.2)
    plt.xlabel('Language', fontsize=14, fontweight='bold')
    plt.ylabel('Success Rate (%)', fontsize=14, fontweight='bold')
    plt.title('API Performance: Success Rate Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.ylim([0, 105])
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'success_rate_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated success_rate_comparison.png")

def create_interactive_dashboard(results, output_dir):
    """Create interactive HTML dashboard with plotly."""
    
    # Prepare data
    languages = sorted(results.keys())
    throughputs = [results[lang]['requests_per_second'] for lang in languages]
    success_rates = [(results[lang]['successful_requests'] / results[lang]['total_requests']) * 100 
                     for lang in languages]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Throughput Comparison', 'Success Rate', 
                       'Response Time Distribution', 'Request Completion Timeline'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}],
               [{'type': 'box'}, {'type': 'scatter'}]]
    )
    
    # Throughput comparison
    fig.add_trace(
        go.Bar(x=[l.upper() for l in languages], y=throughputs, 
               name='Requests/sec',
               marker_color=[COLORS.get(l, '#888888') for l in languages],
               text=[f'{t:.0f}' for t in throughputs],
               textposition='outside'),
        row=1, col=1
    )
    
    # Success rate
    fig.add_trace(
        go.Bar(x=[l.upper() for l in languages], y=success_rates, 
               name='Success %',
               marker_color=[COLORS.get(l, '#888888') for l in languages],
               text=[f'{s:.1f}%' for s in success_rates],
               textposition='outside'),
        row=1, col=2
    )
    
    # Response time distribution (box plot)
    for lang in languages:
        data = results[lang]
        if data.get('response_times') and data['successful_requests'] > 0:
            rt = data['response_times']
            fig.add_trace(
                go.Box(y=[rt['min_ms'], rt['median_ms'], rt['p95_ms'], rt['p99_ms'], rt['max_ms']],
                       name=lang.upper(),
                       marker_color=COLORS.get(lang, '#888888')),
                row=2, col=1
            )
    
    # Cumulative timeline
    for lang in languages:
        data = results[lang]
        if data.get('timeseries') and len(data['timeseries']) > 0:
            timeseries = sorted(data['timeseries'], key=lambda x: x['timestamp'])
            timestamps = [point['timestamp'] for point in timeseries]
            cumulative = list(range(1, len(timestamps) + 1))
            
            fig.add_trace(
                go.Scatter(x=timestamps, y=cumulative, name=lang.upper(),
                          mode='lines',
                          line=dict(color=COLORS.get(lang, '#888888'), width=2)),
                row=2, col=2
            )
    
    # Update layout
    fig.update_layout(
        title_text="API Performance Dashboard",
        title_font_size=24,
        showlegend=True,
        height=1000,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Language", row=1, col=1)
    fig.update_yaxes(title_text="Requests/sec", row=1, col=1)
    fig.update_xaxes(title_text="Language", row=1, col=2)
    fig.update_yaxes(title_text="Success Rate (%)", row=1, col=2)
    fig.update_xaxes(title_text="Language", row=2, col=1)
    fig.update_yaxes(title_text="Response Time (ms)", row=2, col=1)
    fig.update_xaxes(title_text="Time (seconds)", row=2, col=2)
    fig.update_yaxes(title_text="Cumulative Requests", row=2, col=2)
    
    # Save to HTML
    fig.write_html(output_dir / 'api_performance_dashboard.html')
    print("✓ Generated api_performance_dashboard.html")

def main():
    """Main function to generate all visualizations."""
    print("\n" + "="*60)
    print("API Performance Visualization Generator")
    print("="*60 + "\n")
    
    # Load results
    print("Loading API test results...\n")
    results = load_results()
    print(f"\n✓ Successfully loaded {len(results)} language results\n")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'graphs'
    output_dir.mkdir(exist_ok=True)
    
    # Generate visualizations
    print("Generating visualizations...\n")
    
    try:
        create_throughput_comparison(results, output_dir)
        create_response_time_distribution(results, output_dir)
        create_cumulative_requests_timeline(results, output_dir)
        create_response_time_heatmap(results, output_dir)
        create_success_rate_comparison(results, output_dir)
        create_interactive_dashboard(results, output_dir)
        
        print("\n" + "="*60)
        print("✓ All visualizations generated successfully!")
        print(f"✓ Output directory: {output_dir}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
