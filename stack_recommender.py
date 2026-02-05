#!/usr/bin/env python3
"""
Stack Wizard - Intelligent Backend Stack Recommendation System

This tool analyzes project requirements and recommends the best backend
language and framework combination based on various criteria including:
- Performance requirements
- Scalability needs
- Team expertise
- Project type and complexity
- Development speed priorities
- Budget constraints
- Deployment model
- Compliance requirements
- Reliability targets (latency/throughput)
"""

import sys
import json
from typing import Dict, List, Tuple

# Backend language and framework combinations
STACK_OPTIONS = {
    'python': {
        'name': 'Python',
        'frameworks': ['Django', 'Flask', 'FastAPI', 'Tornado'],
        'strengths': ['Rapid development', 'Large ecosystem', 'Data science', 'Machine learning', 'Easy learning curve'],
        'weaknesses': ['Slower execution', 'GIL for concurrency', 'Higher memory usage'],
        'best_for': ['MVPs', 'Data-heavy applications', 'APIs', 'ML/AI services', 'Prototyping'],
        'team_size': 'any',
        'maturity': 'high'
    },
    'javascript': {
        'name': 'JavaScript (Node.js)',
        'frameworks': ['Express.js', 'NestJS', 'Koa', 'Fastify', 'Hapi'],
        'strengths': ['Full-stack JS', 'Event-driven', 'Large ecosystem', 'Real-time apps', 'Fast I/O'],
        'weaknesses': ['Callback complexity', 'Single-threaded', 'Type safety issues'],
        'best_for': ['Real-time apps', 'APIs', 'Microservices', 'Full-stack JS teams', 'Chat apps'],
        'team_size': 'any',
        'maturity': 'high'
    },
    'go': {
        'name': 'Go',
        'frameworks': ['Gin', 'Echo', 'Fiber', 'Chi', 'Gorilla', 'Buffalo', 'Goa', 'Beego'],
        'strengths': ['Fast execution', 'Easy concurrency', 'Simple syntax', 'Good performance', 'Built-in tooling'],
        'weaknesses': ['Limited ecosystem', 'Verbose error handling', 'Less mature frameworks'],
        'best_for': ['Microservices', 'Cloud services', 'APIs', 'CLI tools', 'Network services'],
        'team_size': 'small-to-medium',
        'maturity': 'medium-high'
    },
    'rust': {
        'name': 'Rust',
        'frameworks': ['Actix-web', 'Rocket', 'Warp', 'Axum'],
        'strengths': ['Highest performance', 'Memory safety', 'Zero-cost abstractions', 'Thread safety'],
        'weaknesses': ['Steep learning curve', 'Slower development', 'Smaller ecosystem'],
        'best_for': ['High-performance services', 'Systems programming', 'Security-critical apps', 'WebAssembly'],
        'team_size': 'small',
        'maturity': 'medium'
    },
    'java': {
        'name': 'Java',
        'frameworks': ['Spring Boot', 'Micronaut', 'Quarkus', 'Dropwizard', 'Helidon', 'Vert.x', 'Javalin'],
        'strengths': ['Enterprise-ready', 'Mature ecosystem', 'Strong typing', 'JVM performance', 'Large talent pool'],
        'weaknesses': ['Verbose syntax', 'Slower startup', 'Higher memory usage', 'Complex config'],
        'best_for': ['Enterprise apps', 'Large systems', 'Banking/Finance', 'Long-term projects', 'Android backends'],
        'team_size': 'medium-to-large',
        'maturity': 'very-high'
    },
    'csharp': {
        'name': 'C#',
        'frameworks': ['ASP.NET Core', '.NET', 'Nancy', 'ServiceStack', 'FastEndpoints', 'Carter', 'Minimal APIs'],
        'strengths': ['Modern language', 'Excellent tooling', 'Cross-platform', 'Strong typing', 'Great async support'],
        'weaknesses': ['Microsoft ecosystem', 'Limited Linux talent', 'Licensing concerns'],
        'best_for': ['Enterprise apps', 'Windows services', 'Azure cloud', 'Gaming backends', 'Desktop integration'],
        'team_size': 'medium-to-large',
        'maturity': 'very-high'
    },
    'ruby': {
        'name': 'Ruby',
        'frameworks': ['Ruby on Rails', 'Sinatra', 'Hanami', 'Grape'],
        'strengths': ['Developer happiness', 'Convention over config', 'Rapid prototyping', 'Clean syntax'],
        'weaknesses': ['Slower execution', 'Scaling challenges', 'Smaller talent pool', 'Memory usage'],
        'best_for': ['Startups', 'MVPs', 'Web applications', 'Content management', 'Rapid development'],
        'team_size': 'small-to-medium',
        'maturity': 'high'
    },
    'elixir': {
        'name': 'Elixir',
        'frameworks': ['Phoenix', 'Plug', 'Nerves'],
        'strengths': ['Fault tolerance', 'Concurrency', 'Scalability', 'Real-time', 'Functional programming'],
        'weaknesses': ['Smaller community', 'Learning curve', 'Limited libraries', 'Niche'],
        'best_for': ['Real-time systems', 'Chat applications', 'IoT', 'Distributed systems', 'High concurrency'],
        'team_size': 'small',
        'maturity': 'medium'
    },
    'scala': {
        'name': 'Scala',
        'frameworks': ['Play Framework', 'Akka HTTP', 'Finatra', 'Http4s'],
        'strengths': ['Functional + OO', 'JVM performance', 'Type safety', 'Concurrency', 'Scalable'],
        'weaknesses': ['Complex syntax', 'Steep learning curve', 'Slow compilation', 'Small talent pool'],
        'best_for': ['Data processing', 'Streaming apps', 'Financial systems', 'Big data', 'Complex systems'],
        'team_size': 'small-to-medium',
        'maturity': 'medium-high'
    },
    'cpp': {
        'name': 'C++',
        'frameworks': ['Crow', 'Pistache', 'Drogon', 'oatpp'],
        'strengths': ['Maximum performance', 'Low-level control', 'System access', 'Legacy integration'],
        'weaknesses': ['Memory management', 'Complex development', 'Security risks', 'Slow development'],
        'best_for': ['High-performance computing', 'Game servers', 'Embedded systems', 'Low-latency trading'],
        'team_size': 'small',
        'maturity': 'high'
    }
}

FRAMEWORK_DETAILS = {
    'Django': {
        'type': 'Full-featured',
        'strengths': ['Batteries included', 'Admin panel', 'ORM', 'Security features'],
        'best_for': ['CMS', 'Social networks', 'E-commerce', 'Complex apps']
    },
    'Flask': {
        'type': 'Micro-framework',
        'strengths': ['Lightweight', 'Flexible', 'Simple', 'Easy to learn'],
        'best_for': ['APIs', 'Small apps', 'Custom solutions', 'Learning']
    },
    'FastAPI': {
        'type': 'Modern API',
        'strengths': ['Fast', 'Async', 'Type hints', 'Auto docs', 'Modern'],
        'best_for': ['APIs', 'Microservices', 'ML services', 'Modern projects']
    },
    'Spring Boot': {
        'type': 'Enterprise',
        'strengths': ['Comprehensive', 'Production-ready', 'Microservices', 'Security'],
        'best_for': ['Enterprise', 'Microservices', 'Cloud', 'Large systems']
    },
    'Micronaut': {
        'type': 'Cloud-native',
        'strengths': ['Fast startup', 'Low memory', 'DI compile-time', 'Serverless'],
        'best_for': ['Microservices', 'Serverless', 'Cloud', 'Fast startup']
    },
    'Quarkus': {
        'type': 'Cloud-native',
        'strengths': ['Fast startup', 'Kubernetes', 'GraalVM', 'Dev services'],
        'best_for': ['Microservices', 'Containers', 'Serverless', 'Cloud']
    },
    'Dropwizard': {
        'type': 'Minimal',
        'strengths': ['Operationally focused', 'Metrics', 'Simple'],
        'best_for': ['APIs', 'Microservices', 'Small services']
    },
    'Helidon': {
        'type': 'Microservices',
        'strengths': ['Lightweight', 'Reactive', 'Configurable'],
        'best_for': ['Microservices', 'Cloud', 'Reactive systems']
    },
    'Vert.x': {
        'type': 'Reactive',
        'strengths': ['Event-driven', 'Reactive', 'Polyglot'],
        'best_for': ['Real-time', 'Event-driven', 'Reactive systems']
    },
    'Javalin': {
        'type': 'Minimal',
        'strengths': ['Simple', 'Lightweight', 'Fast'],
        'best_for': ['APIs', 'Microservices', 'Simple services']
    },
    'Express.js': {
        'type': 'Minimal',
        'strengths': ['Simple', 'Flexible', 'Large ecosystem', 'Unopinionated'],
        'best_for': ['APIs', 'Web apps', 'Microservices', 'Rapid dev']
    },
    'NestJS': {
        'type': 'Structured',
        'strengths': ['TypeScript', 'Angular-like', 'Scalable', 'Modular'],
        'best_for': ['Enterprise', 'Large teams', 'Microservices', 'GraphQL']
    },
    'Ruby on Rails': {
        'type': 'Full-stack',
        'strengths': ['Convention over config', 'Rapid dev', 'Mature', 'Community'],
        'best_for': ['Startups', 'MVPs', 'Web apps', 'SaaS']
    },
    'Phoenix': {
        'type': 'Real-time',
        'strengths': ['Channels', 'Scalable', 'Fast', 'Fault-tolerant'],
        'best_for': ['Real-time', 'Chat', 'Collaborative apps', 'APIs']
    },
    'ASP.NET Core': {
        'type': 'Enterprise',
        'strengths': ['Performance', 'Cross-platform', 'Tooling', 'Security'],
        'best_for': ['Enterprise', 'Azure', 'Microservices', 'APIs']
    },
    'ServiceStack': {
        'type': 'Productivity',
        'strengths': ['Productivity', 'Typed APIs', 'Performance'],
        'best_for': ['APIs', 'Services', 'Enterprise']
    },
    'FastEndpoints': {
        'type': 'Minimal',
        'strengths': ['Minimal APIs', 'Performance', 'Typed endpoints'],
        'best_for': ['APIs', 'Microservices', 'High throughput']
    },
    'Carter': {
        'type': 'Minimal',
        'strengths': ['Modular routing', 'Minimal APIs', 'Simple'],
        'best_for': ['APIs', 'Microservices', 'Simple services']
    },
    'Minimal APIs': {
        'type': 'Minimal',
        'strengths': ['Lightweight', 'Fast startup', 'Simple'],
        'best_for': ['APIs', 'Microservices', 'Small services']
    },
    'Gin': {
        'type': 'Fast',
        'strengths': ['Performance', 'Simple', 'Middleware', 'JSON'],
        'best_for': ['APIs', 'Microservices', 'High throughput', 'Simple services']
    },
    'Echo': {
        'type': 'Fast',
        'strengths': ['Performance', 'Middleware', 'Minimal'],
        'best_for': ['APIs', 'Microservices', 'High throughput']
    },
    'Fiber': {
        'type': 'Fast',
        'strengths': ['Express-like', 'Performance', 'Low overhead'],
        'best_for': ['APIs', 'Microservices', 'High throughput']
    },
    'Chi': {
        'type': 'Minimal',
        'strengths': ['Lightweight', 'Composable', 'Router'],
        'best_for': ['APIs', 'Microservices', 'Simple services']
    },
    'Gorilla': {
        'type': 'Toolkit',
        'strengths': ['Stable', 'Routing', 'Middleware'],
        'best_for': ['APIs', 'Microservices', 'Traditional services']
    },
    'Buffalo': {
        'type': 'Full-stack',
        'strengths': ['Conventions', 'Productivity', 'All-in-one'],
        'best_for': ['Web apps', 'Full-stack', 'Rapid dev']
    },
    'Goa': {
        'type': 'Design-first',
        'strengths': ['Design-first', 'Codegen', 'Typed APIs'],
        'best_for': ['APIs', 'Microservices', 'Contracts']
    },
    'Beego': {
        'type': 'Full-stack',
        'strengths': ['Full-featured', 'ORM', 'Scaffolding'],
        'best_for': ['Web apps', 'APIs', 'Rapid dev']
    },
    'Actix-web': {
        'type': 'High-performance',
        'strengths': ['Fastest', 'Actor model', 'Async', 'Type-safe'],
        'best_for': ['High-performance', 'Real-time', 'WebSockets', 'APIs']
    }
}


class StackRecommender:
    """Analyzes requirements and recommends the best backend stack"""
    
    def __init__(self):
        self.scores = {}
        self.requirements = {}
    
    def analyze_requirements(self, requirements: Dict) -> List[Tuple[str, float, str]]:
        """
        Analyze requirements and score each language
        
        Args:
            requirements: Dictionary of project requirements
        
        Returns:
            List of (language, score, framework) tuples sorted by score
        """
        self.requirements = requirements
        self.scores = {}
        
        # Apply hard constraints first
        constrained_languages = list(STACK_OPTIONS.keys())
        must_use = [l.strip().lower() for l in requirements.get('must_use', []) if l.strip()]
        avoid = [l.strip().lower() for l in requirements.get('avoid', []) if l.strip()]

        if must_use:
            constrained_languages = [l for l in constrained_languages if l in must_use]
            if not constrained_languages:
                # If nothing matches, fall back to all and note the miss
                constrained_languages = list(STACK_OPTIONS.keys())
                requirements['constraint_miss'] = True

        if avoid:
            constrained_languages = [l for l in constrained_languages if l not in avoid]

        # Score each language
        for lang_key in constrained_languages:
            lang_data = STACK_OPTIONS[lang_key]
            score = 0.0
            
            # Performance requirements (0-10)
            performance_need = requirements.get('performance', 5)
            if lang_key in ['rust', 'cpp']:
                score += performance_need * 1.5
            elif lang_key in ['go', 'java', 'csharp']:
                score += performance_need * 1.2
            elif lang_key in ['javascript', 'elixir', 'scala']:
                score += performance_need * 0.8
            else:
                score += performance_need * 0.5
            
            # Scalability requirements (0-10)
            scalability_need = requirements.get('scalability', 5)
            if lang_key in ['go', 'elixir', 'rust']:
                score += scalability_need * 1.4
            elif lang_key in ['java', 'csharp', 'scala']:
                score += scalability_need * 1.2
            else:
                score += scalability_need * 0.8
            
            # Development speed priority (0-10)
            dev_speed = requirements.get('development_speed', 5)
            if lang_key in ['python', 'ruby', 'javascript']:
                score += dev_speed * 1.5
            elif lang_key in ['go', 'java', 'csharp']:
                score += dev_speed * 1.0
            else:
                score += dev_speed * 0.6
            
            # Team size consideration
            team_size = requirements.get('team_size', 'medium')
            if team_size == 'large' and lang_data['team_size'] in ['medium-to-large', 'any']:
                score += 10
            elif team_size == 'small' and lang_data['team_size'] in ['small', 'small-to-medium', 'any']:
                score += 8
            
            # Project type matching
            project_type = requirements.get('project_type', '')
            if project_type and self._matches_project_type(project_type, lang_data):
                score += 15
            
            # Real-time requirements
            if requirements.get('real_time', False):
                if lang_key in ['elixir', 'javascript', 'go']:
                    score += 12
            
            # Machine learning / AI
            if requirements.get('ml_ai', False):
                if lang_key == 'python':
                    score += 20
            
            # Existing team expertise
            team_expertise = requirements.get('team_expertise', [])
            if lang_key in [e.lower() for e in team_expertise]:
                score += 15
            
            # Enterprise requirements
            if requirements.get('enterprise', False):
                if lang_key in ['java', 'csharp', 'scala']:
                    score += 12
            
            # Microservices architecture
            if requirements.get('microservices', False):
                if lang_key in ['go', 'java', 'javascript']:
                    score += 10

            # Budget constraints
            budget = requirements.get('budget', '').lower()
            if budget == 'low' and lang_key in ['python', 'javascript', 'go', 'ruby']:
                score += 5
            elif budget == 'high' and lang_key in ['java', 'csharp', 'rust']:
                score += 3

            # Deployment model
            deployment = requirements.get('deployment', '').lower()
            if deployment == 'serverless' and lang_key in ['python', 'javascript', 'go']:
                score += 6
            elif deployment == 'containers' and lang_key in ['go', 'rust', 'java']:
                score += 4
            elif deployment == 'on-prem' and lang_key in ['java', 'csharp']:
                score += 5
            elif deployment == 'edge' and lang_key in ['rust', 'cpp', 'go']:
                score += 6

            # Reliability targets
            latency_ms = requirements.get('latency_ms')
            if isinstance(latency_ms, int):
                if latency_ms <= 100 and lang_key in ['rust', 'cpp', 'go']:
                    score += 6
                elif latency_ms <= 500 and lang_key in ['java', 'csharp', 'go']:
                    score += 4

            throughput_rps = requirements.get('throughput_rps')
            if isinstance(throughput_rps, int):
                if throughput_rps >= 10000 and lang_key in ['go', 'rust', 'cpp']:
                    score += 6
                elif throughput_rps >= 1000 and lang_key in ['go', 'rust', 'java']:
                    score += 4

            # Data store preference
            data_store = requirements.get('data_store', '').lower()
            if data_store == 'sql' and lang_key in ['java', 'csharp', 'python', 'ruby']:
                score += 3
            elif data_store == 'nosql' and lang_key in ['javascript', 'go']:
                score += 3

            # Compliance requirements
            compliance = [c.lower() for c in requirements.get('compliance', [])]
            if compliance:
                if lang_key in ['java', 'csharp']:
                    score += 6
                elif lang_key in ['python', 'go']:
                    score += 3

            # Hiring priority
            hiring_priority = requirements.get('hiring_priority', '').lower()
            if hiring_priority == 'high' and lang_key in ['python', 'javascript', 'java', 'csharp']:
                score += 5
            
            self.scores[lang_key] = score
        
        # Get top recommendations
        sorted_langs = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        
        # Match with best framework for each language
        recommendations = []
        for lang_key, score in sorted_langs[:5]:  # Top 5
            framework = self._recommend_framework(lang_key, requirements)
            recommendations.append((lang_key, score, framework))
        
        return recommendations
    
    def _matches_project_type(self, project_type: str, lang_data: Dict) -> bool:
        """Check if project type matches language's best use cases"""
        best_for_text = ' '.join(lang_data['best_for']).lower()
        project_keywords = [pt.strip().lower() for pt in project_type.split(',')]
        return any(keyword in best_for_text for keyword in project_keywords)
    
    def _recommend_framework(self, lang_key: str, requirements: Dict) -> str:
        """Recommend the best framework for a language based on requirements"""
        frameworks = STACK_OPTIONS[lang_key]['frameworks']
        
        # Simple framework selection logic
        project_type = requirements.get('project_type', '').lower()
        
        if lang_key == 'python':
            if 'api' in project_type or requirements.get('ml_ai'):
                return 'FastAPI'
            elif requirements.get('enterprise') or 'complex' in project_type:
                return 'Django'
            else:
                return 'Flask'
        
        elif lang_key == 'javascript':
            if requirements.get('enterprise') or requirements.get('team_size') == 'large':
                return 'NestJS'
            else:
                return 'Express.js'
        
        elif lang_key == 'java':
            return 'Spring Boot'
        
        elif lang_key == 'go':
            return 'Gin'
        
        elif lang_key == 'rust':
            return 'Actix-web'
        
        elif lang_key == 'ruby':
            return 'Ruby on Rails'
        
        elif lang_key == 'elixir':
            return 'Phoenix'
        
        elif lang_key == 'csharp':
            return 'ASP.NET Core'
        
        elif lang_key == 'scala':
            return 'Play Framework'
        
        elif lang_key == 'cpp':
            return 'Drogon'
        
        return frameworks[0] if frameworks else 'None'
    
    def format_recommendation(self, recommendations: List[Tuple[str, float, str]]) -> str:
        """Format recommendations as a readable string"""
        output = []
        output.append("\n" + "="*80)
        output.append("  STACK WIZARD - BACKEND STACK RECOMMENDATIONS")
        output.append("="*80 + "\n")
        
        for idx, (lang_key, score, framework) in enumerate(recommendations, 1):
            lang_data = STACK_OPTIONS[lang_key]
            output.append(f"\n#{idx}. {lang_data['name']} with {framework}")
            output.append(f"    Score: {score:.1f}/100")
            output.append(f"    Framework Type: {FRAMEWORK_DETAILS.get(framework, {}).get('type', 'N/A')}")
            output.append(f"\n    Strengths:")
            for strength in lang_data['strengths'][:3]:
                output.append(f"      ✓ {strength}")
            
            if framework in FRAMEWORK_DETAILS:
                output.append(f"\n    Framework Strengths:")
                for strength in FRAMEWORK_DETAILS[framework]['strengths'][:3]:
                    output.append(f"      ✓ {strength}")
            
            output.append(f"\n    Best For:")
            for use_case in lang_data['best_for'][:3]:
                output.append(f"      • {use_case}")
            
            output.append(f"\n    Considerations:")
            for weakness in lang_data['weaknesses'][:2]:
                output.append(f"      ⚠ {weakness}")
            output.append("")
        
        output.append("="*80)
        output.append("\nRecommendation Criteria Used:")
        if self.requirements.get('budget'):
            output.append(f"  • Budget: {self.requirements['budget']}")
        if self.requirements.get('deployment'):
            output.append(f"  • Deployment Model: {self.requirements['deployment']}")
        if self.requirements.get('performance'):
            output.append(f"  • Performance Priority: {self.requirements['performance']}/10")
        if self.requirements.get('scalability'):
            output.append(f"  • Scalability Need: {self.requirements['scalability']}/10")
        if self.requirements.get('development_speed'):
            output.append(f"  • Development Speed: {self.requirements['development_speed']}/10")
        if self.requirements.get('team_size'):
            output.append(f"  • Team Size: {self.requirements['team_size']}")
        if self.requirements.get('project_type'):
            output.append(f"  • Project Type: {self.requirements['project_type']}")
        if self.requirements.get('latency_ms'):
            output.append(f"  • Latency Target: {self.requirements['latency_ms']} ms")
        if self.requirements.get('throughput_rps'):
            output.append(f"  • Throughput Target: {self.requirements['throughput_rps']} rps")
        if self.requirements.get('data_store'):
            output.append(f"  • Data Store Preference: {self.requirements['data_store']}")
        if self.requirements.get('compliance'):
            output.append(f"  • Compliance: {', '.join(self.requirements['compliance'])}")
        if self.requirements.get('hiring_priority'):
            output.append(f"  • Hiring Priority: {self.requirements['hiring_priority']}")
        if self.requirements.get('must_use'):
            output.append(f"  • Must Use: {', '.join(self.requirements['must_use'])}")
        if self.requirements.get('avoid'):
            output.append(f"  • Avoid: {', '.join(self.requirements['avoid'])}")
        if self.requirements.get('constraint_miss'):
            output.append("  • Note: None of the must-use languages matched; broadened recommendations.")

        missing = []
        for key, label in [
            ('performance', 'Performance'),
            ('scalability', 'Scalability'),
            ('development_speed', 'Development Speed'),
            ('team_size', 'Team Size'),
            ('project_type', 'Project Type'),
            ('deployment', 'Deployment Model'),
            ('latency_ms', 'Latency Target'),
            ('throughput_rps', 'Throughput Target'),
            ('budget', 'Budget'),
            ('compliance', 'Compliance'),
        ]:
            if not self.requirements.get(key):
                missing.append(label)
        if missing:
            output.append("\nMissing Inputs (may reduce confidence):")
            for item in missing:
                output.append(f"  • {item}")
        
        output.append("\n" + "="*80)
        
        return "\n".join(output)


def interactive_mode():
    """Run the recommender in interactive mode"""
    print("\n" + "="*80)
    print("  STACK WIZARD - Backend Stack Recommendation Tool")
    print("="*80)
    print("\nAnswer the following questions to get personalized stack recommendations.\n")
    
    requirements = {}
    
    # Performance requirements
    print("1. How important is raw performance for your project? (1-10)")
    print("   1 = Not important | 5 = Moderate | 10 = Critical")
    while True:
        try:
            perf = int(input("   Your answer: ").strip() or "5")
            if 1 <= perf <= 10:
                requirements['performance'] = perf
                break
            print("   Please enter a number between 1 and 10")
        except ValueError:
            print("   Please enter a valid number")
    
    # Scalability requirements
    print("\n2. What are your scalability requirements? (1-10)")
    print("   1 = Small app | 5 = Medium traffic | 10 = Massive scale")
    while True:
        try:
            scale = int(input("   Your answer: ").strip() or "5")
            if 1 <= scale <= 10:
                requirements['scalability'] = scale
                break
            print("   Please enter a number between 1 and 10")
        except ValueError:
            print("   Please enter a valid number")
    
    # Development speed
    print("\n3. How important is rapid development? (1-10)")
    print("   1 = Not important | 5 = Moderate | 10 = Need MVP fast")
    while True:
        try:
            speed = int(input("   Your answer: ").strip() or "5")
            if 1 <= speed <= 10:
                requirements['development_speed'] = speed
                break
            print("   Please enter a number between 1 and 10")
        except ValueError:
            print("   Please enter a valid number")
    
    # Team size
    print("\n4. What is your team size?")
    print("   Options: small (1-5), medium (5-20), large (20+)")
    team = input("   Your answer: ").strip().lower() or "medium"
    requirements['team_size'] = team if team in ['small', 'medium', 'large'] else 'medium'
    
    # Project type
    print("\n5. What type of project are you building?")
    print("   (e.g., API, microservice, web app, real-time app, ML service, e-commerce)")
    project_type = input("   Your answer: ").strip()
    if project_type:
        requirements['project_type'] = project_type

    # Budget constraints
    print("\n6. What is your budget sensitivity?")
    print("   Options: low / medium / high")
    budget = input("   Your answer: ").strip().lower()
    if budget in ['low', 'medium', 'high']:
        requirements['budget'] = budget
    
    # Real-time requirements
    print("\n7. Do you need real-time features? (yes/no)")
    real_time = input("   Your answer: ").strip().lower()
    requirements['real_time'] = real_time in ['yes', 'y', 'true']
    
    # ML/AI requirements
    print("\n8. Will this involve machine learning or AI? (yes/no)")
    ml_ai = input("   Your answer: ").strip().lower()
    requirements['ml_ai'] = ml_ai in ['yes', 'y', 'true']
    
    # Enterprise requirements
    print("\n9. Is this an enterprise application? (yes/no)")
    enterprise = input("   Your answer: ").strip().lower()
    requirements['enterprise'] = enterprise in ['yes', 'y', 'true']
    
    # Microservices
    print("\n10. Are you building microservices? (yes/no)")
    microservices = input("   Your answer: ").strip().lower()
    requirements['microservices'] = microservices in ['yes', 'y', 'true']

    # Deployment model
    print("\n11. What is your deployment model?")
    print("    Options: serverless / containers / on-prem / edge / hybrid / unsure")
    deployment = input("    Your answer: ").strip().lower()
    if deployment in ['serverless', 'containers', 'on-prem', 'edge', 'hybrid']:
        requirements['deployment'] = deployment

    # Reliability targets
    print("\n12. What is your target p95 latency in ms? (press Enter to skip)")
    latency = input("    Your answer: ").strip()
    if latency.isdigit():
        requirements['latency_ms'] = int(latency)

    print("\n13. What throughput do you expect (requests per second)? (press Enter to skip)")
    rps = input("    Your answer: ").strip()
    if rps.isdigit():
        requirements['throughput_rps'] = int(rps)

    # Data store preference
    print("\n14. Data store preference?")
    print("    Options: sql / nosql / mixed / unsure")
    data_store = input("    Your answer: ").strip().lower()
    if data_store in ['sql', 'nosql', 'mixed']:
        requirements['data_store'] = data_store

    # Compliance
    print("\n15. Any compliance requirements? (comma-separated, e.g., HIPAA, GDPR, SOC2)")
    compliance = input("    Your answer: ").strip()
    if compliance:
        requirements['compliance'] = [c.strip() for c in compliance.split(',') if c.strip()]

    # Hiring priority
    print("\n16. How important is hiring availability? (low/medium/high)")
    hiring = input("    Your answer: ").strip().lower()
    if hiring in ['low', 'medium', 'high']:
        requirements['hiring_priority'] = hiring
    
    # Team expertise
    print("\n17. What languages does your team already know?")
    print("    (comma-separated, e.g., Python, JavaScript, Java)")
    expertise = input("    Your answer: ").strip()
    if expertise:
        requirements['team_expertise'] = [e.strip() for e in expertise.split(',')]

    # Hard constraints
    print("\n18. Must-use languages? (comma-separated, optional)")
    must_use = input("    Your answer: ").strip()
    if must_use:
        requirements['must_use'] = [e.strip() for e in must_use.split(',')]

    print("\n19. Languages to avoid? (comma-separated, optional)")
    avoid = input("    Your answer: ").strip()
    if avoid:
        requirements['avoid'] = [e.strip() for e in avoid.split(',')]
    
    # Analyze and show recommendations
    print("\n\nAnalyzing your requirements...")
    recommender = StackRecommender()
    recommendations = recommender.analyze_requirements(requirements)
    print(recommender.format_recommendation(recommendations))
    
    # Save results
    save = input("\nWould you like to save these recommendations to a file? (yes/no): ").strip().lower()
    if save in ['yes', 'y']:
        filename = input("Enter filename (default: recommendations.json): ").strip() or "recommendations.json"
        result = {
            'requirements': requirements,
            'recommendations': [
                {
                    'rank': idx,
                    'language': STACK_OPTIONS[lang]['name'],
                    'framework': framework,
                    'score': score
                }
                for idx, (lang, score, framework) in enumerate(recommendations, 1)
            ]
        }
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Recommendations saved to {filename}")


def cli_mode(args):
    """Run the recommender with command-line arguments"""
    requirements = {}
    
    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ['--performance', '-p'] and i + 1 < len(args):
            requirements['performance'] = int(args[i + 1])
            i += 2
        elif arg in ['--scalability', '-s'] and i + 1 < len(args):
            requirements['scalability'] = int(args[i + 1])
            i += 2
        elif arg in ['--dev-speed', '-d'] and i + 1 < len(args):
            requirements['development_speed'] = int(args[i + 1])
            i += 2
        elif arg in ['--team-size', '-t'] and i + 1 < len(args):
            requirements['team_size'] = args[i + 1]
            i += 2
        elif arg in ['--project-type', '-pt'] and i + 1 < len(args):
            requirements['project_type'] = args[i + 1]
            i += 2
        elif arg == '--budget' and i + 1 < len(args):
            requirements['budget'] = args[i + 1]
            i += 2
        elif arg == '--deployment' and i + 1 < len(args):
            requirements['deployment'] = args[i + 1]
            i += 2
        elif arg == '--latency-ms' and i + 1 < len(args):
            try:
                requirements['latency_ms'] = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif arg == '--throughput-rps' and i + 1 < len(args):
            try:
                requirements['throughput_rps'] = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif arg == '--data-store' and i + 1 < len(args):
            requirements['data_store'] = args[i + 1]
            i += 2
        elif arg == '--compliance' and i + 1 < len(args):
            requirements['compliance'] = [c.strip() for c in args[i + 1].split(',') if c.strip()]
            i += 2
        elif arg == '--hiring-priority' and i + 1 < len(args):
            requirements['hiring_priority'] = args[i + 1]
            i += 2
        elif arg == '--must-use' and i + 1 < len(args):
            requirements['must_use'] = [c.strip() for c in args[i + 1].split(',') if c.strip()]
            i += 2
        elif arg == '--avoid' and i + 1 < len(args):
            requirements['avoid'] = [c.strip() for c in args[i + 1].split(',') if c.strip()]
            i += 2
        elif arg == '--real-time':
            requirements['real_time'] = True
            i += 1
        elif arg == '--ml-ai':
            requirements['ml_ai'] = True
            i += 1
        elif arg == '--enterprise':
            requirements['enterprise'] = True
            i += 1
        elif arg == '--microservices':
            requirements['microservices'] = True
            i += 1
        elif arg in ['--team-expertise', '-e'] and i + 1 < len(args):
            requirements['team_expertise'] = args[i + 1].split(',')
            i += 2
        else:
            i += 1
    
    if not requirements:
        print("Error: No requirements provided. Use --help for usage information.")
        return
    
    recommender = StackRecommender()
    recommendations = recommender.analyze_requirements(requirements)
    print(recommender.format_recommendation(recommendations))


def show_help():
    """Show help information"""
    help_text = """
Stack Wizard - Backend Stack Recommendation Tool

USAGE:
    python stack_recommender.py [OPTIONS]
    python stack_recommender.py              # Interactive mode (no arguments)

OPTIONS:
    -p, --performance NUM        Performance priority (1-10)
    -s, --scalability NUM        Scalability requirement (1-10)
    -d, --dev-speed NUM          Development speed priority (1-10)
    -t, --team-size SIZE         Team size (small/medium/large)
    -pt, --project-type TYPE     Project type (e.g., api, microservice, webapp)
    --budget LEVEL               Budget sensitivity (low/medium/high)
    --deployment MODEL           Deployment model (serverless/containers/on-prem/edge/hybrid)
    --latency-ms NUM             Target p95 latency in ms
    --throughput-rps NUM         Target throughput (requests per second)
    --data-store TYPE            Data store preference (sql/nosql/mixed)
    --compliance LIST            Compliance requirements (comma-separated)
    --hiring-priority LEVEL      Hiring availability importance (low/medium/high)
    --must-use LIST              Must-use languages (comma-separated)
    --avoid LIST                 Languages to avoid (comma-separated)
    --real-time                  Real-time features required
    --ml-ai                      Machine learning/AI features needed
    --enterprise                 Enterprise application
    --microservices              Microservices architecture
    -e, --team-expertise LANGS   Team expertise (comma-separated languages)
    -h, --help                   Show this help message

EXAMPLES:
    # Interactive mode
    python stack_recommender.py
    
    # API with high performance
    python stack_recommender.py -p 9 -s 8 --project-type api
    
    # Startup MVP with Python expertise
    python stack_recommender.py -d 9 -t small -e Python --project-type webapp
    
    # Enterprise microservices
    python stack_recommender.py -s 9 --enterprise --microservices -t large
    
    # Real-time ML service
    python stack_recommender.py -p 8 --real-time --ml-ai --project-type "ML API"

SUPPORTED LANGUAGES:
    Python, JavaScript (Node.js), Go, Rust, Java, C#, Ruby, Elixir, Scala, C++

For more information, visit: https://github.com/teralad/stack-wizard
"""
    print(help_text)


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            show_help()
        else:
            cli_mode(sys.argv[1:])
    else:
        # Interactive mode
        interactive_mode()


if __name__ == '__main__':
    main()
