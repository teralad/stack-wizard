#!/usr/bin/env python3
"""
Tests for the Stack Wizard Recommendation System
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stack_recommender import StackRecommender, STACK_OPTIONS


def get_language_score(recommendations, language):
    """Helper function to get score for a specific language from recommendations"""
    return next((score for lang, score, _ in recommendations if lang == language), 0)


def test_performance_priority():
    """Test that high-performance requirements favor compiled languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 10,
        'scalability': 5,
        'development_speed': 5
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]
    
    # Top recommendation should be a high-performance language
    assert top_lang in ['rust', 'cpp', 'go', 'java', 'csharp'], \
        f"Expected high-performance language, got {top_lang}"
    
    print("✓ Performance priority test passed")


def test_ml_ai_requirements():
    """Test that ML/AI requirements strongly favor Python"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'ml_ai': True,
        'project_type': 'ML API'
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]
    
    assert top_lang == 'python', \
        f"Expected Python for ML/AI, got {top_lang}"
    
    print("✓ ML/AI requirements test passed")


def test_rapid_development():
    """Test that rapid development favors dynamic languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 3,
        'scalability': 4,
        'development_speed': 10,
        'team_size': 'small'
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]
    
    # Top should be a rapid development language
    assert top_lang in ['python', 'ruby', 'javascript'], \
        f"Expected rapid development language, got {top_lang}"
    
    print("✓ Rapid development test passed")


def test_enterprise_requirements():
    """Test that enterprise requirements favor enterprise-ready languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 6,
        'scalability': 9,
        'development_speed': 5,
        'team_size': 'large',
        'enterprise': True,
        'microservices': True
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]
    
    # Should favor enterprise languages
    assert top_lang in ['java', 'csharp', 'scala', 'go', 'javascript'], \
        f"Expected enterprise language, got {top_lang}"
    
    print("✓ Enterprise requirements test passed")


def test_real_time_requirements():
    """Test that real-time requirements favor appropriate languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 7,
        'scalability': 8,
        'development_speed': 6,
        'real_time': True,
        'project_type': 'chat application'
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]
    
    # Should favor real-time capable languages
    assert top_lang in ['elixir', 'javascript', 'go'], \
        f"Expected real-time language, got {top_lang}"
    
    print("✓ Real-time requirements test passed")


def test_team_expertise_bonus():
    """Test that team expertise provides significant bonus"""
    recommender = StackRecommender()
    
    # Without expertise
    requirements1 = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
    }
    recommendations1 = recommender.analyze_requirements(requirements1)
    
    # With Ruby expertise (not typically high-scoring)
    requirements2 = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'team_expertise': ['Ruby']
    }
    recommendations2 = recommender.analyze_requirements(requirements2)
    
    # Find Ruby's rank in both using helper
    ruby_score1 = get_language_score(recommendations1, 'ruby')
    ruby_score2 = get_language_score(recommendations2, 'ruby')
    
    assert ruby_score2 > ruby_score1, \
        "Team expertise should boost score"
    
    print("✓ Team expertise bonus test passed")



def test_framework_recommendations():
    """Test that framework recommendations are appropriate"""
    recommender = StackRecommender()
    
    # API project should get FastAPI for Python
    requirements = {
        'performance': 7,
        'project_type': 'API',
        'development_speed': 7
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    
    # Find Python recommendation
    python_rec = next((rec for rec in recommendations if rec[0] == 'python'), None)
    
    if python_rec:
        framework = python_rec[2]
        assert framework in ['FastAPI', 'Flask'], \
            f"Expected FastAPI or Flask for API project, got {framework}"
    
    print("✓ Framework recommendation test passed")


def test_balanced_requirements():
    """Test with balanced, moderate requirements"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'team_size': 'medium'
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    
    # Should get all recommendations by default
    assert len(recommendations) == len(STACK_OPTIONS), \
        f"Expected {len(STACK_OPTIONS)} recommendations, got {len(recommendations)}"
    
    # All should have positive scores
    for _, score, _ in recommendations:
        assert score > 0, "All recommendations should have positive scores"
    
    # Scores should be in descending order
    scores = [score for _, score, _ in recommendations]
    assert scores == sorted(scores, reverse=True), \
        "Recommendations should be sorted by score"
    
    print("✓ Balanced requirements test passed")


def test_all_languages_present():
    """Test that all languages can be recommended in some scenario"""
    recommender = StackRecommender()
    all_languages_seen = set()
    
    # Test various scenarios
    scenarios = [
        {'performance': 10, 'scalability': 8},  # High performance
        {'development_speed': 10, 'team_size': 'small'},  # Rapid dev
        {'enterprise': True, 'team_size': 'large'},  # Enterprise
        {'ml_ai': True, 'performance': 8},  # ML
        {'real_time': True, 'scalability': 8},  # Real-time
        {'performance': 10, 'scalability': 10, 'development_speed': 2},  # Max performance
    ]
    
    for scenario in scenarios:
        recommendations = recommender.analyze_requirements(scenario)
        for lang, _, _ in recommendations:
            all_languages_seen.add(lang)
    
    # Check if we've seen most languages
    assert len(all_languages_seen) >= 8, \
        f"Expected to see at least 8 languages across scenarios, saw {len(all_languages_seen)}"
    
    print(f"✓ All languages test passed (saw {len(all_languages_seen)}/10 languages)")


def test_score_ranges():
    """Test that scores are within reasonable ranges"""
    recommender = StackRecommender()
    
    # Extreme high requirements
    requirements = {
        'performance': 10,
        'scalability': 10,
        'development_speed': 10,
        'team_size': 'large',
        'enterprise': True,
        'microservices': True,
        'real_time': True
    }
    
    recommendations = recommender.analyze_requirements(requirements)
    
    # Top score should be substantial
    top_score = recommendations[0][1]
    assert top_score > 30, \
        f"Expected high score for extreme requirements, got {top_score}"
    
    print("✓ Score ranges test passed")


def test_must_use_filtering():
    """Test that must-use languages constrain recommendations"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'must_use': ['Rust']
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang == 'rust', \
        f"Expected Rust due to must-use constraint, got {top_lang}"

    print("✓ Must-use filtering test passed")


def test_avoid_filtering():
    """Test that avoid list removes languages from recommendations"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'avoid': ['python']
    }

    recommendations = recommender.analyze_requirements(requirements)
    languages = [lang for lang, _, _ in recommendations]

    assert 'python' not in languages, \
        "Expected python to be excluded by avoid list"

    print("✓ Avoid filtering test passed")


def test_latency_throughput_bias():
    """Test that tight latency/high throughput favors high-perf languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 7,
        'scalability': 8,
        'development_speed': 4,
        'latency_ms': 80,
        'throughput_rps': 20000
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang in ['rust', 'cpp', 'go'], \
        f"Expected low-latency/high-throughput language, got {top_lang}"

    print("✓ Latency/throughput bias test passed")


def test_deployment_serverless_bias():
    """Test that serverless deployment favors supported languages"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 6,
        'deployment': 'serverless'
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang in ['python', 'javascript', 'go'], \
        f"Expected serverless-friendly language, got {top_lang}"

    print("✓ Deployment model bias test passed")


def test_compliance_bonus():
    """Test that compliance + enterprise favors Java/C#"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 7,
        'development_speed': 4,
        'team_size': 'large',
        'enterprise': True,
        'compliance': ['HIPAA']
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang in ['java', 'csharp'], \
        f"Expected compliance/enterprise language, got {top_lang}"

    print("✓ Compliance bonus test passed")


def test_unknown_must_use_fallback():
    """Test that unknown must-use languages fall back to full set"""
    recommender = StackRecommender()
    requirements = {
        'performance': 5,
        'scalability': 5,
        'development_speed': 5,
        'must_use': ['kotlin']
    }

    recommendations = recommender.analyze_requirements(requirements)
    assert len(recommendations) == len(STACK_OPTIONS), \
        "Expected fallback to full recommendations when must-use misses"
    assert recommender.requirements.get('constraint_miss') is True, \
        "Expected constraint_miss flag when must-use doesn't match"

    print("✓ Unknown must-use fallback test passed")


def test_scraping_parallel_bias():
    """Test that scraping/parallel wording favors Go/Elixir"""
    recommender = StackRecommender()
    requirements = {
        'performance': 8,
        'scalability': 7,
        'development_speed': 4,
        'project_type': 'scraping several websites in parallel'
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang in ['go', 'elixir'], \
        f"Expected Go or Elixir for scraping/parallel, got {top_lang}"

    print("✓ Scraping/parallel bias test passed")


def test_io_bound_bias():
    """Test that IO-bound flag favors Go/Elixir"""
    recommender = StackRecommender()
    requirements = {
        'performance': 8,
        'scalability': 7,
        'development_speed': 4,
        'io_bound': True
    }

    recommendations = recommender.analyze_requirements(requirements)
    top_lang = recommendations[0][0]

    assert top_lang in ['go', 'elixir'], \
        f"Expected Go or Elixir for IO-bound, got {top_lang}"

    print("✓ IO-bound bias test passed")


def run_all_tests():
    """Run all test functions"""
    print("\n" + "="*60)
    print("Running Stack Recommender Tests")
    print("="*60 + "\n")
    
    tests = [
        test_performance_priority,
        test_ml_ai_requirements,
        test_rapid_development,
        test_enterprise_requirements,
        test_real_time_requirements,
        test_team_expertise_bonus,
        test_framework_recommendations,
        test_balanced_requirements,
        test_all_languages_present,
        test_score_ranges,
        test_must_use_filtering,
        test_avoid_filtering,
        test_latency_throughput_bias,
        test_deployment_serverless_bias,
        test_compliance_bonus,
        test_unknown_must_use_fallback,
        test_scraping_parallel_bias,
        test_io_bound_bias
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} errored: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
