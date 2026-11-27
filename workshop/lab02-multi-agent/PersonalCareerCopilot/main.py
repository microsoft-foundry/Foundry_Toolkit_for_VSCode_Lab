# Copyright (c) Microsoft. All rights reserved.

import json
import logging
import os

from agent_framework import Agent, AgentExecutor, WorkflowBuilder, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

# Load environment variables from .env file (override=True ensures .env wins over shell vars)
load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resume-job-fit")

MICROSOFT_LEARN_MCP_ENDPOINT = os.getenv(
    "MICROSOFT_LEARN_MCP_ENDPOINT", "https://learn.microsoft.com/api/mcp"
)

RESUME_PARSER_INSTRUCTIONS = """\
You are the Resume Parser and Content Router.
Your input contains a resume and usually a job description - BOTH must be preserved.

TASK 1 - Parse the resume into a structured candidate profile.
TASK 2 - Copy the job description verbatim into the pass-through section below.

Output EXACTLY these two labeled sections:

[PARSED RESUME]
1) Candidate Profile
2) Technical Skills (grouped categories)
3) Soft Skills
4) Certifications & Awards
5) Domain Experience
6) Notable Achievements

[JOB DESCRIPTION PASS-THROUGH]
<Copy the complete job description here exactly as given. Do NOT summarize or paraphrase.
If no job description is present, write only: No job description provided.>

Rules:
- Use only explicit or strongly implied evidence for the resume sections.
- Do not invent skills, titles, or experience.
- Keep resume bullets concise; no long paragraphs.
- The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
  Omitting or truncating it breaks the downstream Job Description Agent.
"""

JOB_DESCRIPTION_INSTRUCTIONS = """\
You are the Job Description Analyst and Resume Relay.
Your input is the Resume Parser output. It contains two clearly labeled sections:
  - [PARSED RESUME] - copy this verbatim to [PARSED RESUME PASS-THROUGH] in your output.
  - [JOB DESCRIPTION PASS-THROUGH] - extract the structured JD requirements from here only.

Output EXACTLY these two labeled sections:

[JD REQUIREMENTS]
1) Role Overview
2) Required Skills
3) Preferred Skills
4) Experience Required
5) Certifications Required
6) Education
7) Domain / Industry
8) Key Responsibilities

[PARSED RESUME PASS-THROUGH]
<Copy the complete [PARSED RESUME] section here exactly as given. Do NOT summarize or paraphrase.>

Rules:
- Extract requirements ONLY from [JOB DESCRIPTION PASS-THROUGH] - do not use [PARSED RESUME] content.
- Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
- Keep required vs preferred clearly separated.
- Only use what the JD states; do not invent hidden requirements.
- Flag vague requirements briefly.
- If the JD pass-through says \"No job description provided\", write in [JD REQUIREMENTS]:
  \"No JD available - cannot extract requirements. Ask the user to re-submit with a job description.\"
"""

MATCHING_AGENT_INSTRUCTIONS = """\
You are the Matching Agent.
Your input is the Job Description Analyst output. It contains two clearly labeled sections:
  - [JD REQUIREMENTS] - the structured job requirements; use this as the target profile.
  - [PARSED RESUME PASS-THROUGH] - the candidate's parsed profile; use this as the candidate profile.

Compare [PARSED RESUME PASS-THROUGH] vs [JD REQUIREMENTS] and produce an evidence-based fit report.

Scoring (100 total):
- Required Skills 40
- Experience 25
- Certifications 15
- Preferred Skills 10
- Domain Alignment 10

Output exactly these sections:
1) Fit Score (with breakdown math)
2) Matched Skills
3) Missing Skills
4) Partially Matched
5) Experience Alignment
6) Certification Gaps
7) Overall Assessment

Rules:
- Be objective and evidence-only.
- Keep partial vs missing separate.
- Keep Missing Skills precise; it feeds roadmap planning.
"""

GAP_ANALYZER_INSTRUCTIONS = """\
You are the Gap Analyzer and Roadmap Planner.
Create a practical upskilling plan from the matching report.

Microsoft Learn MCP usage (required):
- For EVERY High and Medium priority gap, call tool `search_microsoft_learn_for_plan`.
- Use returned Learn links in Suggested Resources.
- Prefer Microsoft Learn for free resources.

CRITICAL: You MUST produce a SEPARATE detailed gap card for EVERY skill listed in
the Missing Skills and Certification Gaps sections of the matching report. Do NOT
skip or combine gaps. Do NOT summarize multiple gaps into one card.

Output format:
1) Personalized Learning Roadmap for [Role Title]
2) One DETAILED card per gap (produce ALL cards, not just the first):
   - Skill
   - Priority (High/Medium/Low)
   - Current Level
   - Target Level
   - Suggested Resources (include Learn URL from tool results)
   - Estimated Time
   - Quick Win Project
3) Recommended Learning Order (numbered list)
4) Timeline Summary (week-by-week)
5) Motivational Note

Rules:
- Produce every gap card before writing the summary sections.
- Keep it specific, realistic, and actionable.
- Tailor to candidate's existing stack.
- If fit >= 80, focus on polish/interview readiness.
- If fit < 40, be honest and provide a staged path.
"""


@tool
async def search_microsoft_learn_for_plan(
    skill: str, role: str = "", max_results: int = 5
) -> str:
    """Search Microsoft Learn MCP and return curated official links for roadmap planning."""
    query = " ".join(part for part in [skill, role, "learning path module"] if part).strip()
    query = query or "job skills learning path"

    try:
        async with streamable_http_client(MICROSOFT_LEARN_MCP_ENDPOINT) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(
                    "microsoft_docs_search", {"query": query}
                )

        if not result.content:
            return "No results returned. Fallback: https://learn.microsoft.com/training/support/catalog-api"

        payload_text = getattr(result.content[0], "text", "")
        data = json.loads(payload_text) if payload_text else {}
        items = data.get("results", [])[:max(1, min(max_results, 10))]

        if not items:
            return (
                f"No Microsoft Learn results for '{skill}'. "
                "https://learn.microsoft.com/training/support/integrations-learn-platform-api-catalog-quickstart"
            )

        lines = [f"Microsoft Learn resources for '{skill}':"]
        for i, item in enumerate(items, start=1):
            title = item.get("title") or "Microsoft Learn Resource"
            url = item.get("contentUrl") or item.get("url") or item.get("link") or ""
            lines.append(f"{i}. {title} - {url}".rstrip(" -"))
        return "\n".join(lines)
    except Exception as ex:
        return f"Microsoft Learn MCP unavailable ({ex}). See: https://learn.microsoft.com/api/mcp"


def main():
    logger.info("Starting Resume -> Job Fit Evaluator HTTP server...")

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    resume_parser = Agent(client=client, instructions=RESUME_PARSER_INSTRUCTIONS, name="ResumeParser")
    jd_agent = Agent(client=client, instructions=JOB_DESCRIPTION_INSTRUCTIONS, name="JobDescriptionAgent")
    matching_agent = Agent(client=client, instructions=MATCHING_AGENT_INSTRUCTIONS, name="MatchingAgent")
    gap_analyzer = Agent(
        client=client,
        instructions=GAP_ANALYZER_INSTRUCTIONS,
        name="GapAnalyzer",
        tools=[search_microsoft_learn_for_plan],
    )

    resume_executor = AgentExecutor(resume_parser, context_mode="last_agent")
    jd_executor = AgentExecutor(jd_agent, context_mode="last_agent")
    matching_executor = AgentExecutor(matching_agent, context_mode="last_agent")
    gap_executor = AgentExecutor(gap_analyzer, context_mode="last_agent")

    workflow_agent = (
        WorkflowBuilder(
            start_executor=resume_executor,
            output_executors=[gap_executor],
        )
        .add_edge(resume_executor, jd_executor)
        .add_edge(jd_executor, matching_executor)
        .add_edge(matching_executor, gap_executor)
        .build()
        .as_agent()
    )

    server = ResponsesHostServer(workflow_agent)
    server.run()


if __name__ == "__main__":
    main()
