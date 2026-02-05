#!/usr/bin/env python3
"""
Example scenarios demonstrating the Stack Recommender
"""

import subprocess
import sys

def run_example(title, args, description):
    """Run an example and display results"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)
    print(f"\n{description}\n")
    print(f"Command: python3 stack_recommender.py {args}\n")
    
    result = subprocess.run(
        f"python3 stack_recommender.py {args}",
        shell=True,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False
    return True

def main():
    print("\n" + "="*80)
    print("  STACK WIZARD - Example Scenarios")
    print("="*80)
    
    examples = [
        (
            "Example 1: High-Performance API",
            "-p 9 -s 8 --project-type api",
            "Building a high-performance RESTful API that needs to handle lots of requests."
        ),
        (
            "Example 2: Startup MVP",
            "-d 9 -t small --project-type webapp -s 4",
            "Small startup team needs to build an MVP web application quickly."
        ),
        (
            "Example 3: Machine Learning Service",
            "--ml-ai -p 7 --project-type 'ML API' -d 6",
            "Building an API to serve machine learning model predictions."
        ),
        (
            "Example 4: Real-Time Chat App",
            "--real-time -s 8 --project-type 'chat application' -p 6",
            "Creating a real-time chat application with WebSocket support."
        ),
        (
            "Example 5: Enterprise Microservices",
            "--enterprise --microservices -t large -s 9 -p 7",
            "Large enterprise building a microservices architecture."
        ),
        (
            "Example 6: Team with Python Expertise",
            "-d 7 -s 6 --project-type api -e Python",
            "Team already knows Python well, building a new API service."
        )
    ]
    
    for title, args, description in examples:
        if not run_example(title, args, description):
            print(f"\nFailed to run example: {title}")
            return 1
    
    print("\n" + "="*80)
    print("  All examples completed successfully!")
    print("="*80 + "\n")
    return 0

if __name__ == '__main__':
    sys.exit(main())
