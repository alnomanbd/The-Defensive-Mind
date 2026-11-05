---
id: GOV-05
title: SOC RACI
owner: SOC Manager
audience: SOC team, IT, and all teams that work with the SOC
review: Every 12 months
summary: Who is Responsible, Accountable, Consulted and Informed for each SOC activity, so work does not fall between teams and nobody is surprised.
---
## 1. Purpose

This RACI chart makes clear, for each SOC activity, who does the work, who is answerable for it, who must be asked, and who must be told. It prevents the two classic failures: a task nobody owns, and a decision made without the right people.

> NOTE: RACI stands for Responsible (does the work), Accountable (answerable, one person), Consulted (asked before), Informed (told after). There is exactly one Accountable per activity.

## 2. How to read this chart

- **R (Responsible):** carries out the task.
- **A (Accountable):** owns the outcome; just one role per row.
- **C (Consulted):** gives input before the task is done.
- **I (Informed):** told once it is done or decided.

## 3. RACI chart

Roles: SOCM (SOC manager), L1, L2, L3, DE (detection engineer), IT, ID (identity team), CISO, Legal.

| Activity | SOCM | L1 | L2 | L3 | DE | IT | ID | CISO | Legal |
|---|---|---|---|---|---|---|---|---|---|
| Monitor the alert queue | A | R | C | | | | | I | |
| Triage an alert | A | R | C | | | | | | |
| Investigate an escalation | A | | R | C | | C | C | I | |
| Declare an incident | A | | R | R | | | | I | |
| Approve host isolation (server) | A | | R | R | | C | | I | |
| Approve account disable (exec/admin) | A | | C | | | | R | I | |
| Lead a major incident | A | | | R | | C | C | C | C |
| Build or change a detection | A | | C | C | R | | | I | |
| Tune a noisy rule | A | | R | C | R | | | | |
| Onboard a log source | A | | | C | R | R | | I | |
| Produce the monthly report | A | | | | | | | I | |
| Decide on breach notification | I | | | | | | | C | A |
| Insider investigation authorisation | C | | | | | | | C | A |
| Set SOC budget and staffing | R | | | | | | | A | |

Adjust the roles and rows to [ORGANISATION]. The point is that every activity has exactly one A and at least one R.

## 4. Decisions that are never the SOC's alone

Some decisions sit with other owners even when the SOC does the technical work:

- [ ] Breach notification to regulators or customers: Legal is Accountable.
- [ ] Insider investigation of a named person: Legal and HR authorise (see GOV-10 and the HR authorisation template).
- [ ] Shutting off a production service: the business owner or CISO decides.
- [ ] Paying a ransom: a business and legal decision, never the SOC's.

## 5. Review

Reviewed every 12 months, and whenever team structure changes.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
