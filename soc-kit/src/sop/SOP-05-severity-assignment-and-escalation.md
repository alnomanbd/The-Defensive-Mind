---
id: SOP-05
title: Severity Assignment and Escalation
owner: SOC Lead
audience: All SOC analysts, shift leads, incident leads
review: Every 12 months, and after any incident where severity was disputed
summary: How to set the severity of an alert or incident in under a minute, when to raise or lower it, and exactly who must be told, how and how fast.
---
## 1. Purpose

Severity decides how fast the SOC moves and who gets woken up. If every analyst sets it differently, either managers get called for noise or real attacks wait until morning. This procedure gives one scale, one method and one escalation path.

## 2. Scope

- Alerts after triage, security incidents, and incidents reported from outside the SOC (users, IT, vendors, law enforcement).
- Severity can change at any time during an incident. Every change is recorded.

## 3. Severity scale

| Severity | Meaning | Examples | Response starts | Update stakeholders |
|---|---|---|---|---|
| P1 Critical | Confirmed compromise with major business impact, or an attack in progress that can cause it | Ransomware spreading, domain admin compromised, confirmed data breach of personal or payment data, production outage caused by an attack | 15 minutes, 24 hours a day | Every 1 hour |
| P2 High | Confirmed compromise of a limited scope, or a serious attempt likely to succeed | One server with a web shell, one account taken over, malware executed on a laptop, successful phishing with credentials entered | 1 hour, 24 hours a day | Every 4 hours |
| P3 Medium | Suspicious activity needing investigation, or a contained policy violation | Malware blocked but run from a user folder, unusual admin login, silent critical log source, policy breach without data loss | 4 hours, business hours | Daily |
| P4 Low | Attempts that failed, informational findings, hygiene issues | Blocked internet scanning, failed brute force with no success, single spam campaign | Next business day | Weekly report |

Your organisation's exact times are set in GOV-03. This procedure uses the scale above as the default.

## 4. Procedure

### 4.1 Score impact and urgency

Answer two questions. Use the higher answer if unsure.

| Impact: what is or could be affected? | Score |
|---|---|
| Many systems, critical business service, or regulated data (personal, payment, health) | 3 |
| One important system, one privileged account, or confidential data | 2 |
| One ordinary user or system, no sensitive data | 1 |

| Urgency: how fast is it moving? | Score |
|---|---|
| Active now and spreading, or data leaving now | 3 |
| Confirmed but contained or not spreading | 2 |
| Attempt only, or happened in the past with no ongoing activity | 1 |

### 4.2 Read the severity

| Impact plus urgency | Severity |
|---|---|
| 6 | P1 Critical |
| 5 | P2 High (P1 if regulated data is involved) |
| 3 or 4 | P3 Medium |
| 2 | P4 Low |

### 4.3 Automatic overrides

Set P1 straight away, whatever the score, when any of these is true:

- [ ] Ransomware or a wiper is confirmed on any system
- [ ] A domain administrator, cloud root or global administrator account is compromised
- [ ] Confirmed theft of personal, payment or health data
- [ ] The SOC's own tools or the security team's accounts are compromised
- [ ] An attacker is confirmed to have interactive access to a production system
- [ ] A regulator, law enforcement agency or the media reports a breach

### 4.4 Change severity

1. Raise severity as soon as new facts justify it. Do not wait for confirmation of the worst case.
2. Lower severity only with evidence, and for P1 and P2 only with the incident lead's agreement.
3. Record every change with time, old and new severity, reason and who decided, in the case and the incident timeline (TPL-09).

## 5. Escalation matrix

Names and numbers are kept in GOV-04. This table sets who and how.

| Severity | Inside the SOC | Outside the SOC | How | Within |
|---|---|---|---|---|
| P1 Critical | L2, incident lead, SOC Lead | CISO or head of security, IT operations lead, system owner. CISO decides on executives, legal, privacy, communications | Phone call, then incident channel. Open a bridge call | 15 minutes |
| P2 High | L2, incident lead, SOC Lead informed | System owner, IT operations | Phone for the incident lead, chat and ticket for others | 1 hour |
| P3 Medium | L2 if needed | System owner by ticket | Ticket and chat | 4 business hours |
| P4 Low | None | Included in weekly report | Report | Weekly |

> WARNING: If the person on the matrix does not answer within 10 minutes for P1 or 30 minutes for P2, go to their backup, then one level up. Never stop at a voicemail.

### 5.1 What to say when you escalate

Use the same five points every time, by phone or in writing:

```text
1. Who I am and that this is a security incident, severity P_.
2. What happened, in one sentence.
3. What is affected (systems, users, data) and whether it is ongoing.
4. What the SOC has done so far.
5. What I need from you and by when (decision, access, action).
```

### 5.2 Legal and regulatory clocks

Some laws and contracts set reporting deadlines that start when the organisation becomes aware of a breach (for example 72 hours under the EU GDPR). The SOC does not decide on notification, but must inform the CISO and the privacy or legal contact at once when personal data, payment data or a regulated service may be involved, so the clock is not missed.

## 6. Disagreements

If an analyst and a system owner disagree on severity, the higher severity applies until the incident lead decides. Disputes are recorded and reviewed in the post-incident review.

## 7. Records

- Severity and every change, in the case and in TPL-09.
- Escalation calls: who was called, when, outcome.
- Notification decisions by the CISO, privacy or legal, referenced in the case.

## 8. Metrics

| Metric | Target |
|---|---|
| P1 escalated within 15 minutes | 100 percent |
| P2 escalated within 1 hour | 95 percent |
| Severity changed down after escalation (over-escalation) | Tracked, reviewed monthly |
| Incidents found later to be under-rated | Zero; each one reviewed |

## 9. Common mistakes

- Waiting to be sure before raising to P1. Raise first, lower later.
- Escalating by email at night.
- Setting severity by the alert's default level and never revisiting it.
- Calling the boss with no clear ask. Always end with what you need.
- Forgetting privacy and legal when personal data is involved.

## 10. Related documents

- GOV-03 Severity, Priority and SLA Standard, GOV-04 Escalation and Contact Matrix, GOV-06 Incident Response Policy
- SOP-03 Alert Triage and Classification, SOP-07 On-Call and After-Hours Response, SOP-42 Major Incident and War Room, SOP-43 Incident Communication
- TPL-07 Incident Report: Initial Notification, TPL-09 Incident Timeline and Decision Log
