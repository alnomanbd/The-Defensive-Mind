---
id: GOV-03
title: Severity, Priority and SLA Standard
owner: SOC Manager
audience: SOC team, IT, incident leads, stakeholders
review: Every 12 months
summary: The single scale for how serious an alert or incident is, and the time the SOC commits to act at each level. Every SOP that mentions severity or an SLA refers here.
---
## 1. Purpose

This standard sets one severity scale and one set of service level agreements (SLAs) for [ORGANISATION]. It stops every analyst and tool using a different scale, which is how real attacks get treated as noise and noise wakes up managers.

## 2. Severity scale

| Severity | Meaning | Examples |
|---|---|---|
| P1 Critical | Confirmed compromise with major business impact, or an attack in progress that can cause it | Ransomware spreading, domain or cloud admin compromised, confirmed breach of personal or payment data |
| P2 High | Confirmed compromise of limited scope, or a serious attempt likely to succeed | One server with a web shell, one account taken over, malware executed, credentials phished and entered |
| P3 Medium | Suspicious activity needing investigation, or a contained policy violation | Malware blocked but run from a user folder, unusual admin login, a silent critical log source |
| P4 Low | Failed attempts, informational findings, hygiene issues | Blocked scanning, failed brute force, a single spam message |

## 3. SLAs by severity

These are the times the SOC commits to. Adjust the bracketed values to what [ORGANISATION] can sustain, then hold to them.

| Severity | Acknowledge within | Response starts within | Stakeholder updates | Coverage |
|---|---|---|---|---|
| P1 Critical | [15 minutes] | [15 minutes] | [every 1 hour] | 24 hours a day |
| P2 High | [30 minutes] | [1 hour] | [every 4 hours] | 24 hours a day |
| P3 Medium | [4 business hours] | [1 business day] | [daily] | Business hours |
| P4 Low | [1 business day] | [best effort] | [weekly report] | Business hours |

> NOTE: "Acknowledge" means a human has taken ownership, not that it is resolved. "Response starts" means active work on containment or investigation has begun.

## 4. Setting severity

Severity is set by scoring impact and urgency, with automatic overrides to P1. The method is in SOP-05 (Severity Assignment and Escalation). This standard owns the scale and the SLAs; SOP-05 owns how an analyst applies them.

### Automatic P1 overrides

Regardless of score, set P1 immediately when any of these is true:

- [ ] Ransomware or a wiper confirmed on any system.
- [ ] A domain, cloud root or global administrator account compromised.
- [ ] Confirmed theft of personal, payment or health data.
- [ ] The SOC's own tools or the security team's accounts compromised.
- [ ] An attacker confirmed to have interactive access to production.

## 5. Changing severity

- [ ] Raise severity as soon as new facts justify it; do not wait for the worst case to be confirmed.
- [ ] Lower severity only with evidence, and for P1 and P2 only with the incident lead's agreement.
- [ ] Record every severity change with the reason and time.

## 6. Measuring SLA performance

The SOC reports SLA attainment (the share of alerts and incidents handled within these times) monthly, per the Metrics and KPI Standard (GOV-08). Repeated breaches are treated as a resourcing or process problem, not an individual failing.

## 7. Review

Reviewed every 12 months, and after any incident where the severity or SLA was disputed.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
