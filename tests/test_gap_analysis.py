import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main

def test_gap_analysis_happy():
    user_skills = ["Python", "Docker"]
    job_skills = ["Python", "Docker", "SQL"]
    missing = main.gap_analysis(user_skills, job_skills)
    assert missing == ["sql"]

def test_gap_analysis_edge():
    user_skills = []
    job_skills = ["Python"]
    missing = main.gap_analysis(user_skills, job_skills)
    assert missing == ["python"]

def test_gap_analysis_case_insensitive():
    user_skills = ["python", "DOCKER"]
    job_skills = ["Python", "Docker", "SQL"]
    missing = main.gap_analysis(user_skills, job_skills)
    assert missing == ["sql"]

def test_matched_skills():
    user_skills = ["Python", "Docker"]
    job_skills = ["Python", "Docker", "SQL"]
    matched = main.find_matched_skills(user_skills, job_skills)
    assert set(matched) == {"python", "docker"}