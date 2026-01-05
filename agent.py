from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from text_extractor import extract_text_from_pdf
import os
import json
import re
import glob

load_dotenv()

file_path = r"D:\AI Projects\ReadyMinds\Auto-Jobs-Bot\resumes\TanmayBuradkarResume.pdf"

json_path = os.path.basename(file_path).replace(".pdf", ".json")

text = extract_text_from_pdf(file_path)

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
)

resume_analyzer_agent = Agent(
    role="Resume Analyzer",
    goal="Extract structured job-relevant information from resume text and produce strict JSON.",
    llm=llm,
    backstory="""
You are an expert recruiter and parser. Only return valid JSON strictly following schema.
Do not include explanations or additional text.
""",
    verbose=False,
)


resume_analysis_task = Task(
    description=f"""
You MUST return ONLY a valid JSON object.
NO markdown, NO explanations, NO comments.

Rules:
- If a field is missing, return null.
- experience_years must be a NUMBER.
- skills must be normalized (e.g., "Python", "FastAPI", "LLMs").
- search_keywords must be optimized for job portals (LinkedIn, Indeed).

JSON Schema:
{{
  "role": string | null,
  "skills": [string],
  "experience_years": number | null,
  "seniority": "Intern" | "Junior" | "Mid" | "Senior" | null,
  "preferred_location": string | null,
  "search_keywords": [string]
}}

Resume Text:
{text}
""",
    agent=resume_analyzer_agent,
    expected_output="""
A JSON object strictly following the provided schema with fields role, skills,
experience_years, seniority, preferred_location, and search_keywords.
""",
)

crew = Crew(agents=[resume_analyzer_agent], tasks=[resume_analysis_task])


results = crew.kickoff()


raw_output = results.raw

json_str = re.search(r"\{.*\}", raw_output, re.DOTALL).group()
parsed_output = json.loads(json_str)
print(json.dumps(parsed_output, indent=2))

with open(rf"resumes_jsons/{json_path}", "w") as f:
    json.dump(parsed_output, f, indent=2)
