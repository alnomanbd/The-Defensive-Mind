# SOC Career Paths

This page maps the main career paths inside and around a Security Operations Center (SOC), the skills each role needs, and practical 30/60/90-day plans. Use it to plan your own growth or to mentor others.

!!! abstract "At a glance"
    - Audience: aspiring and current analysts, mentors, SOC managers
    - Time to read: 15 minutes
    - Outcome: you can pick a target role, see the skill gaps, and follow a concrete plan for your first 90 days

## The career map

```text
                      ┌──► Detection Engineer ──► Detection Lead
                      │
 L1 Analyst ──► L2 Analyst ──► L3 / Senior Analyst ──► SOC Lead ──► SOC Manager ──► Head of SecOps / CISO
                      │                │
                      │                ├──► Incident Responder ──► IR Lead / DFIR specialist
                      │                │
                      │                └──► Threat Hunter ──► Threat Intel / Adversary research
                      │
                      └──► Security Automation Engineer ──► Security Platform / Architecture
```

Choose by what energises you: **solving puzzles** (hunting, IR), **building** (detection, automation), or **growing people** (leadership).

## Roles at a glance

| Role | Core question they answer | Typical experience | Main outputs |
|------|---------------------------|--------------------|--------------|
| L1 analyst | "Is this alert real?" | 0-2 years | Triaged alerts, clean escalations |
| L2 analyst | "What happened and how far did it spread?" | 2-4 years | Investigations, scoping, containment |
| L3 / senior analyst | "What is the attacker doing and how do we stop it?" | 4+ years | Complex cases, mentoring, tuning |
| Detection engineer | "How do we catch this reliably next time?" | 3+ years | Tested detection rules, coverage maps |
| Incident responder | "How do we contain, clean and recover?" | 4+ years | Incident leadership, forensics, reports |
| Threat hunter | "What did our rules miss?" | 4+ years | Hypothesis-driven hunts, new detections |
| SOC lead | "Is the shift working well today?" | 5+ years | Prioritisation, quality review, coaching |
| SOC manager | "Is the SOC delivering value to the business?" | 7+ years | Strategy, budget, staffing, reporting |

## Skills by role

Rating: 1 = awareness, 2 = working knowledge, 3 = strong, 4 = expert.

| Skill | L1 | L2 | L3 | Det. eng. | IR | Hunter | Manager |
|-------|----|----|----|-----------|----|--------|---------|
| Networking (TCP/IP, DNS, HTTP, TLS) | 2 | 3 | 3 | 3 | 3 | 3 | 2 |
| Windows internals and logging | 2 | 3 | 4 | 4 | 4 | 4 | 1 |
| Linux internals and logging | 1 | 2 | 3 | 3 | 3 | 3 | 1 |
| Cloud identity and logs | 1 | 2 | 3 | 3 | 3 | 3 | 2 |
| SIEM query language | 2 | 3 | 4 | 4 | 3 | 4 | 1 |
| MITRE ATT&CK | 2 | 3 | 4 | 4 | 3 | 4 | 2 |
| Scripting (Python, PowerShell) | 1 | 2 | 3 | 4 | 3 | 3 | 1 |
| Malware triage | 1 | 2 | 3 | 2 | 3 | 3 | 1 |
| Digital forensics | 1 | 2 | 3 | 2 | 4 | 3 | 1 |
| Detection-as-code, version control | 1 | 1 | 2 | 4 | 2 | 3 | 1 |
| Written communication | 2 | 3 | 3 | 3 | 4 | 3 | 4 |
| Stakeholder management | 1 | 2 | 3 | 2 | 4 | 2 | 4 |
| Budgeting, hiring, metrics | 1 | 1 | 1 | 1 | 2 | 1 | 4 |

!!! tip "The underrated skill"
    Clear writing separates good analysts from great ones. A case note that a stranger can understand at 3 a.m. is worth more than a clever query nobody can follow.

## Practical skill tests by level

Use these as interview tasks or self-checks. If you can do them in the time shown, you are working at that level.

| Level | Task | Time |
|-------|------|------|
| L1 | Given an alert "5 failed logons then success", decide true/false positive and write a 3-line case note | 15 min |
| L2 | Given a phishing click, list every user who received the same email and who clicked | 30 min |
| L3 | Given one compromised host, build a timeline of lateral movement across the estate | 2 hours |
| Detection engineer | Write a rule for the L1 scenario, test it on 7 days of data, report false-positive rate | 2 hours |
| Manager | From last month's cases, produce 5 metrics and one improvement proposal | 1 hour |

### L1 test: brute force followed by success

Sample Windows Security log lines:

```text
2026-03-04T09:12:01Z EventID=4625 TargetUserName=a.khan IpAddress=203.0.113.45 LogonType=3 Status=0xC000006A
2026-03-04T09:12:03Z EventID=4625 TargetUserName=a.khan IpAddress=203.0.113.45 LogonType=3 Status=0xC000006A
... (5 more 4625 events within 6 seconds)
2026-03-04T09:12:09Z EventID=4624 TargetUserName=a.khan IpAddress=203.0.113.45 LogonType=3
```

=== "Splunk SPL"

    ```spl
    index=win_sec (EventCode=4625 OR EventCode=4624) earliest=-1h
    | stats count(eval(EventCode=4625)) as fails count(eval(EventCode=4624)) as success by TargetUserName, IpAddress
    | where fails>=5 AND success>=1
    ```

=== "Microsoft KQL"

    ```kql
    SecurityEvent
    | where TimeGenerated > ago(1h) and EventID in (4624, 4625)
    | summarize fails=countif(EventID==4625), success=countif(EventID==4624) by TargetUserName, IpAddress
    | where fails >= 5 and success >= 1
    ```

=== "Wazuh (OpenSearch DQL)"

    ```text
    data.win.system.eventID:(4625 or 4624) and data.win.eventdata.targetUserName:"a.khan"
    ```

What a good L1 answer contains: source IP owner (internal? VPN? foreign hosting provider?), whether the user confirms the activity, what the account did after the success, and an escalation if the source is unknown.

## Certifications (vendor-neutral examples)

Certifications open doors and give structure to learning; they do not replace hands-on skill. Pick one that matches your next step, not the one with the longest name.

| Stage | Example certifications | Why |
|-------|------------------------|-----|
| Entry | CompTIA Security+, ISC2 Certified in Cybersecurity (CC) | Broad foundations, often required by employers |
| Analyst | CompTIA CySA+, GIAC Certified Intrusion Analyst (GCIA), Blue Team Level 1 (BTL1) | Log analysis, network traffic, triage |
| Incident response | GIAC Certified Incident Handler (GCIH), GIAC Certified Forensic Analyst (GCFA) | Handling and forensics |
| Detection / hunting | GIAC Cyber Threat Intelligence (GCTI), hunting-focused practical certifications | Intel and hypothesis-driven work |
| Cloud | Cloud provider security specialty certifications, Certificate of Cloud Security Knowledge (CCSK) | Cloud logs, identity, controls |
| Management | ISC2 Certified Information Systems Security Professional (CISSP), ISACA Certified Information Security Manager (CISM) | Governance, risk, program management |

!!! note "Free and low-cost alternatives"
    Public capture-the-flag events, free blue-team challenge platforms, open-source lab builds and writing public detection rules all build a portfolio that hiring managers value. A GitHub repository with ten well-documented detections can outweigh a certificate.

## 30/60/90-day plans

### New L1 analyst

| Period | Goals | Evidence of success |
|--------|-------|---------------------|
| Days 1-30 | Learn the environment: key assets, crown jewels, top 10 alert types, escalation contacts. Shadow seniors. Complete tool access. | Can triage the top 5 alert types with review; knows who to call for what |
| Days 31-60 | Triage independently on day shift. Use playbooks for every case. Write clear case notes. | Escalations rarely bounced back for missing data; notes pass peer review |
| Days 61-90 | Own a small improvement: one tuning suggestion, one playbook fix or one enrichment idea. | At least one accepted improvement; ready for on-call shadowing |

### New L2 analyst (promoted or hired)

| Period | Goals | Evidence of success |
|--------|-------|---------------------|
| Days 1-30 | Learn investigation tooling deeply: endpoint telemetry, identity logs, email trace. Review 20 closed incidents. | Can scope a phishing or malware case end to end |
| Days 31-60 | Lead medium-severity investigations. Coach L1 on escalations. | Cases closed within SLA; L1 feedback given weekly |
| Days 61-90 | Propose two detection improvements from real cases. Take part in a tabletop. | Improvements merged; tabletop role performed well |

### New detection engineer

| Period | Goals | Evidence of success |
|--------|-------|---------------------|
| Days 1-30 | Inventory existing rules, log sources and false-positive rates. Map coverage to ATT&CK. | Coverage map and top-10 noisy rule list published |
| Days 31-60 | Set up a detection-as-code workflow: repository, review, test data. Tune the five noisiest rules. | Alert volume down measurably (for example 20-40%) with no loss of true positives |
| Days 61-90 | Ship five new high-value detections from the [prioritised use cases](../01-build-a-soc/use-case-prioritization.md). | Each new rule tested, documented, linked to a playbook |

### New SOC lead / manager

| Period | Goals | Evidence of success |
|--------|-------|---------------------|
| Days 1-30 | Listen: one-to-ones with every analyst, key stakeholders and IT owners. Read last quarter's incidents and metrics. | Written "current state" summary with top 5 problems |
| Days 31-60 | Fix the most painful problem (often noise, unclear severity or shift gaps). Agree metrics with management. | One visible improvement; agreed KPI set |
| Days 61-90 | Publish a 12-month plan based on the [maturity model](../01-build-a-soc/maturity-model.md) and [roadmap](../01-build-a-soc/roadmap.md). | Plan approved, budget request prepared |

## Moving up: what promotion committees look for

| From -> to | Look for |
|-----------|----------|
| L1 -> L2 | Consistent quality, good questions, starts investigating beyond the alert |
| L2 -> L3 | Leads incidents calmly, finds root cause, teaches others |
| Analyst -> detection engineer | Writes and tests rules, understands false-positive trade-offs, uses version control |
| Analyst -> IR | Handles pressure, documents decisions, communicates with non-technical people |
| Senior -> lead | Improves the team's output, not only their own |

!!! warning "Burnout is a career risk"
    Night shifts and alert fatigue drive people out of security. Protect learning time (for example 10-20% of each week), rotate people off pure triage, and track overtime. A tired analyst misses things.

## Checklist: personal development plan

- [ ] I have chosen a target role for the next 12-24 months
- [ ] I have rated myself on the skills table and picked three gaps
- [ ] I have a hands-on project (lab, detection, script) for each gap
- [ ] I have a mentor and meet them at least monthly
- [ ] I have agreed learning time with my manager

## Related pages

- [Team and roles](../01-build-a-soc/team-and-roles.md)
- [What is a SOC?](what-is-a-soc.md)
- [Detection lifecycle](../05-detection-engineering/detection-lifecycle.md)
- [Incident response lifecycle](../03-incident-response/ir-lifecycle.md)
- [Open-source SOC lab](../10-labs-and-tools/open-source-soc-lab.md)
- [Glossary](glossary.md)
