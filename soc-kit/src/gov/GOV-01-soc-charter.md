---
id: GOV-01
title: SOC Charter
owner: CISO
audience: Executives, SOC team, IT, and all stakeholders
review: Every 12 months, or after a major change to the organisation or the SOC
summary: The founding document of the SOC. It states why the SOC exists, what it does, what authority it has, and who is accountable, so everyone agrees on its purpose and mandate.
---
## 1. Purpose

This charter establishes the Security Operations Center (SOC) of [ORGANISATION]. It defines the SOC's mission, scope, services, authority and accountability. It is the document everyone points to when asking "what is the SOC for, and what is it allowed to do?"

## 2. Mission

The SOC exists to protect [ORGANISATION] by detecting, investigating and responding to security threats, every day, and by continuously improving that ability. The SOC reduces the time between an attack starting and the organisation stopping it.

## 3. Scope

- [ ] Systems covered: [list, for example all corporate endpoints, servers, cloud environments, identity systems, email].
- [ ] Systems excluded, if any, and who covers them instead: [list].
- [ ] Hours of coverage: [for example business hours plus on-call, or 24/7].

## 4. Services

The SOC provides the following services. Details are in the Operating Model (GOV-02).

| Service | What it means |
|---|---|
| Security monitoring | Watching for threats across the covered systems |
| Alert triage and investigation | Deciding which alerts are real and what they mean |
| Incident response | Containing, eradicating and recovering from incidents |
| Detection engineering | Building and tuning what the SOC detects |
| Threat intelligence | Context on threats relevant to the organisation |
| Reporting | Regular reporting to management on security posture |

## 5. Authority

To do its job, the SOC is granted the following authority. Business-affecting actions follow the approvals in the Escalation Matrix (GOV-04).

- [ ] To access the logs and telemetry of covered systems for security purposes.
- [ ] To investigate suspected security incidents on covered systems.
- [ ] To take or request pre-agreed containment actions (for example isolating an endpoint, disabling an account) under the approvals set in GOV-04.
- [ ] To declare a security incident and convene the response.
- [ ] To require cooperation from IT and system owners during an incident.

> NOTE: The SOC's authority is bounded by this charter, the privacy rules in GOV-10, and the approvals in GOV-04. The SOC acts within an agreed mandate, not on its own discretion.

## 6. Accountability

| Role | Accountable for |
|---|---|
| CISO (or [role]) | The SOC's overall effectiveness and this charter |
| SOC manager | Running the SOC day to day, its metrics and its people |
| SOC analysts | Following the SOPs and documenting their work |
| System owners | Supporting the SOC with access and context |
| Executive sponsor | Funding and backing the SOC's mandate |

## 7. How success is measured

The SOC's performance is measured against the metrics in the Metrics and KPI Standard (GOV-08), focusing on outcomes: how fast real incidents are detected and contained, and how much the organisation's risk is reduced, not on activity volume.

## 8. Review

This charter is reviewed every 12 months and whenever the organisation or the SOC changes significantly. Changes are approved by [role].

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
