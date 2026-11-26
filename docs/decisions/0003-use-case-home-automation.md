# ADR 0003: Support agent for a home automation managed service provider

**Status:** Accepted
**Date:** 2026-11-26

## Context
Milestone 0 chose a contact-center customer-support agent, with a telecom/ISP
provider in mind. While building the first agent, the domain was reconsidered.
The agent pattern stays the same (customer lookup, status checks, grounded answers,
actions, escalation to a human); only the business it supports changes.

## Options considered
1. **Telecom / internet provider support:** a very common demo scenario; maps to
   contact-center experience.
2. **Home automation managed service provider:** support for a company that
   installs and manages smart home systems (hub, sensors, cameras, alarm
   monitoring). Less common, and builds on hands-on smart home experience.

## Decision
Option 2. The agent supports customers of **Contoso Home Services**, a fictional
home automation managed service provider. The knowledge base (`data/kb/`) is
synthetic and covers plans, alarm monitoring, hub and device troubleshooting,
outages and credits, support hours and escalation, billing, and video privacy.

## Consequences
- **Positive:** a distinctive scenario; realistic safety and escalation cases
  (alarms, emergencies, passcodes) that are good material for Responsible AI and
  evaluation work; natural tools for Milestone 2 (hub/device status, callback
  requests).
- **Negative:** the domain includes safety-critical topics, so the agent must
  route emergencies to 911 and humans reliably. This raises the bar for
  instructions and evaluation.
- **Unchanged:** the contact-center pattern, the agent stack (ADR 0002) and the
  milestone plan.
