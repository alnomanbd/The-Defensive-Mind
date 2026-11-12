---
id: SOP-21
title: UEBA Anomaly Review
owner: SOC Lead
audience: L2 and L3 analysts
review: Every 12 months
summary: How to review user and entity behaviour analytics (UEBA) anomalies: treat them as leads to investigate, not alerts to act on, and turn real patterns into detections.
---
## 1. Purpose

User and entity behaviour analytics (UEBA) flags behaviour that is unusual for a user or system: a login at an odd hour, access to data they never touch, a sudden spike in activity. This procedure handles UEBA anomalies correctly: as signals to investigate, not verdicts, so they add value without flooding the queue.

> NOTE: A UEBA anomaly says "this is unusual", not "this is malicious". Unusual is often harmless (a new project, travel, a role change). Treat an anomaly as a lead that points you where to look, and confirm with evidence before acting.

## 2. Scope

UEBA anomalies from [the UEBA tool or SIEM module] for [ORGANISATION].

## 3. Procedure

### 3.1 Triage the anomaly

- [ ] What is unusual: the user, the entity, the time, the volume, the access?
- [ ] How far from normal is it, and over what period?
- [ ] Is there a benign explanation (role change, project, travel, a known job)?
- [ ] Does it line up with any other alert or signal on the same user or host?

### 3.2 Investigate

Use the anomaly to focus a normal investigation:

| Anomaly | Look at |
|---|---|
| Login at an unusual time or place | Sign-in logs, device, whether MFA was used |
| Access to data outside the user's role | What was accessed, and whether it is normal for a peer in that team |
| Spike in data downloaded or sent | Volume against baseline, destination, and the data exfiltration playbook |
| Unusual admin or privileged activity | What was done, under what change or ticket |

### 3.3 Decide

- [ ] Benign (explained): close with a note; consider tuning if the anomaly type is noisy.
- [ ] Suspicious: escalate and work it as the matching playbook (account compromise, insider, exfiltration).
- [ ] Insider concern about a named person: follow the privacy rules (GOV-10) and the insider process before targeted monitoring.

## 4. Turning anomalies into detections

When a UEBA pattern reliably indicates something real, convert it into a specific detection (SOP-13) rather than relying on the anomaly score alone. A precise rule is more trustworthy and less noisy than a general "unusual" flag.

## 5. Avoiding UEBA noise

- [ ] Tune or lower the weight of anomaly types that are mostly benign.
- [ ] Feed context (role changes, leavers, projects) into UEBA so it learns normal.
- [ ] Do not page on raw anomaly scores; route them to a review queue, not to on-call.

## 6. Records

Record the anomaly, the investigation, the verdict, and any detection or tuning follow-up.

## 7. Review

Reviewed every 12 months.
