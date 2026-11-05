---
id: GOV-02
title: Operating Model and Service Catalogue
owner: SOC Manager
audience: SOC team, IT, stakeholders who consume SOC services
review: Every 12 months
summary: How the SOC is organised and what it delivers. It sets the operating model, the hours, the services with their service levels, and what the SOC does not do, so expectations are clear.
---
## 1. Purpose

This document describes how the SOC of [ORGANISATION] operates and what it delivers. It turns the mission in the Charter (GOV-01) into concrete services, hours and responsibilities.

## 2. Operating model

| Aspect | Decision |
|---|---|
| Model | [In-house / Managed (MSSP or MDR) / Hybrid] |
| Hours of coverage | [for example business hours plus on-call for P1 and P2] |
| Out-of-hours | [on-call rota / managed provider] |
| Managed provider, if any | [name], covering [what and when] |
| Escalation out of hours | See GOV-04 |

## 3. Service catalogue

The SOC provides these services. Each has an owner and a service level.

| Service | Delivered as | Service level |
|---|---|---|
| Alert monitoring and triage | Continuous during coverage hours | Alerts acknowledged within SLA (GOV-03) |
| Incident response | On declaration of an incident | Response starts within the severity SLA (GOV-03) |
| Detection engineering | Ongoing | New detections tested before production |
| Threat intelligence | Daily routine plus monthly report | Relevant threats actioned, monthly summary |
| Vulnerability alerting | On critical and actively exploited issues | Notified to owners within [time] |
| Reporting | Daily, weekly, monthly | Delivered on schedule |

## 4. What the SOC does not do

To avoid confusion, the SOC does not:

- [ ] Own patching or system administration (it alerts; owners act).
- [ ] Approve business-affecting containment alone (see GOV-04).
- [ ] Monitor systems outside its scope (GOV-01).
- [ ] Make legal, HR or disclosure decisions (it supports those who do).

> NOTE: Being clear about what the SOC does not do prevents gaps ("we thought the SOC patched that") and overreach. Anything not listed as a SOC service belongs to another owner.

## 5. Interfaces with other teams

| Team | How they work with the SOC |
|---|---|
| IT operations | Acts on SOC requests (patch, reset, isolate); provides context |
| Identity team | Account actions, access reviews |
| Cloud or platform team | Cloud containment, key rotation |
| Legal and privacy | Decisions on notification and lawful monitoring |
| HR | Insider cases, disciplinary action |
| Leadership | Funding, major-incident decisions |

## 6. Capacity and escalation of demand

When alert volume or incidents exceed the SOC's capacity, the SOC manager [escalates for more resource / engages the managed provider / reprioritises], following [process]. Sustained overload is reported to [role] as a risk.

## 7. Review

Reviewed every 12 months, and when the model, hours or services change.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
