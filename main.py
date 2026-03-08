import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")

def load_jobs():
    with open("data/jobs.json", "r") as f:
        return json.load(f)

def get_user_skills():
    skills = input("Enter your skills (comma separated): ")
    return [s.strip().lower() for s in skills.split(",") if s.strip()]

def calculate_match_percentage(user_skills, job_skills):
    if not job_skills:
        return 0
    matched = len(set(user_skills) & set(job_skills))
    return int((matched / len(job_skills)) * 100)

def choose_job(jobs, user_skills):
    print("\nAvailable Jobs:")
    for i, job in enumerate(jobs):
        match_pct = calculate_match_percentage(user_skills, [s.lower() for s in job['skills']])
        print(f"{i + 1}. {job['title']} (Match: {match_pct}%)")
    
    while True:
        try:
            choice = int(input("Select a job number: ")) - 1
            if 0 <= choice < len(jobs):
                return jobs[choice]
            print(f"Please enter a number between 1 and {len(jobs)}")
        except ValueError:
            print("Please enter a valid number")

def gap_analysis(user_skills, job_skills):
    user_skills_lower = set(s.lower() for s in user_skills)
    job_skills_lower = set(s.lower() for s in job_skills)
    return list(job_skills_lower - user_skills_lower)

def find_matched_skills(user_skills, job_skills):
    user_skills_lower = set(s.lower() for s in user_skills)
    job_skills_lower = set(s.lower() for s in job_skills)
    return list(user_skills_lower & job_skills_lower)

# In case the user runs out of credits or Claude is down, 
# the program will list out the learning roadmap in a formulaic order.
def fallback_learning_roadmap(missing_skills):
    roadmap = "Suggested Learning Order:\n"
    for i, skill in enumerate(missing_skills):
        roadmap += f"{i+1}. Learn {skill}\n"
    return roadmap

# Prompt that guides claude to give the learning roadmap with estimate time and proper ordering
def ai_learning_roadmap(user_skills, missing_skills):
    if not ANTHROPIC_API_KEY:
        return fallback_learning_roadmap(missing_skills)
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = f"""
You are a career advisor helping someone transition to a new role.

User's current skills: {', '.join(user_skills)}
Skills needed for target role: {', '.join(missing_skills)}

Create a practical, prioritized learning roadmap with:
1. Optimal learning order (foundational skills first)
2. Estimated time for each skill
3. One recommended free resource per skill

Keep it concise and actionable.
"""
        # latest claude model
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"[Warning] Claude API failed: {e}")
        return fallback_learning_roadmap(missing_skills)

def main():
    print("=== Skill-Bridge Career Navigator ===")
    jobs = load_jobs()
    user_skills = get_user_skills()
    job = choose_job(jobs, user_skills)
    
    matched = find_matched_skills(user_skills, job["skills"])
    missing = gap_analysis(user_skills, job["skills"])

    print(f"\n{'='*50}")
    print(f"Target Role: {job['title']}")
    print(f"{'='*50}")
    
    if matched:
        print(f"\n✓ Skills You Have ({len(matched)}/{len(job['skills'])}):")
        for skill in matched:
            print(f"  • {skill.title()}")
    
    if not missing:
        print("\n🎉 You already meet all listed skills!")
    else:
        print(f"\n⚠ Skills to Acquire ({len(missing)}/{len(job['skills'])}):")
        for skill in missing:
            print(f"  • {skill.title()}")
        
        print("\n" + "="*50)
        print("Learning Roadmap")
        print("="*50 + "\n")
        roadmap = ai_learning_roadmap(user_skills, missing)
        print(roadmap)

if __name__ == "__main__":
    main()