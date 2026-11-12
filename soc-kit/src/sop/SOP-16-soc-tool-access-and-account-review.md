---
id: SOP-16
title: SOC Tool Access and Account Review
owner: SOC Manager
audience: SOC manager, SOC engineers, identity team
review: Every 6 months
summary: Who has access to the SOC's own tools, at what level, and how that access is granted, reviewed and removed. The SOC's tools are powerful, so their access deserves extra care.
---
## 1. Purpose

The SOC's tools can read everything and, in the case of EDR and SOAR, act on everything. Access to them is some of the most powerful in the organisation. This procedure keeps that access least-privilege, reviewed and removed when no longer needed.

> WARNING: An attacker who reaches the SOC's tools can turn your defences into a weapon: read all logs, disable detections, or use EDR and SOAR to act across the estate. Guard access to SOC tools more tightly than ordinary systems.

## 2. Scope

Access to the SOC's tools for [ORGANISATION]: SIEM, EDR and XDR, SOAR, case management, threat intel platform, and admin consoles.

## 3. Granting access

- [ ] Access is requested and approved by the SOC manager (or [role]).
- [ ] Grant the least level needed for the role: read-only where that suffices, admin only where genuinely required.
- [ ] Separate admin access from everyday access where the tool allows.
- [ ] Protect SOC-tool accounts with strong, phishing-resistant MFA.
- [ ] Record the grant: who, what level, which tool, why, and the approver.

## 4. Levels of access

| Level | Who | Can do |
|---|---|---|
| Read-only | L1, auditors | View alerts and search; no changes, no actions |
| Analyst | L1, L2 | Work cases, run approved response within the matrix (GOV-04) |
| Engineer | L3, detection engineers | Change detections, pipelines, configuration |
| Admin | Named few | Full control of the platform |

Keep admin to the smallest possible number of named people.

## 5. Reviewing access

- [ ] Review all SOC-tool access at least [every 6 months], and admin access [every 3 months].
- [ ] The SOC manager confirms each person still needs their level; remove the rest.
- [ ] Check for dormant accounts and disable them.
- [ ] Review service accounts and integration credentials the tools use.

## 6. Removing access

- [ ] When someone leaves the SOC or the organisation, remove their access on their last day (immediately if the departure is not amicable).
- [ ] When someone changes role, reduce their access to what the new role needs.
- [ ] Rotate any shared or service credentials they knew.

## 7. Monitoring

- [ ] Log and monitor access to and actions within the SOC tools.
- [ ] Alert on new admin accounts, privilege changes, and access from unusual places.
- [ ] Treat the SOC's own tools as a monitored, high-value asset (self-monitoring).

## 8. Records

Keep a current record of who has access to each SOC tool, at what level, and the date of the last review.

## 9. Review

Reviewed every 6 months.
