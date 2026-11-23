# Progress Log

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| 0 | Define & set up | ✅ Done (budget alert pending, see notes) |
| 1 | First working agent: grounded answers from a knowledge base | ⏳ Next |
| 2 | Tools: agent calls 2+ tools and completes a task end to end | |
| 3 | Evaluate & observe: eval set with scores, tracing | |
| 4 | Harden: safety, error handling, deploy from scratch with IaC | |
| 5 | Publish: README, architecture diagram, demo video | |

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

**Open**
- Budget alert: cost visibility is restricted in the current lab subscription
  (managed at the billing level). Requested; meanwhile using compensating
  controls: lowest-cost tiers, teardown when idle, usage-based alerts on the model.

**Next:** Milestone 1. Pick the agent framework, deploy a model, index a small
knowledge base in Azure AI Search, and get grounded answers.

