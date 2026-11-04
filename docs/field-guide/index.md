# SOC Field Guide

This section shows how a Security Operations Centre (SOC) actually works, hour by hour, role by role. Pick your role, follow the day, copy the queries.

!!! abstract "At a glance"
    - Audience: new and working SOC analysts (L1, L2, L3) and SOC managers
    - Time to read: 5 minutes for this page, 20-40 minutes per role page
    - Outcome: you know what your role does today, which tools you use, and where the worked examples are

## Find your role

| If you are... | You spend most of your day on... | Start here | Then read |
|---|---|---|---|
| New to the SOC, first 90 days | Alert queue, triage, notes, escalations | [L1 analyst](l1-analyst.md) | [Investigation cheat sheet](investigation-cheatsheet.md), [Case 02](walkthroughs/case-02-brute-force-then-success.md) |
| L1 who wants to move up | Scoping, timelines, containment | [L2 analyst](l2-analyst.md) | [Case 01](walkthroughs/case-01-phishing-to-credential-theft.md), [Case 03](walkthroughs/case-03-infostealer-on-laptop.md) |
| Incident handler / L2 | Escalations, coordination with IT and DevOps | [L2 analyst](l2-analyst.md) | All [walkthroughs](walkthroughs/index.md) |
| Threat hunter / detection engineer / L3 | Hunts, new rules, tuning, malware basics | [L3 analyst](l3-analyst.md) | [Case 04](walkthroughs/case-04-web-secret-file-probing.md), [Case 06](walkthroughs/case-06-cloud-key-leak-cryptomining.md) |
| SOC lead / SOC manager | Queue health, Service Level Agreements (SLAs), people, reports, major incidents | [SOC manager](soc-manager.md) | [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md) |
| Anyone, mid-investigation | "How do I check X?" | [Investigation cheat sheet](investigation-cheatsheet.md) | The matching playbook in [04-playbooks](../04-playbooks/phishing.md) |

## How the roles hand work to each other

```text
 Detection (SIEM / EDR / email gateway / cloud)
          │
          ▼
   L1  ── triage ≤ 15 min ──► close as benign / false positive (with note)
          │
          └─ escalate (note + evidence) ──► L2 ── scope, contain, coordinate ──► close with lessons
                                              │
                                              └─ needs deep analysis / new detection ──► L3
                                                                                          │
   SOC manager ◄── SLA breaches, major incidents, metrics, staffing ◄─────────────────────┘
```

!!! tip "One rule that applies to every role"
    If it is not in the ticket, it did not happen. Every check you run, every result, every decision goes into the case notes with a timestamp in UTC (Coordinated Universal Time).

## How to use the walkthroughs

Each [walkthrough](walkthroughs/index.md) is one realistic case told from first alert to lessons learned.

1. **Read the alert** as it arrives. Stop and write down what *you* would check first.
2. **Follow the L1 triage**. Run the queries in your own lab SIEM (Security Information and Event Management) if you have one; swap field names for yours.
3. **Read the escalation note** and compare it with what you would have written.
4. **Follow the L2/L3 investigation** and the timeline table. Notice how each finding leads to the next pivot.
5. **Check the containment commands**, note who approved each one.
6. **Answer the quiz** before you open the answers.

!!! note "Field names"
    Queries use common field names (`user`, `src_ip`, `host`) for Splunk Search Processing Language (SPL), Microsoft Sentinel / Defender tables for Kusto Query Language (KQL), and Elastic Common Schema (ECS) for Elastic / OpenSearch. Your data will differ, keep a one-page field-mapping note for your own SIEM.

## What is in this section

| Page | What you get |
|---|---|
| [L1 analyst](l1-analyst.md) | A full shift hour by hour, triage of the 10 most common alerts, note and escalation templates, 90-day skill plan |
| [L2 analyst](l2-analyst.md) | Taking escalations, pivoting, timelines, containment with approvals, closing with lessons |
| [L3 analyst](l3-analyst.md) | Weekly hunt, detection engineering end to end (Sigma, SPL, KQL), malware triage basics, purple team |
| [SOC manager](soc-manager.md) | Daily, weekly, monthly routine, metric formulas, major-incident bridge, message templates |
| [Investigation cheat sheet](investigation-cheatsheet.md) | 30+ investigation questions with ready queries and live-response one-liners |
| [Walkthroughs](walkthroughs/index.md) | Six end-to-end cases with quizzes |

## Related pages

- [Alert triage](../02-daily-operations/alert-triage.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
- [Shift handover template](../09-templates/shift-handover-template.md)
- [Incident report template](../09-templates/incident-report.md)
