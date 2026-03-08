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
    return [s.strip() for s in skills.split(",") if s.strip()]

def choose_job(jobs):
    print("\nAvailable Jobs:")
    for i, job in enumerate(jobs):
        print(f"{i + 1}. {job['title']}")
    choice = int(input("Select a job number: ")) - 1
    return jobs[choice]

def gap_analysis(user_skills, job_skills):
    return list(set(job_skills) - set(user_skills))

# In case the user runs out of credits or Claude is down, 
# the program will list out the learning roadmap in a formulaic order.
def fallback_learning_roadmap(missing_skills):
    roadmap = "Suggested Learning Order:\n"
    for i, skill in enumerate(missing_skills):
        roadmap += f"{i+1}. Learn {skill}\n"
    return roadmap

def ai_learning_roadmap(user_skills, missing_skills):
    if not ANTHROPIC_API_KEY:
        return fallback_learning_roadmap(missing_skills)
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = f"""
User skills: {user_skills}
Missing skills: {missing_skills}

Generate a short and practical learning roadmap to acquire the missing skills.
"""
        # current stable claude model
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
    job = choose_job(jobs)
    missing = gap_analysis(user_skills, job["skills"])

    print(f"\nTarget Role: {job['title']}")
    if not missing:
        print("You already meet all listed skills!")
    else:
        print("\nMissing Skills:")
        for skill in missing:
            print(f"- {skill}")

    print("\nLearning Roadmap:\n")
    roadmap = ai_learning_roadmap(user_skills, missing)
    print(roadmap)

if __name__ == "__main__":
    main()