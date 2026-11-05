# Maturity Model

A simple way to score where your SOC is and decide the next step up. Maturity is not about having more tools; it is about doing the basics reliably, then getting smarter. Use this to set honest targets and show progress.

!!! abstract "At a glance"
    - Audience: SOC manager, CISO
    - Time to read: 10 minutes
    - Outcome: a self-score across the parts of a SOC, and a clear next step for each

!!! tip "Mature means reliable, then smart"
    A level 3 SOC that does triage, response and tuning the same way every day is more valuable than a level 2 SOC with a shiny threat-hunting programme and no consistent queue management. Get reliable first. Add clever last.

## The five levels

| Level | Name | What it looks like |
|---|---|---|
| 1 | Initial | Ad hoc. Someone looks at alerts when they can. No defined process. Detection is whatever the tools ship with |
| 2 | Developing | A named owner, a SIEM, some detections, basic triage. Work is inconsistent and reactive |
| 3 | Defined | Written process for triage, severity, incidents. Daily rhythm. Detections mapped to risk. Metrics reported |
| 4 | Managed | Measured and tuned continuously. Automation for repetitive work. Threat intel applied. Regular hunting |
| 5 | Optimising | Detection as code, purple teaming, proactive hunting, metrics that drive change. Always improving |

Most organisations should aim for a solid **level 3** first. Level 4 and 5 are worth real money only once level 3 is genuinely reliable.

## Score yourself across the parts

Rate each area 1 to 5. The lowest scores show where to invest next.

| Area | Level 1 | Level 3 | Level 5 |
|---|---|---|---|
| People and roles | Whoever is free | Defined roles, a rota, training time | Specialists, strong retention, mentoring |
| Process | None written | Triage, severity, IR runbooks followed daily | Process measured and improved continuously |
| Log coverage | A few sources, gaps unknown | Priority sources onboarded, silence alerted | Broad coverage, gaps tracked against risk |
| Detection | Default rules only | Risk-based, mapped to ATT&CK, tested | Detection as code, versioned, CI-tested |
| Triage and response | Inconsistent | Consistent method, measured times | Automated enrichment and fast containment |
| Metrics | None | Core KPIs reported monthly | Metrics drive detection and staffing decisions |
| Threat intel | None | A feed and a watchlist applied to alerts | Intel shapes detection and hunting |
| Hunting | None | Occasional hunts recorded | Regular, hypothesis-driven, feeds detections |
| Improvement | None | Post-incident reviews held | Purple teaming, measured detection gaps closed |

Plot these and you get an honest shape of your SOC. A line of 3s with one 1 tells you exactly where to spend next.

## Moving up a level

You do not jump levels. You close the lowest gaps.

| From | To | The work |
|---|---|---|
| 1 to 2 | Initial to Developing | Name an owner, stand up a SIEM and EDR, onboard priority logs, write first detections |
| 2 to 3 | Developing to Defined | Write and follow runbooks, run a daily rhythm, map detections to risk, report metrics |
| 3 to 4 | Defined to Managed | Tune continuously, automate the repetitive work, apply threat intel, hunt regularly |
| 4 to 5 | Managed to Optimising | Detection as code, purple teaming, metrics that drive change |

## How to use this honestly

- [ ] Score with evidence, not optimism. "We have a runbook" is not level 3 if nobody follows it.
- [ ] Re-score every quarter and show the trend to leadership.
- [ ] Set the next target as closing your lowest score, not raising your average.
- [ ] Do not chase level 5 features while level 3 basics are shaky.

!!! warning "Maturity theatre"
    It is easy to buy a threat intelligence platform and a hunting tool and claim level 4, while the alert queue goes unworked and detections are untested. Leadership sees tools; attackers see the gaps. Score by what you reliably do, not by what you own.

## Reference models

This is a simplified model for everyday use. For formal assessments, see SOC-CMM (a detailed SOC capability maturity model) and the MITRE and SANS SOC guidance. Use a formal model yearly; use a simple self-score like this one every quarter.

## Related pages

- [Roadmap](roadmap.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
- [Use case prioritization](use-case-prioritization.md)
- [Budget and staffing](budget-and-staffing.md)
