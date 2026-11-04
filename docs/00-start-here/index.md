# Start Here

This section is the front door to the handbook. Read it first if you are new to security operations, new to this handbook, or about to build or rebuild a Security Operations Center (SOC).

!!! abstract "At a glance"
    - Audience: everyone, new analysts, SOC leads, managers, engineers
    - Time to read: 5 minutes for this page, about 90 minutes for the whole section
    - Outcome: you know what a SOC is, how to navigate this handbook, where your career can go, and what the common terms mean

## Pages in this section

| Page | What you get | Read it if... |
|------|--------------|---------------|
| [What is a SOC?](what-is-a-soc.md) | The functions a SOC performs, tiered vs. modern team models, in-house vs. managed vs. hybrid, and what "good" looks like | You need to explain the SOC to someone, or you are deciding how to structure one |
| [How to use this handbook](how-to-use-this-handbook.md) | Reading paths by role, how the sections connect, and how to adapt the content to your organisation | You want to know where to start and what to skip |
| [Career paths](career-paths.md) | Roles from L1 analyst to SOC manager, the skills each needs, vendor-neutral certification examples and 30/60/90-day plans | You are joining a SOC, mentoring someone, or planning your next step |
| [Glossary](glossary.md) | 80+ terms used across SOC, incident response, detection engineering, cloud and threat intelligence | You hit an unfamiliar term anywhere in the handbook |

## How the whole handbook is organised

The handbook follows the life of a SOC: you build it, run it every day, respond when things go wrong, and improve it over time.

| Section | Theme | Typical reader |
|---------|-------|----------------|
| 00 Start here | Orientation and vocabulary | Everyone |
| 01 Build a SOC | Roadmap, operating model, team, technology, budget | SOC lead, manager, Chief Information Security Officer (CISO) |
| 02 Daily operations | Triage, severity, Service Level Agreements (SLAs), shift handover, metrics | Analysts, shift leads |
| 03 Incident response | Lifecycle, roles, communication, evidence | Incident responders, SOC lead |
| 04 Playbooks | Step-by-step response for common attack types | Analysts, responders |
| 05 Detection engineering | Writing, testing and tuning detections | Detection engineers, L2/L3 analysts |
| 06 Threat intelligence | Intel sources, attack surface monitoring, sharing | Intel analysts, hunters |
| 07 Automation and SOAR | Security Orchestration, Automation and Response (SOAR) design | Engineers, SOC lead |
| 08 Security policies | Policy framework that gives the SOC its authority | Managers, governance teams |
| 10 Labs and tools | Hands-on open-source lab to practise everything | Anyone learning |

!!! tip "Fastest useful path"
    If you only have one hour: read [What is a SOC?](what-is-a-soc.md), skim the [Glossary](glossary.md), then jump to [Alert triage](../02-daily-operations/alert-triage.md). That is enough to sit with an analyst on shift and follow what they do.

## Conventions used in every page

- **"At a glance" box** at the top tells you the audience, reading time and outcome.
- **Abbreviations** are spelled out the first time they appear on each page, so any page can be read on its own.
- **Examples** use neutral names: `ACME` for the organisation, `example.com` for domains, `203.0.113.0/24` and `10.0.0.0/8` for addresses.
- **Products** are named only as examples, and every list includes at least one open-source option.
- **Admonitions** carry meaning:

| Box | Meaning |
|-----|---------|
| `tip` | A shortcut or good habit |
| `warning` | A common mistake that costs time or quality |
| `danger` | A mistake that can cause damage, data loss or legal exposure |
| `example` | A worked scenario |
| `note` | Background or nuance |

## Your first day: do these, in this order

| Step | Do | With | Done when |
|------|----|------|-----------|
| 1 | Confirm access to the SIEM, case tool, EDR console and chat channel | Your onboarding ticket | You can log in to all four |
| 2 | Run the five health checks in [What is a SOC?](what-is-a-soc.md) | SIEM search | You know which sources are silent and how old the queue is |
| 3 | Read the last shift handover and the 5 most recent closed cases | Case tool | You can say what normal looks like |
| 4 | Triage 3 low-severity alerts with a senior watching | [Alert triage](../02-daily-operations/alert-triage.md) | Senior agrees with your verdicts |
| 5 | Save the escalation contact list and on-call number | Team wiki | It is on your phone |

!!! warning "Common mistake on day one"
    Closing an alert as "false positive" without writing why. Every closure needs one sentence of evidence, for example: "Login from 203.0.113.10 is the ACME VPN egress, confirmed in asset list."

## Before you move on

- [ ] I can run the silent-log-source query in our SIEM
- [ ] I know which reading path in [How to use this handbook](how-to-use-this-handbook.md) fits my role
- [ ] I have bookmarked the [Glossary](glossary.md)

## Related pages

- [What is a SOC?](what-is-a-soc.md)
- [How to use this handbook](how-to-use-this-handbook.md)
- [Build a SOC, section overview](../01-build-a-soc/index.md)
- [Alert triage](../02-daily-operations/alert-triage.md)
- [Open-source SOC lab](../10-labs-and-tools/open-source-soc-lab.md)
