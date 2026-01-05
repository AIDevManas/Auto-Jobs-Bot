from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from text_extractor import extract_text_from_pdf
import os


load_dotenv()

text = extract_text_from_pdf("03_Professional CV Resume Template.pdf")

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
You MUST output ONLY valid JSON and nothing else.

Required JSON schema:
{{
        "role": string | null,
  "skills": [string],
  "experience_years": number | null,
  "seniority": "Intern" | "Junior" | "Mid" | "Senior" | null,
  "preferred_location": string | null,
  "search_keywords": [string]
}}

Here is the resume text:

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
print(results)
