---
id: GOV-11
title: AI Use in the SOC Policy
owner: CISO
audience: SOC team, and anyone using AI tools for SOC work
review: Every 6 months (this field moves fast)
summary: Which AI tools the SOC may use, what data may be given to them, and the rule that a human stays in control of every decision and action. It lets the SOC use AI safely instead of banning or misusing it.
---
## 1. Purpose

Artificial intelligence (AI), especially large language models (LLMs), can speed up SOC work: summarising, drafting queries, enriching, suggesting next steps. It can also be confidently wrong, be manipulated, and leak data. This policy lets the SOC of [ORGANISATION] use AI usefully while keeping humans in control and data protected.

> WARNING: AI in the SOC assists; it does not decide. Treat AI output as a lead to verify, never a verdict to act on. A human approves every decision and every action that matters.

## 2. Scope

All use of AI tools by the SOC for security work: assistants, copilots, AI features in SOC tools, and any AI agents or automations the SOC builds.

## 3. Approved tools

- [ ] Only AI tools on the approved list in [location] may be used for SOC work.
- [ ] The approved list records, for each tool: what it may be used for, what data it may receive, and where that data goes.
- [ ] A new AI tool is assessed and approved by [role] before use, including where it sends data and how that data is handled.

## 4. What data may be given to AI

This is the heart of the policy. The risk is leaking sensitive data to a third-party service.

| Data | Allowed? |
|---|---|
| Public or non-sensitive technical data (a public IP, a generic query) | Yes, to approved tools |
| Internal security data (alert details, logs, case notes) | Only to approved tools that keep the data private and do not train on it, per the approved list |
| Personal data | Only where the tool and the use are approved for it, following the Privacy policy (GOV-10) |
| Secrets, credentials, keys | Never |
| Another person's private content without authority | Never |

- [ ] Do not paste secrets, credentials, or another person's private data into any AI tool.
- [ ] Do not upload confidential files to a public AI service; use the approved tools and their agreed data handling.

## 5. Human in the loop

- [ ] AI may enrich, summarise, draft and suggest. A human verifies before relying on it.
- [ ] AI must not take a business-affecting action (disable an account, isolate a host, block, send a message) without a human approving that action.
- [ ] AI-drafted conclusions in a case are checked against the evidence before they stand.
- [ ] AI-drafted communications to people outside the SOC are reviewed by a human before sending.

## 6. AI agents and automations

Where the SOC builds an AI agent or automation:

- [ ] It follows the SOAR principles: automate enrichment freely, keep action behind human approval.
- [ ] Its actions are logged and reversible.
- [ ] Its access and credentials are limited and protected.
- [ ] Its accuracy is measured; if it is unreliable, it is turned off and fixed.

## 7. Accountability

The analyst using AI remains responsible for the result. "The AI said so" is not a defence for a wrong action. AI changes how fast the work is done, not who is accountable for it.

## 8. Review

Reviewed every 6 months, because AI capability and risk change quickly.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
