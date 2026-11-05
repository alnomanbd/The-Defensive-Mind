---
id: GOV-04
title: Escalation and Contact Matrix
owner: SOC Manager
audience: SOC team, incident leads, IT, leadership
review: Every 6 months, and whenever contacts change
summary: Who to contact, when, how and for what approval, at each severity. The one place that answers "who do I call at 3am and what can they authorise?"
---
## 1. Purpose

This matrix sets out who is contacted during a security incident, in what order, by which method, and who approves business-affecting actions. In an incident, there is no time to work this out; it must be decided in advance.

> WARNING: Keep the contact details in this document current. A matrix with an old phone number is worse than none, because people trust it. Review contacts every 6 months and whenever someone changes role.

## 2. Escalation by severity

| Severity | Inside the SOC | Outside the SOC | Method | Within |
|---|---|---|---|---|
| P1 Critical | L2, incident lead, SOC manager | CISO, IT operations lead, system owner; CISO decides on executives, legal, privacy, communications | Phone first, then incident channel and bridge | [15 minutes] |
| P2 High | L2, incident lead; SOC manager informed | System owner, IT operations | Phone for the lead, chat and ticket for others | [1 hour] |
| P3 Medium | L2 if needed | System owner | Ticket and chat | [4 business hours] |
| P4 Low | None | Weekly report | Report | Weekly |

> NOTE: If a P1 contact does not answer within [10 minutes] (P2 within [30 minutes]), call their backup, then their manager. Record every attempt in the incident timeline.

## 3. Contact list

Fill in and keep current. Store the live version where the on-call team can reach it, including offline.

| Role | Primary | Backup | Phone | Hours |
|---|---|---|---|---|
| SOC manager | [name] | [name] | [number] | [hours] |
| Incident lead | [name] | [name] | [number] | [hours] |
| CISO | [name] | [name] | [number] | [hours] |
| IT operations lead | [name] | [name] | [number] | [hours] |
| Identity team | [name] | [name] | [number] | [hours] |
| Cloud or platform team | [name] | [name] | [number] | [hours] |
| Legal | [name] | [name] | [number] | [hours] |
| Privacy or data protection officer | [name] | [name] | [number] | [hours] |
| Communications | [name] | [name] | [number] | [hours] |
| Managed provider (if any) | [name] | [name] | [number] | [hours] |

## 4. Who approves what

Business-affecting containment needs the approval named here. The SOC may act without waiting only where this matrix pre-authorises it.

| Action | Pre-authorised for SOC? | Otherwise approved by |
|---|---|---|
| Isolate a laptop (EDR) | Yes, for confirmed malware | - |
| Isolate a server | No | SOC manager or system owner |
| Disable a user account | Yes, for confirmed compromise | - |
| Disable an executive or admin account | No | SOC manager, inform CISO |
| Block an external IP (time-limited) | Yes | - |
| Shut off VPN or a production service | No | CISO or IT operations lead |
| Reset the KRBTGT or rotate domain secrets | No | Identity team lead, incident lead |

## 5. Out-of-band communication

If an attacker may be inside email or chat (identity provider or mailbox compromise), switch the response to the pre-agreed out-of-band channel: [for example personal phones and a separate chat workspace]. Do not discuss the incident where the attacker might read it.

## 6. Review

Reviewed every 6 months, and whenever a contact changes role or number.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
