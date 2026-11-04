# How to Use This Handbook

Pick your role, follow the reading path, and practise each page on shift the same day. Then adapt the pages into your own procedures using the conversion steps at the bottom.

!!! abstract "At a glance"
    - Audience: L1/L2/L3 analysts, detection engineers, SOC leads, SOC managers
    - Time to read: 10 minutes
    - Outcome: a personal reading-and-practice plan, and a method to turn any page into an internal procedure

## Three ways to use it

| Mode | How | When |
|------|-----|------|
| **On shift** | Search the attack type ("phishing", "impossible travel"), open the playbook, follow the steps | Live alert or incident |
| **Learn** | Follow a reading path below; after each page, do the practice task | Onboarding, promotion prep |
| **Template** | Copy a page into your wiki, replace placeholders, publish | Writing your own procedures |

## Reading paths by role

Each path pairs a page with a task you do in your real tools. Do not move on until the task is done.

### L1 analyst (weeks 1-4)

| Week | Read | Practise in your tools | Proof |
|------|------|------------------------|-------|
| 1 | [What is a SOC?](what-is-a-soc.md), [Glossary](glossary.md) | Run the five health checks | Screenshot of results in your notes |
| 1 | [Alert triage](../02-daily-operations/alert-triage.md) | Triage 10 low-severity alerts with a senior reviewing | 8 of 10 verdicts agreed |
| 2 | [Severity and SLA](../02-daily-operations/severity-and-sla.md) | Re-rate 5 closed cases; compare with what was assigned | Differences explained |
| 2-3 | [Playbooks](../04-playbooks/index.md): the 3 most frequent alert types | Work one real case per playbook end to end | Case notes pass peer review |
| 4 | [Open-source SOC lab](../10-labs-and-tools/open-source-soc-lab.md) | Replay one attack, find it in the SIEM | Query saved to your library |

### L2 analyst

| Read | Practise |
|------|----------|
| [Incident response lifecycle](../03-incident-response/ir-lifecycle.md) | Write a timeline for a closed incident from raw logs only |
| [Playbooks](../04-playbooks/index.md) | Pick one playbook, run it in the lab, list three steps that are wrong for your environment |
| [Detection lifecycle](../05-detection-engineering/detection-lifecycle.md) | Submit one tuning request with evidence (rule name, false-positive pattern, proposed exclusion) |
| [External attack surface management](../06-threat-intelligence/external-attack-surface-management.md) | List all internet-facing hosts for `example.com` your SOC currently monitors |

### L3 analyst / detection engineer

| Read | Practise |
|------|----------|
| [Use case prioritisation](../01-build-a-soc/use-case-prioritization.md) | Score your top 10 missing detections with the matrix |
| [Log source priorities](../01-build-a-soc/log-source-priorities.md) | Build the log-source inventory; mark gaps |
| [Detection lifecycle](../05-detection-engineering/detection-lifecycle.md) | Move 5 existing rules into version control with test data |
| [SOAR principles](../07-automation-soar/soar-principles.md) | Automate one enrichment step (for example IP reputation on every alert) |

### SOC lead / manager

| Read | Practise |
|------|----------|
| [Operating model](../01-build-a-soc/operating-model.md) | Write or update the service catalog and RACI (Responsible, Accountable, Consulted, Informed) |
| [Team and roles](../01-build-a-soc/team-and-roles.md) | Run the 24x7 staffing formula with your real numbers |
| [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md) | Build the monthly report from last month's data |
| [Maturity model](../01-build-a-soc/maturity-model.md) | Score the SOC; pick 3 improvements for next quarter |
| [Budget and staffing](../01-build-a-soc/budget-and-staffing.md) | Draft the one-page budget request |
| [Policy framework](../08-security-policies/policy-framework.md) | Confirm in writing who may isolate hosts and disable accounts |

## How the sections connect

```text
 08 Policies ──► authority for ──► 01 Build (model, team, stack)
                                          │
 06 Threat intel ──► 05 Detection ──► alerts ──► 02 Daily ops (triage, SLA)
                                                       │ escalate
                                                       ▼
                               04 Playbooks ◄── 03 Incident response
                                                       │ lessons learned
                                                       └──► back to 05 Detection
 07 Automation speeds every step, 10 Labs to practise and test
```

The loop that matters: **every incident or hunt should produce at least one new or tuned detection or one playbook fix.** Track it as a metric.

## Turning a page into your own procedure

Follow these steps for any playbook or procedure page.

1. **Copy** the page into your wiki or Git repository.
2. **Replace placeholders** using this table:

    | Placeholder in handbook | Replace with |
    |-------------------------|--------------|
    | "your SIEM" | Product name + saved search name or link |
    | Generic query | Your exact index/table and field names, tested |
    | "SOC lead" | Role title + named deputy |
    | "notify the owner" | Team name, chat channel, phone |
    | Severity/SLA times | Your agreed times for your coverage hours |
    | "isolate the host" | Exact console steps + who approved this authority |
    | Regulatory deadline | The deadlines that apply to your sector and region |

3. **Test every query.** Run it against the last 7 days. If it returns nothing, check field names before assuming "no activity".
4. **Dry-run** the procedure with one L1 and one L2 on a closed case. Note every step where they hesitated.
5. **Fix** and add an owner, version number and next review date (6-12 months).
6. **Link** the procedure from the matching SIEM rule or SOAR playbook so analysts land on it from the alert.

!!! example "Adapting one query"
    Handbook: `index=auth action=failure | stats count by user`.
    ACME version: `index=win_sec EventCode=4625 | stats count by TargetUserName, IpAddress`. Tested on 7 days of data, 312 results, saved as "AUTH, failed logons by user".

!!! danger "Common mistake: copying authority statements"
    "The SOC may isolate any endpoint" is only true if management approved it. Confirm each containment action in policy before it appears in a procedure, or analysts will hesitate during a real incident.

!!! warning "Common mistake: untested queries"
    A procedure with a query that silently returns zero results is worse than no query. It gives false confidence. Always test against data where you know the answer is non-zero.

## Keeping your version current

| Trigger | Action | Owner |
|---------|--------|-------|
| Major incident closed | Ask "which page was wrong or missing?"; fix within 2 weeks | Incident lead |
| Tool change (new SIEM, EDR) | Re-test every query and console step | Detection engineer |
| Quarterly | Review the 10 most-used procedures | SOC lead |
| Analyst feedback | Fix or reply within 1 week | Page owner |

## Checklist

- [ ] I picked my role path and booked practice time
- [ ] I adapted my first three pages (usually triage, severity, one playbook)
- [ ] Every query in my adapted pages was tested on real data
- [ ] Each adapted page has an owner and review date
- [ ] Containment authority is confirmed in policy

## Related pages

- [Start here](index.md)
- [What is a SOC?](what-is-a-soc.md)
- [Career paths](career-paths.md)
- [Alert triage](../02-daily-operations/alert-triage.md)
- [Policy framework](../08-security-policies/policy-framework.md)
