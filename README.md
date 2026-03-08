Candidate Name: Harish Varadarajan

Scenario Chosen: Skill-Bridge Career Navigator

Estimated Time Spent: 5 hours

Quick Start:

Prerequisites: 

- pip install -r requirements.txt

If you recieve an error saying it cannot find the module anthropic, 
it is likely that the command did not download the package in the correct place.

Try creating a virtual environment if that is the case.

- create a .env file
- in the env file, enter:
 - CLAUDE_API_KEY={YOUR_API_KEY}


Run Commands: 

To run, enter:
- python main.py

You have to run it with the terminal, some editors like vscode do not allow you to respond to the input() statements.

If it works, you will see a prompt in the terminal, which you can use to interact with the whole program.

Test Commands:

You can test gap analysis using the command:
- pytest tests/

AI Disclosure:

Did you use an AI assistant (Copilot, ChatGPT, etc.)? 
- No

How did you verify suggestions? 

- We validated the output by comparing suggested skills to the known missing skills from the gap analysis, ensuring the roadmap was logical and practical

Example of a suggestion rejected or changed: 
- If Claude suggested skills unrelated to the selected job or the API call fails, the program defaults to the fallback roadmap for that skill

Tradeoffs and Prioritization:

What did you cut to stay within 4–6 hours?

- The program uses a CLI interface only instead of building a full web UI.

- AI integration is limited to one use case (learning roadmap generation) rather than multiple features like dynamic mock interviews.

- Limited input validation and edge case handling beyond basic checks (e.g., no advanced natural language parsing for skills).

What would you build next if you had more time?

- Add a web-based interface with better interactivity and dashboards.

- Integrate real job board data to dynamically update available jobs.

- Expand AI functionality: generate mock interview questions, provide skill-level assessment, or include course links with completion times.

- Add unit tests for all edge cases and expand test coverage.

Known limitations:

- Learning roadmap depends on Claude API; fallback is deterministic but simple.

- CLI-only interface — no GUI, limited visual feedback.

Video Link: https://youtu.be/s3UIl5fVmB0
