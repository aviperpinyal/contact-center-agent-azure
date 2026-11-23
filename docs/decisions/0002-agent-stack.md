# ADR 0002: Build the agent with Microsoft Agent Framework on Microsoft Foundry, grounded with Foundry IQ

**Status:** Accepted
**Date:** 2026-11-22

## Context
The agent must answer customer-support questions grounded in a knowledge base,
later call tools (CRM lookup, ticketing), and be evaluated and traced. Microsoft's
agent tooling has been renamed and consolidated several times (Semantic Kernel,
AutoGen, Azure AI Agent Service, Azure AI Foundry), so the choice was checked
against current documentation rather than older tutorials.

## Options considered
1. **Prompt agent defined in the Foundry portal (Foundry Agent Service):** fastest
   start, but the agent definition lives in the portal, not in the repo, so it is
   harder to review, version and test in CI.
2. **Microsoft Agent Framework (Python), code-first, calling the Foundry project
   endpoint:** the agent's instructions, model and tools live in code. Agent
   Framework is the successor to Semantic Kernel and AutoGen (v1.0).
3. **Raw OpenAI SDK against the endpoint:** maximum control, but tool wiring,
   orchestration and session handling would have to be built by hand.

For grounding:
- **Hand-built RAG** (own chunking, embeddings, search queries) vs.
- **Foundry IQ knowledge base** (agentic retrieval on Azure AI Search, with citations).

## Decision
Option 2: Microsoft Agent Framework in Python with `FoundryChatClient` against a
Foundry project. Grounding uses a Foundry IQ knowledge base backed by Azure AI Search.
Deploying the agent as a hosted agent in Foundry Agent Service is deferred to
Milestone 4.

## Consequences
- **Positive:** agent definition is versioned with the code; testable locally and
  in CI; same framework scales to multi-agent workflows (stretch goal); managed
  retrieval with citations instead of custom RAG plumbing.
- **Negative:** Agent Framework and Foundry IQ are young and change quickly, so
  package versions must be pinned and docs re-checked. Less low-level retrieval
  control than hand-built RAG.
- **Cost:** start with a small model and the Azure AI Search Free tier; revisit if
  limits block the knowledge base.



