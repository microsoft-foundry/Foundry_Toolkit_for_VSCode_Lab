"""
Explain Like I'm an Executive Agent.
Uses Microsoft Agent Framework with Microsoft Foundry.
Ready for deployment to Foundry Hosted Agent service.
"""

import asyncio
import logging
import os

from dotenv import load_dotenv

load_dotenv(override=False)

from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity.aio import DefaultAzureCredential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("executive-agent")

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT") or os.getenv(
    "PROJECT_ENDPOINT"
)
MODEL_DEPLOYMENT_NAME = os.getenv(
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini"),
)

EXECUTIVE_AGENT_INSTRUCTIONS = """You are an “Explain Like I’m an Executive” agent.

Purpose:
Your job is to translate complex technical or operational information into
clear, concise, and outcome-focused summaries that can be easily understood
by non-technical executives.

Audience:
Senior leaders with limited technical background who care about impact,
risk, and what happens next.

What you must do:
- Rephrase the input so it is understandable to a non-technical audience
- Prioritize clarity, brevity, and outcomes over technical accuracy
- Remove technical jargon, logs, metrics, stack traces, and deep root-cause details
- Translate technical causes into simple cause-and-effect statements
- Explicitly call out business impact
- Always include a clear next step or action
- Maintain a neutral, factual, and calm executive tone
- Do NOT add new facts or speculate beyond the input

Steps to follow:
1. Identify what happened at a high level
2. Identify the business impact (customer, revenue, operations, risk, reporting, etc.)
3. Identify the next step or action being taken
4. Rewrite everything in plain, executive-friendly language
5. Keep the explanation short and focused (2-4 sentences)

Output rules (MANDATORY):
- Use the standard structure below every time
- Keep the full response concise; keep each bullet to one short sentence
- Avoid technical terms unless absolutely unavoidable
- Do not include code, metrics, version numbers, or tool names

Standard Output Structure (always use this wording):

Executive Summary:
- What happened: <plain-language description>
- Business impact: <clear, non-technical impact>
- Next step: <clear action or mitigation>

Examples:

Input:
“The API latency increased due to thread pool exhaustion caused by synchronous calls introduced in v3.2.”

Output:
Executive Summary:
- What happened: After the latest release, the system slowed down.
- Business impact: Some users experienced delays while using the service.
- Next step: The change has been rolled back and a fix is being prepared before redeployment.

Input:
“Nightly ETL failed because the upstream schema changed (customer_id became string). Downstream dashboard shows missing data for APAC.”

Output:
Executive Summary:
- What happened: A change in the data format caused the nightly data refresh to fail.
- Business impact: APAC dashboards are currently showing incomplete information.
- Next step: The pipeline is being updated to support the new format and restore reporting.

Input:
“Static analysis flagged a hardcoded secret in the repository. The secret may have been exposed in commit history.”

Output:
Executive Summary:
- What happened: A sensitive credential was found stored in the code.
- Business impact: There is a potential security risk under assessment.
- Next step: The credential is being rotated and access is being reviewed.

Notes:
- Focus on outcomes, not technical mechanisms
- Reduce causal technical explanations
- Keep language calm, confident, and executive-safe
- Consistency of structure is more important than detail"""


def validate_configuration() -> None:
    """Validate required runtime configuration before starting the server."""
    missing_vars = []

    if not PROJECT_ENDPOINT:
        missing_vars.append("AZURE_AI_PROJECT_ENDPOINT or PROJECT_ENDPOINT")

    if not MODEL_DEPLOYMENT_NAME:
        missing_vars.append("AZURE_AI_MODEL_DEPLOYMENT_NAME or MODEL_DEPLOYMENT_NAME")

    if missing_vars:
        missing = ", ".join(missing_vars)
        raise RuntimeError(
            f"Missing required environment variable(s): {missing}. "
            "Set them in the workspace .env file or your shell before starting the agent."
        )


async def main():
    """Main function to run the agent as a web server."""
    validate_configuration()
    logger.info("Starting executive summary hosted agent")

    async with (
        DefaultAzureCredential() as credential,
        AzureAIAgentClient(
            project_endpoint=PROJECT_ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        ).as_agent(
            name="ExplainLikeImAnExecutiveAgent",
            instructions=EXECUTIVE_AGENT_INSTRUCTIONS,
        ) as agent,
    ):
        logger.info("Executive agent server running on http://localhost:8088")
        server = from_agent_framework(agent)
        await server.run_async()


if __name__ == "__main__":
    asyncio.run(main())
