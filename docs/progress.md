# Progress Log

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 0 | Define & set up | ✅ Done |
| 1 | First working agent: grounded answers from a knowledge base | ✅ Done |
| 2 | Tools: agent calls 2+ tools and completes a task end to end | ⏳ Next |
| 3 | Evaluate & observe: eval set with scores, tracing | |
| 4 | Harden: safety, error handling, deploy from scratch with IaC | |
| 5 | Publish: README, architecture diagram, demo video | |

---

## 2026-11-26 — Milestone 1: First working agent

**Use case refined** ([ADR 0003](decisions/0003-use-case-home-automation.md)): a support agent for
Contoso Home Services, a fictional home automation managed service provider.

**Done**
- [ADR 0002](decisions/0002-agent-stack.md): Microsoft Agent Framework (code-first) on Microsoft
  Foundry, grounded with a Foundry IQ knowledge base on Azure AI Search
- Microsoft Foundry resource and project; `gpt-5.4-mini` (chat) and `text-embedding-3-small`
  (embeddings) deployments with low rate limits as a cost control
- Baseline ungrounded agent (`src/hello_agent.py`): it didn't invent prices, but it invented a
  capability and a support process — the "before" picture for grounding
- Synthetic knowledge base: 8 support documents designed for evaluation (checkable facts,
  facts spanning documents, safety cases, deliberate gaps)
- Azure AI Search (Free tier) + Blob Storage + Foundry IQ knowledge source and knowledge base,
  created by `scripts/setup_knowledge_base.py` (idempotent)
- **Keyless end to end:** Entra ID for the app; the Search service's managed identity reads
  Blob Storage and calls the models, with least-privilege roles
- Grounded support agent (`src/support_agent.py`): the model decides when to call the
  knowledge-base tool, answers only from retrieved passages, cites sources, keeps multi-turn
  context, follows safety-first and hard-limit rules

**Results**
- Ingestion: 8 documents, 0 failures, about 5 seconds
- Agentic retrieval: LLM query planning (~1 s) and 3 parallel sub-queries per question
- For "Does alarm monitoring keep working if my home internet goes down?", the three relevant
  passages scored 3.0–3.7 (semantic reranker, 0–4) and the rest 1.3–1.6. No cutoff is set yet;
  the threshold will be tuned against the Milestone 3 evaluation set

**Issues found and fixed**
- The primary region was out of Azure AI Search capacity; placed Search in a neighboring US region
  with the same features
- Docs suggested the Free tier doesn't support managed identity; tested it instead of assuming —
  it works, so the pipeline stayed keyless
- Red-teaming: Azure's default content filter blocked a harmful question (the platform safety layer
  working), but the app crashed. Added graceful handling that logs the event and keeps the
  conversation going
- A duplicated answer in the output: the response held the final text twice; the app now shows
  only the last answer

**Open / next**
- Ambiguous follow-ups ("that level of redundancy" with no prior context) are answered by inference;
  add a clarifying-question rule and an eval case
- Decide conversation retention: the Responses API stores turns server-side by default (Milestone 4)
- **Next:** Milestone 2 — tools (hub/device status, callback booking, human hand-off with summary)

---

## 2026-11-22 — Milestone 0: Define & set up

**Use case:** a contact-center support agent that looks up the customer, checks
service status, answers from a knowledge base, takes an action (ticket or callback)
and escalates to a human with a summary when confidence is low.

**Done**
- Repository created (MIT license, Python `.gitignore`)
- Reproducible dev environment: GitHub Codespaces + dev container
  (Python 3.12, Azure CLI with Bicep, Azure Developer CLI, GitHub CLI, Git LFS)
- [ADR 0001](decisions/0001-dev-environment.md): Codespaces with a dev container
- Azure: signed in from the dev container; dedicated resource group with
  naming convention and tags (project, environment, owner)

**Issues found and fixed**
- The unpinned base image moved to Debian 13, where Microsoft's Azure CLI packages
  aren't published, so the CLI fell back to an old, partly broken version.
  Fixed by pinning the image to Debian 12 (`python:3.12-bookworm`).
- Git LFS hooks blocked `git push` because `git-lfs` wasn't installed. Fixed by
  adding the Git LFS dev container feature.

**Cost controls:** spending approved by the environment owner; lowest-cost tiers,
low model rate limits and teardown when idle.
