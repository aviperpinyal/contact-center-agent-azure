# ADR 0001: Use GitHub Codespaces with a dev container

**Status:** Accepted
**Date:** 2026-11-22

## Context
The project needs Python, Azure CLI, Bicep, Azure Developer CLI (azd) and GitHub CLI.
Installing these locally was unreliable: the local machine is an Intel Mac, and
Homebrew no longer provides pre-built packages for Intel macOS, so tools compile
from source (slow and fragile). Anyone else who clones the repo would face their
own local setup differences.

## Options considered
1. **Local install with Homebrew:** unsupported on Intel macOS; slow source builds.
2. **Local install with each vendor's installer:** works, but every machine drifts
   and reviewers must repeat the setup.
3. **GitHub Codespaces + dev container:** environment defined in
   `.devcontainer/devcontainer.json`, built the same way every time.

## Decision
Use GitHub Codespaces with a dev container based on
`mcr.microsoft.com/devcontainers/python:3.12-bookworm`, adding Azure CLI (with Bicep),
azd, GitHub CLI and Git LFS as dev container features.

## Consequences
- **Positive:** reproducible environment; anyone can open the repo in Codespaces
  and get a working setup in minutes; no dependence on local hardware.
- **Negative:** needs internet access; Codespaces usage is billed after the free
  monthly allowance (mitigated with a 30-minute idle timeout).
- **Lesson learned:** the unpinned `python:3.12` image moved to Debian 13 (Trixie),
  which Microsoft's Azure CLI packages don't support yet, so the CLI fell back to
  an old, partly broken version. Pinning the OS release (`-bookworm`) fixed it.
  Pin base images explicitly.