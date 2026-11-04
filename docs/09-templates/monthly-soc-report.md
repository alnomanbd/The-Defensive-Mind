# Monthly SOC Report Template

A management-friendly template for reporting what the Security Operations Center (SOC) did, how well it performed and which decisions leadership needs to make.

!!! abstract "At a glance"
    - Audience: SOC manager (author); leadership, Chief Information Security Officer (CISO), risk committee (readers)
    - Time to read: 5 minutes (2-4 hours to prepare)
    - Outcome: a two-to-four-page report that a busy executive can read in ten minutes and act on

!!! tip "How to use"
    - Lead with the message, not the data. The executive summary should stand on its own.
    - Show trends (this month versus the last three) rather than single numbers.
    - Explain every metric in business terms: what it means and whether it is good.
    - Keep raw alert counts out of the headline; leaders care about risk and outcomes.
    - End with clear decisions needed, each with options and a recommendation.
    - Use the same structure every month so readers know where to look.

---

## SOC report: `<Month YYYY>`

| Field | Value |
|---|---|
| Reporting period | `<YYYY-MM-01>` to `<YYYY-MM-DD>` |
| Prepared by | `<name, role>` |
| Distribution | `<CISO, CIO, risk committee>` |
| Classification | `<Internal / Confidential>` |

### Executive summary

> **Overall status:** `<Green / Amber / Red>`, `<one-line reason>`
>
> - `<Most important point, e.g. "No incident caused customer impact this month.">`
> - `<Second point, e.g. "One High incident (account compromise) contained within 3 hours.">`
> - `<Trend, e.g. "Time to contain improved 25% after automation of account lockout.">`
> - `<Top risk, e.g. "40% of servers still do not send logs; detection blind spot.">`
> - `<Decision needed, e.g. "Approval to extend log retention to 12 months.">`

### Key performance indicators (KPIs)

| KPI | Target | Last month | This month | Trend | Comment |
|---|---|---|---|---|---|
| Incidents (Critical / High / Medium / Low) |: | `<0/1/4/12>` | `<0/1/3/9>` | `<↓>` | `<...>` |
| Mean time to detect (MTTD) | `<< 1 h>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Mean time to acknowledge (MTTA) | `<< 15 min>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Mean time to contain (MTTC), High and above | `<< 4 h>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Alerts triaged within service level | `<≥ 95%>` | `<...>` | `<...>` | `<...>` | `<...>` |
| False positive rate (top 10 rules) | `<< 30%>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Critical assets sending logs | `<100%>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Endpoint agent coverage | `<≥ 98%>` | `<...>` | `<...>` | `<...>` | `<...>` |
| ATT&CK techniques with tested detection | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Overdue post-incident actions | `<0>` | `<...>` | `<...>` | `<...>` | `<...>` |

!!! note "Definitions"
    Write a one-line definition of each KPI in an appendix and never change it silently. If a definition changes, say so in the report and restate last month's value.

### Top incidents

Limit to three to five incidents that matter to the business.

| Incident | Severity | What happened (plain English) | Business impact | Status | Lesson |
|---|---|---|---|---|---|
| `<INC-...>` | `<High>` | `<Staff account taken over through phishing>` | `<No data loss; 1 user offline 2 h>` | `<Closed>` | `<Enforce phishing-resistant MFA>` |
| `<INC-...>` | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

### Threat landscape

- `<Relevant external trend, e.g. "Rise in invoice fraud emails across our sector.">`
- `<What the SOC did about it, e.g. "Added two detections and briefed finance team.">`

### Detection changes

| Change | Count | Examples |
|---|---|---|
| New detections deployed | `<n>` | `<Suspicious mailbox forwarding rule>` |
| Detections tuned | `<n>` | `<Reduced noise on admin logon rule by 60%>` |
| Detections retired | `<n>` | `<Rule superseded by EDR native alert>` |
| New log sources onboarded | `<n>` | `<Cloud identity provider audit logs>` |
| Detection tests run (for example with Atomic Red Team) | `<n>` | `<12 passed, 3 failed, tickets raised>` |

### Improvement and project status

| Initiative | Goal | Status | % done | Next milestone |
|---|---|---|---|---|
| `<SOAR phishing automation>` | `<Cut triage time by half>` | `<On track>` | `<60%>` | `<Go-live <date>>` |
| `<...>` | `<...>` | `<At risk>` | `<...>` | `<...>` |

### Top risks

| Risk | Likelihood | Impact | Trend | Mitigation / owner |
|---|---|---|---|---|
| `<No logging from legacy servers>` | `<High>` | `<High>` | `<->>` | `<Onboarding plan, owner <name>>` |
| `<Single analyst on night shift>` | `<Medium>` | `<High>` | `<↑>` | `<Hiring request pending>` |
| `<Accepted risk RA-... expiring>` | `<...>` | `<...>` | `<...>` | `<Review due <date>>` |

### Decisions needed

| # | Decision | Options | Recommendation | Needed by |
|---|---|---|---|---|
| 1 | `<Extend log retention to 12 months>` | `<A: approve budget; B: keep 90 days and accept risk>` | `<A, needed for investigations and audit>` | `<date>` |
| 2 | `<...>` | `<...>` | `<...>` | `<...>` |

### Appendix

- KPI definitions
- Full incident list (link to case management export)
- Staffing and on-call summary

---

## Worked example

??? example "Filled-in summary: SOC report, April 2026 (ACME)"
    **Overall status: Amber**, no customer impact, but log coverage of servers is still below target.

    - No incident affected customers or caused data loss.
    - One High incident (phishing led to mailbox takeover) contained in 46 minutes.
    - Mean time to contain serious incidents dropped from 4.1 h to 2.9 h after automated account lockout.
    - 38% of Linux servers still send no logs: attacks there would go unseen.
    - Decision needed: budget for 12-month log retention by 31 May.

    | KPI | Target | March | April | Trend |
    |---|---|---|---|---|
    | Incidents (C/H/M/L) |, | 0/2/5/14 | 0/1/3/11 | ↓ |
    | MTTD | < 1 h | 52 min | 38 min | ↑ better |
    | MTTA | < 15 min | 11 min | 9 min | ↑ better |
    | MTTC (High+) | < 4 h | 4.1 h | 2.9 h | ↑ better |
    | Alerts triaged in service level | ≥ 95% | 91% | 96% | ↑ better |
    | Critical assets sending logs | 100% | 58% | 62% | -> slow |
    | Overdue post-incident actions | 0 | 4 | 2 | ↓ |

    | Decision | Options | Recommendation | Needed by |
    |---|---|---|---|
    | Log retention | A: 12 months (extra storage cost); B: keep 90 days | A, two investigations this year needed data older than 90 days | 2026-05-31 |
    | Night shift staffing | A: hire one analyst; B: outsource nights; C: accept single cover | B for 6 months, then review | 2026-06-15 |

## Writing tips

| Instead of | Write |
|---|---|
| "We processed 48,000 alerts." | "Automation filtered 97% of alerts; analysts reviewed 1,400." |
| "MTTC 3.2 h." | "We contained serious incidents in about 3 hours, inside our 4-hour target." |
| "Need more budget." | "Option A costs X and closes risk Y; option B leaves Y open." |

## Checklist

- [ ] Executive summary readable on its own
- [ ] Every KPI has a target and a trend
- [ ] Incidents described in business terms
- [ ] Risks link to owners and the risk register
- [ ] Each decision has options and a recommendation
- [ ] Classification and distribution list set

## Related pages

- [Post-incident review template](post-incident-review-template.md)
- [Risk acceptance template](risk-acceptance.md)
- [Detection request](detection-request.md)
- [Templates overview](index.md)
