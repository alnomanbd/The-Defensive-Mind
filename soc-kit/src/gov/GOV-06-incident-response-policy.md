---
id: GOV-06
title: Incident Response Policy
owner: CISO
audience: SOC team, IT, leadership, and all staff (for reporting)
review: Every 12 months, and after any major incident
summary: The policy that gives the SOC authority to respond to incidents, defines what an incident is, sets the lifecycle, and names who decides what. The procedures sit below it in the SOPs and playbooks.
---
## 1. Purpose

This policy sets out how [ORGANISATION] responds to security incidents. It gives the SOC the authority to act, defines the response lifecycle, and names the decisions that belong to leadership, legal and the business.

## 2. Scope

Applies to all security incidents affecting [ORGANISATION] systems, data and people, on all covered systems (GOV-01), and to everyone who may detect or respond to one.

## 3. What is a security incident

A security incident is any event that harms, or threatens to harm, the confidentiality, integrity or availability of [ORGANISATION] systems or data. Examples: malware execution, account compromise, data theft, ransomware, a successful intrusion.

An **event** or **alert** becomes an **incident** when triage confirms it is real and harmful. Severity is set per GOV-03.

## 4. The response lifecycle

[ORGANISATION] follows this lifecycle. The detailed steps are in the SOPs and playbooks.

| Phase | What happens |
|---|---|
| Prepare | Keep tools, runbooks, contacts and training ready before any incident |
| Identify | Detect and confirm the incident; set severity; declare it |
| Contain | Stop the spread without destroying evidence, with the right approvals (GOV-04) |
| Eradicate | Remove the cause: malware, accounts, access, persistence |
| Recover | Restore to known-good and confirm normal operation |
| Learn | Hold a blameless review and turn lessons into changes |

Evidence is collected throughout, not only at the end.

## 5. Roles and decisions

| Decision | Who |
|---|---|
| Declare an incident | SOC (incident lead) |
| Set and change severity | SOC, per GOV-03 |
| Approve business-affecting containment | Per GOV-04 |
| Lead a major incident | Incident lead, with the SOC manager and CISO |
| Communicate to leadership | SOC manager or CISO |
| Notify regulators or customers | Legal decides |
| Involve law enforcement | Legal decides |

## 6. Legal and regulatory duties

When an incident may involve personal, payment or health data, the SOC alerts the CISO, legal and privacy immediately, because notification deadlines may already be running (for example [GDPR 72 hours], or your local rules). The SOC provides facts; legal decides on notification.

> WARNING: The SOC does not decide whether to notify regulators or customers. Its duty is to alert legal and privacy fast, with accurate facts, so they can decide within the legal clock.

## 7. Evidence and records

Every incident is recorded in the case system with a timeline. Evidence is handled per the Evidence Handling SOP and the Privacy policy (GOV-10). A legal hold is applied where an incident may lead to legal action.

## 8. Reporting and improvement

Every P1 and P2 incident gets a post-incident review (and P3 where there is a useful lesson). Review actions are owned and tracked to closure. Incident trends are reported to leadership monthly.

## 9. Review

Reviewed every 12 months and after any major incident.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
