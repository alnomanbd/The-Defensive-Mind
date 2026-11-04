---
id: SOP-08
title: Case Management (open, merge, run, close)
owner: SOC Lead
audience: L1 analyst, L2 analyst, incident leads
review: Every 12 months
summary: When an alert becomes a case, how to name, link, work and close it, and what a complete case record must contain.
---
## 1. Purpose

The case is the SOC's memory. It holds what happened, what was decided and why, and the evidence. A good case can be picked up by any analyst at any hour and survive an audit or a court a year later. This procedure sets the rules for every case.

## 2. Scope

- All security cases in the case management tool (for example TheHive, DFIR-IRIS, Jira Service Management, ServiceNow SecOps, Splunk SOAR, Microsoft Sentinel incidents, IBM QRadar SOAR).
- Alerts that are closed during triage without a case are covered by SOP-03.

## 3. Definitions

| Term | Meaning |
|---|---|
| Alert | A single detection from a tool |
| Case | A record of investigation work, holding one or more related alerts |
| Incident | A case confirmed as a security incident (a TP that affects confidentiality, integrity or availability) |
| Observable | An indicator or entity stored in the case (IP, domain, hash, user, host) |
| Task | A piece of work inside a case with its own owner (for example "collect memory from WS-0142") |

## 4. When to open a case

| Situation | Case needed |
|---|---|
| TP of any severity that needs more than closing the alert | Yes |
| Undetermined alert escalated to L2 | Yes |
| Several related alerts | Yes, one case for all |
| Report from a user, IT, vendor or outside party | Yes |
| Threat hunt finding | Yes |
| FP or BTP closed during triage | No, the triage note is enough |
| TP blocked with no follow-on (for example blocked scan) | No, close as TP blocked |

## 5. Procedure

### 5.1 Open the case

1. Search first. If an open case already covers the same user, host, indicator or campaign, add to it instead of opening a new one.
2. Create the case from the alert so the link is kept.
3. Title format: `<Type> - <main entity> - <short description>`, for example `Account compromise - jdoe@example.com - login from new country after MFA push spam`.
4. Fill the mandatory fields:

| Field | Content |
|---|---|
| Severity | P1 to P4 (SOP-05) |
| Classification | Incident type from the taxonomy in GOV-06 (phishing, malware, account compromise, data loss, denial of service, insider, policy violation, other) |
| Owner | One named analyst |
| TLP and PAP | How widely the case content may be shared (Traffic Light Protocol) and what actions are allowed on the indicators (Permissible Actions Protocol) |
| MITRE ATT&CK | Techniques seen, when known |
| Playbook | The PB playbook being followed |
| Affected assets | Hosts, users, applications, data |
| Detection source | Rule or report that started the case |

### 5.2 Work the case

1. Add tasks from the playbook. Each task has an owner and a due time.
2. Add observables and mark which are confirmed malicious (IOC) and which are only seen.
3. Write work notes as you go, in time order, with facts, queries used, and results. Notes are written for a stranger reading them later.
4. Attach evidence or record where it is stored (SOP-36), with hashes.
5. Keep the case status current:

| Status | Meaning |
|---|---|
| New | Created, not started |
| In progress | Being worked |
| Waiting | Blocked on another team or the user; note who and since when |
| Contained | Threat stopped from spreading, eradication not finished |
| Resolved | Threat removed and systems recovered; awaiting review |
| Closed | Final, with resolution and lessons recorded |

### 5.3 Merge and link

1. Merge cases that turn out to be the same incident. Keep the older case number and note the merge in both.
2. Link related but separate cases (for example the same phishing campaign hitting two business units).
3. Never delete a case. Close duplicates as "Duplicate of <case>".

### 5.4 Communicate from the case

1. Requests to other teams go out as tickets referenced in the case.
2. Updates to stakeholders follow SOP-43 and are copied into the case.
3. Do not put passwords, secrets or full personal data in case notes. Reference where they are stored securely.

### 5.5 Close the case

A case can be closed only when every item below is done:

- [ ] Final classification set: TP incident, TP blocked, BTP, FP, or Duplicate
- [ ] Final severity set and any changes recorded
- [ ] Root cause recorded (how it started), or "unknown" with the reason
- [ ] All tasks closed or moved to a follow-up ticket with an owner
- [ ] Confirmed IOCs submitted to the threat intelligence platform (SOP-32)
- [ ] Containment actions reversed where needed (host released, account re-enabled) and recorded
- [ ] Incident report written for P1 and P2 (TPL-08)
- [ ] Post-incident review held or scheduled for P1 and P2 (SOP-44)
- [ ] Detection gaps or tuning requests raised (SOP-10, TPL-21)
- [ ] Resolution summary written: three to five sentences a manager can read

P1 and P2 cases are closed by the incident lead or the SOC Lead, not by the analyst alone.

## 6. Case quality

The shift lead or SOC Lead reviews a sample of closed cases each week using SOP-50. A case passes when someone who was not involved can answer: what happened, how we know, what we did, and what changed afterwards.

## 7. Retention

Keep case records according to GOV-07, at least 12 months, and longer for incidents with legal, regulatory or HR follow-up. Cases under legal hold are never deleted (SOP-41).

## 8. Metrics

| Metric | Target |
|---|---|
| Cases with all mandatory fields | 100 percent |
| Mean time to resolve (MTTR) by severity | P1 under 24 hours to containment, P2 under 3 days, P3 under 10 days |
| Cases in Waiting more than 5 days | Reviewed weekly |
| Closed cases passing quality review | 90 percent or more |
| Cases reopened after closure | Under 5 percent |

## 9. Common mistakes

- One alert, one case, so a single attack ends up in ten separate cases.
- Notes like "checked logs, nothing found" without saying which logs, which time range, which query.
- Cases left "In progress" for weeks with no update.
- Closing without the root cause or without reversing containment.
- Pasting credentials or full customer data into notes.

## 10. Related documents

- SOP-03 Alert Triage and Classification, SOP-05 Severity Assignment and Escalation, SOP-32 IOC Lifecycle, SOP-36 Evidence Collection and Chain of Custody, SOP-43 Incident Communication, SOP-44 Post-Incident Review, SOP-50 Quality Assurance
- TPL-08 Incident Report: Final, TPL-09 Incident Timeline and Decision Log
- GOV-06 Incident Response Policy (incident taxonomy), GOV-07 Log Management and Retention Policy
