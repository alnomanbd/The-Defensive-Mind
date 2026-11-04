# Labs and Tools

Build a practice SOC, choose tools for production and find good external material. Start with the lab: analysts who have broken and fixed their own SIEM triage faster.

!!! abstract "At a glance"
    - Audience: SOC analyst L1-L3 / SOC engineer / SOC manager
    - Time to read: 3 minutes
    - Outcome: you know which page to open for building a lab, buying a tool or finding training

## Pages in this section

| Page | Use it when | Who |
|---|---|---|
| [Open-source SOC lab](open-source-soc-lab.md) | You want a working SOC stack (SIEM, network sensors, case management, threat intel, automation, forensics) to practise on | Analysts, engineers |
| [Tool selection guide](tool-selection-guide.md) | You must choose or replace a SIEM, EDR, SOAR or case management tool | SOC lead, manager, engineers |
| [Useful resources](useful-resources.md) | You need frameworks, rule repositories, training or communities | Everyone |

## Suggested path by role

| Role | Week 1 | Week 2 | Week 3+ |
|---|---|---|---|
| L1 analyst | Lab phases 1-2 (SIEM + endpoint agent) | Run the lab exercises 1-3 | Practise on free training platforms in [useful resources](useful-resources.md) |
| L2 / L3 analyst | Full lab including network sensors | Write and test a Sigma rule against Atomic Red Team output | Add DFIR collection with Velociraptor |
| SOC engineer | Full lab with Docker Compose | Add automation: alert -> case -> enrichment | Run a proof of concept with the [tool selection guide](tool-selection-guide.md) |
| SOC manager | Read the lab architecture | Use the scoring matrix for the next purchase | Pick training and community resources for the team plan |

!!! warning "Lab safety"
    Keep the lab on an isolated network or a separate virtual network. Attack simulations and malware samples must never reach production or the internet without controls.

## Related pages

- [Templates](../09-templates/index.md)
- [Detection request template](../09-templates/detection-request.md)
- [Change request template](../09-templates/change-request.md)
