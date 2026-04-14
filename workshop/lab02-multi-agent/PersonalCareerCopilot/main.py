"""
Resume → Job Fit Evaluator: Multi-Agent Workflow
Uses Microsoft Agent Framework (1.0.0rc3) with Microsoft Foundry.

Agents:
  1. Resume Parser Agent - extracts structured skills/experience from a resume
  2. Job Description Agent - extracts structured requirements from a JD
  3. Matching Agent - computes a fit score and lists missing skills
  4. Gap Analyzer Agent - generates a personalized learning roadmap

SDK pattern: AzureAIAgentClient.as_agent() context-manager (Foundry Agent Service v1)
Hosting: azure-ai-agentserver-agentframework adapter
Ready for deployment to Foundry Hosted Agent service.
"""

import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager

from agent_framework import WorkflowBuilder, tool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential, ManagedIdentityCredential
from dotenv import load_dotenv
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

# override=False so Foundry runtime env vars take precedence over .env
load_dotenv(override=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("resume-job-fit")

# Support both standard Foundry env var names and workshop-specific names
PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT") or os.getenv(
    "PROJECT_ENDPOINT"
)
MODEL_DEPLOYMENT_NAME = os.getenv(
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
)
MICROSOFT_LEARN_MCP_ENDPOINT = os.getenv(
    "MICROSOFT_LEARN_MCP_ENDPOINT", "https://learn.microsoft.com/api/mcp"
)

# ---------------------------------------------------------------------------
# Agent instructions
# ---------------------------------------------------------------------------

RESUME_PARSER_INSTRUCTIONS = """\
You are the Resume Parser.
Extract resume text into a compact, structured profile for downstream matching.

Output exactly these sections:
1) Candidate Profile
2) Technical Skills (grouped categories)
3) Soft Skills
4) Certifications & Awards
5) Domain Experience
6) Notable Achievements

Rules:
- Use only explicit or strongly implied evidence.
- Do not invent skills, titles, or experience.
- Keep concise bullets; no long paragraphs.
- If input is not a resume, return a short warning and request resume text.
"""

JOB_DESCRIPTION_INSTRUCTIONS = """\
You are the Job Description Analyst.
Extract a structured requirement profile from a JD.

Output exactly these sections:
1) Role Overview
2) Required Skills
3) Preferred Skills
4) Experience Required
5) Certifications Required
6) Education
7) Domain / Industry
8) Key Responsibilities

Rules:
- Keep required vs preferred clearly separated.
- Only use what the JD states; do not invent hidden requirements.
- Flag vague requirements briefly.
- If input is not a JD, return a short warning and request JD text.
"""

MATCHING_AGENT_INSTRUCTIONS = """\
You are the Matching Agent.
Compare parsed resume output vs JD output and produce an evidence-based fit report.

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
the Missing Skills and Certification Gaps sections of the matching report.  Do NOT
skip or combine gaps.  Do NOT summarize multiple gaps into one card.

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
            return (
                "No results returned from Microsoft Learn MCP. "
                "Fallback: https://learn.microsoft.com/training/support/catalog-api"
            )

        payload_text = getattr(result.content[0], "text", "")
        data = json.loads(payload_text) if payload_text else {}
        items = data.get("results", [])[: max(1, min(max_results, 10))]

        if not items:
            return (
                f"No direct Microsoft Learn results found for '{skill}'. "
                "Use Learn Catalog API quickstart: "
                "https://learn.microsoft.com/training/support/"
                "integrations-learn-platform-api-catalog-quickstart"
            )

        lines = [f"Microsoft Learn resources for '{skill}':"]
        for i, item in enumerate(items, start=1):
            title = item.get("title") or "Microsoft Learn Resource"
            url = item.get("contentUrl") or item.get("url") or item.get("link") or ""
            lines.append(f"{i}. {title} - {url}".rstrip(" -"))
        return "\n".join(lines)
    except Exception as ex:
        return (
            "Microsoft Learn MCP lookup unavailable. "
            f"Reason: {ex}. "
            "Fallbacks: https://learn.microsoft.com/api/mcp and "
            "https://learn.microsoft.com/training/support/catalog-api"
        )


def get_credential():
    """Use Managed Identity in Azure, otherwise DefaultAzureCredential locally."""
    return (
        ManagedIdentityCredential()
        if os.getenv("MSI_ENDPOINT")
        else DefaultAzureCredential()
    )


@asynccontextmanager
async def create_agents():
    """Create the four agents using the .as_agent() context-manager pattern.

    Each agent gets its own AzureAIAgentClient instance (required by the SDK
    since agent name is scoped to the client).
    """
    async with (
        get_credential() as credential,
        AzureAIAgentClient(
            project_endpoint=PROJECT_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        ).as_agent(
            name="ResumeParser",
            instructions=RESUME_PARSER_INSTRUCTIONS,
        ) as resume_parser,
        AzureAIAgentClient(
            project_endpoint=PROJECT_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        ).as_agent(
            name="JobDescriptionAgent",
            instructions=JOB_DESCRIPTION_INSTRUCTIONS,
        ) as jd_agent,
        AzureAIAgentClient(
            project_endpoint=PROJECT_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        ).as_agent(
            name="MatchingAgent",
            instructions=MATCHING_AGENT_INSTRUCTIONS,
        ) as matching_agent,
        AzureAIAgentClient(
            project_endpoint=PROJECT_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        ).as_agent(
            name="GapAnalyzer",
            instructions=GAP_ANALYZER_INSTRUCTIONS,
            tools=[search_microsoft_learn_for_plan],
        ) as gap_analyzer,
    ):
        yield resume_parser, jd_agent, matching_agent, gap_analyzer


def create_workflow(resume_parser, jd_agent, matching_agent, gap_analyzer):
    """
    Build the multi-agent workflow graph:

        User Input
           │
      ┌────┴────┐
      ▼         ▼
    Resume    Job Description
    Parser      Agent
      └────┬────┘
           ▼
       Matching Agent
           │
           ▼
       Gap Analyzer
           │
           ▼
        Output
    """
    workflow = (
        WorkflowBuilder(
            name="ResumeJobFitEvaluator",
            start_executor=resume_parser,
            output_executors=[gap_analyzer],
        )
        .add_edge(resume_parser, jd_agent)
        .add_edge(resume_parser, matching_agent)
        .add_edge(jd_agent, matching_agent)
        .add_edge(matching_agent, gap_analyzer)
        .build()
    )
    return workflow.as_agent()


def validate_configuration() -> None:
    """Validate required runtime configuration before starting."""
    missing = []
    if not PROJECT_ENDPOINT:
        missing.append("AZURE_AI_PROJECT_ENDPOINT or PROJECT_ENDPOINT")
    if not MODEL_DEPLOYMENT_NAME:
        missing.append("AZURE_AI_MODEL_DEPLOYMENT_NAME or MODEL_DEPLOYMENT_NAME")
    if missing:
        raise RuntimeError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in the workspace .env file or your shell before starting the agent."
        )


async def main() -> None:
    """
    Resume → Job Fit Evaluator multi-agent workflow.

    Usage:
        python main.py          # Server mode (port 8088)
    """
    validate_configuration()

    async with create_agents() as (resume_parser, jd_agent, matching_agent, gap_analyzer):
        agent = create_workflow(resume_parser, jd_agent, matching_agent, gap_analyzer)

        logger.info("Starting Resume → Job Fit Evaluator HTTP server...")
        from azure.ai.agentserver.agentframework import from_agent_framework

        logger.info("Server running on http://localhost:8088")
        await from_agent_framework(agent).run_async()


if __name__ == "__main__":
    asyncio.run(main())
