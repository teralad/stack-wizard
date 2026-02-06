# Stack Wizard - Quick Reference

## Quick Start

### Interactive Mode (Easiest)
```bash
python3 stack_recommender.py
```

### Command-Line Examples

```bash
# High-performance API
python3 stack_recommender.py -p 9 -s 8 --project-type api

# Startup MVP
python3 stack_recommender.py -d 9 -t small --project-type webapp

# Machine Learning Service
python3 stack_recommender.py --ml-ai -p 7 --project-type "ML API"

# Real-time Chat
python3 stack_recommender.py --real-time -s 8 --project-type chat

# Enterprise Microservices
python3 stack_recommender.py --enterprise --microservices -t large -s 9

# With Team Expertise
python3 stack_recommender.py -d 7 -e Python,JavaScript --project-type api

# Serverless API with latency target
python3 stack_recommender.py --deployment serverless --latency-ms 150 -p 7 -s 6 --project-type api

# Compliance-heavy enterprise system
python3 stack_recommender.py --enterprise --compliance HIPAA --team-size large -s 8 -p 6

# Must-use/avoid constraints
python3 stack_recommender.py --must-use Rust --avoid Python,JavaScript -p 8 -s 7

# Show only top 3 recommendations
python3 stack_recommender.py --top 3 -p 8 -s 7
```

## Command-Line Options

| Option | Values | Description |
|--------|--------|-------------|
| `-p, --performance` | 1-10 | Performance priority (10 = critical) |
| `-s, --scalability` | 1-10 | Scalability needs (10 = millions of users) |
| `-d, --dev-speed` | 1-10 | Development speed priority (10 = MVP fast) |
| `-t, --team-size` | small/medium/large | Team size |
| `-pt, --project-type` | text | Type of project (api, webapp, chat, etc.) |
| `--budget` | low/medium/high | Budget sensitivity |
| `--deployment` | serverless/containers/on-prem/edge/hybrid | Deployment model |
| `--latency-ms` | number | Target p95 latency in ms |
| `--throughput-rps` | number | Target throughput (requests per second) |
| `--io-bound` | flag | I/O-bound workload (lots of network calls) |
| `--data-store` | sql/nosql/mixed | Data store preference |
| `--compliance` | comma-separated | Compliance requirements |
| `--hiring-priority` | low/medium/high | Hiring availability importance |
| `--must-use` | comma-separated | Must-use languages |
| `--avoid` | comma-separated | Languages to avoid |
| `--top` | number | Limit number of recommendations (default: all) |
| `--real-time` | flag | Real-time features needed |
| `--ml-ai` | flag | Machine learning/AI features |
| `--enterprise` | flag | Enterprise application |
| `--microservices` | flag | Microservices architecture |
| `-e, --team-expertise` | comma-separated | Languages team knows |
| `-h, --help` | flag | Show help |

## Quick Decision Guide

### Choose Python if:
- 🤖 ML/AI features needed
- 🚀 Rapid prototyping/MVP
- 📊 Data-heavy application
- 👥 Small team, quick delivery

### Choose JavaScript (Node.js) if:
- ⚡ Real-time features (WebSockets)
- 🔄 Full-stack JavaScript team
- 🌐 Event-driven architecture
- 🎯 Microservices with fast I/O

### Choose Go if:
- ☁️ Cloud-native microservices
- 🔀 High concurrency needs
- ⚡ Fast performance + simple code
- 🐳 Containerized applications

### Choose Rust if:
- 🏎️ Maximum performance required
- 🔒 Security-critical system
- 🎮 Low-latency applications
- 💾 Systems programming

### Choose Java if:
- 🏢 Enterprise application
- 👥 Large team (20+ developers)
- 📈 Proven at massive scale
- 🔧 Need mature ecosystem

### Choose C# if:
- 🏢 Enterprise on Microsoft stack
- ☁️ Azure cloud deployment
- 🪟 Windows integration needed
- 🎮 Gaming backend

### Choose Ruby if:
- 🚀 Startup MVP
- 💡 Rapid web development
- 📝 Convention over configuration
- 👥 Small-medium team

### Choose Elixir if:
- 💬 Real-time chat/collaboration
- 🔀 Massive concurrency (millions)
- 🛡️ Fault-tolerant system
- 📡 IoT or distributed systems

### Choose Scala if:
- 💰 Financial/trading systems
- 📊 Big data processing
- 🧮 Complex business logic
- 🔍 Type safety critical

### Choose C++ if:
- 🏎️ Absolute maximum performance
- 🎮 Game servers
- ⚡ Ultra-low latency
- 🔧 System-level control

## Framework Quick Reference

| Language | Rapid Dev | APIs | Enterprise | Real-time |
|----------|-----------|------|------------|-----------|
| Python | Django, Flask | **FastAPI** | Django | FastAPI |
| JavaScript | Express | Express | **NestJS** | Socket.io |
| Go | - | **Gin**, Echo | Gin | Gin |
| Rust | - | **Actix-web** | Actix-web | Actix-web |
| Java | - | Spring Boot | **Spring Boot** | Spring Boot |
| C# | - | ASP.NET Core | **ASP.NET Core** | SignalR |
| Ruby | **Rails** | Sinatra | Rails | - |
| Elixir | Phoenix | Phoenix | - | **Phoenix** |
| Scala | Play | Akka HTTP | Play | Akka |
| C++ | - | Drogon | - | Drogon |

## Common Scenarios Cheat Sheet

| Scenario | Recommended Stack | Why |
|----------|------------------|-----|
| **Startup MVP** | Python/Django or Ruby/Rails | Fast development, full-featured |
| **High-Traffic API** | Go/Gin or Rust/Actix | Performance + scalability |
| **ML Model Serving** | Python/FastAPI | Best ML ecosystem |
| **Real-time Chat** | Elixir/Phoenix or Node/NestJS | Built for real-time |
| **Enterprise System** | Java/Spring Boot or C#/ASP.NET | Mature, proven at scale |
| **Microservices** | Go/Gin or Java/Spring Boot | Cloud-native, containerized |
| **Trading Platform** | Rust/Actix or C++/Drogon | Ultra-low latency |
| **Data Pipeline** | Scala/Akka or Python/FastAPI | Data processing strength |
| **IoT Backend** | Elixir/Phoenix or Go/Gin | Massive concurrency |
| **Mobile Backend** | Node/Express or Python/FastAPI | Quick API development |

## Priority Guidelines

### Performance Priority
- **1-3**: Performance not critical → Python, Ruby OK
- **4-6**: Moderate performance → Most languages work
- **7-8**: Good performance → Go, Java, C#
- **9-10**: Maximum performance → Rust, C++, Go

### Scalability Priority
- **1-3**: Small scale → Any language
- **4-6**: Medium scale → Most languages with good architecture
- **7-8**: High scale → Go, Java, C#, Elixir
- **9-10**: Massive scale → Go, Elixir, Rust, Java

### Development Speed Priority
- **1-3**: Time available → Can use complex languages (Rust, C++)
- **4-6**: Normal timeline → Most languages
- **7-8**: Fast delivery → Python, Ruby, JavaScript
- **9-10**: Ultra-fast MVP → Python/Django, Ruby/Rails

### Team Size
- **Small (1-5)**: Simple languages → Python, Go, Ruby
- **Medium (5-20)**: Most languages work well
- **Large (20+)**: Strong typing helps → Java, C#, TypeScript

## Tips

### 🎯 Be Realistic
Don't set everything to 10. Prioritize what actually matters.

### 👥 Leverage Team Skills
If your team knows a language well, use `-e` flag. Expertise matters!

### 🔍 Read the Justifications
Top recommendation isn't always the answer. Review top 2-3 options.

### 🧪 Test Multiple Scenarios
Run the tool with different priorities to understand trade-offs.

### 📚 Check the Ecosystem
Verify the recommended language has libraries for your specific needs.

### 🏢 Consider Operations
Can you hire for this language? Do you have hosting expertise?

## Running Tests

```bash
# Run automated tests
python3 test_recommender.py

# Run example scenarios
python3 examples.py
```

## Get Help

```bash
# Show help
python3 stack_recommender.py --help

# Read full guide
cat STACK_RECOMMENDATION_GUIDE.md

# Check README
cat README.md
```

## Contributing

Found an issue or want to improve recommendations? Open an issue or PR at:
https://github.com/teralad/stack-wizard

---

**Stack Wizard** - Choose the right stack, backed by data and benchmarks.
