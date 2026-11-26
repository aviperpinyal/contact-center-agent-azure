


"""Milestone 1, Step 3: first agent run against the Foundry project (no grounding yet)."""

import asyncio
import os
import sys

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Read FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL from .env
load_dotenv()

INSTRUCTIONS = (
    "You are a customer support agent for a fictional home automation managed service provider. "
    "Be brief and polite. If you don't know something, say so."
)


async def main() -> None:
    question = " ".join(sys.argv[1:]) or "Hi, what can you help me with?"

    agent = Agent(
        client=FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=AzureCliCredential(),  # uses your `az login`, no keys
        ),
        instructions=INSTRUCTIONS,
    )
    

    print(f"Customer: {question}")
    result = await agent.run(question)
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())