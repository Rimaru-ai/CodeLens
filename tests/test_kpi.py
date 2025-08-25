import pytest
from app import calculate_code_health, generate_insights

def test_calculate_code_health_good_code():
    metrics = {
        "bugs": "0",
        "code_smells": "5",
        "coverage": "85",
        "duplicated_lines_density": "2"
    }
    score = calculate_code_health(metrics)
    assert score > 70  # should be relatively high

def test_calculate_code_health_bad_code():
    metrics = {
        "bugs": "20",
        "code_smells": "200",
        "coverage": "20",
        "duplicated_lines_density": "25"
    }
    score = calculate_code_health(metrics)
    assert score < 40  # should be low

def test_generate_insights_low_coverage():
    metrics = {
        "bugs": "1",
        "code_smells": "5",
        "coverage": "30",
        "duplicated_lines_density": "5"
    }
    insights = generate_insights(metrics)
    assert any("coverage" in msg.lower() for msg in insights)

def test_generate_insights_high_bugs_and_duplication():
    metrics = {
        "bugs": "15",
        "code_smells": "10",
        "coverage": "70",
        "duplicated_lines_density": "20"
    }
    insights = generate_insights(metrics)
    assert any("bugs" in msg.lower() for msg in insights)
    assert any("duplication" in msg.lower() for msg in insights)

def test_generate_insights_good_code():
    metrics = {
        "bugs": "0",
        "code_smells": "0",
        "coverage": "95",
        "duplicated_lines_density": "0"
    }
    insights = generate_insights(metrics)
    assert "looks good" in insights[0].lower()
