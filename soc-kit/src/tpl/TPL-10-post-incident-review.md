---
id: TPL-10
title: Post-Incident Review
owner: SOC Lead
used: For every P1 and P2 incident within 10 working days of resolution, and for any incident with a lesson worth sharing; following SOP-44
summary: A blameless review of an incident. It finds what worked, what did not, and why, and turns that into owned, dated actions. It is about improving the system, not about finding someone to blame.
---
## 1. Review details

| Field | Entry |
|---|---|
| Incident ID and title | |
| Severity | |
| Review date | |
| Facilitator (not the incident lead) | |
| Note taker | |
| Participants (names and roles) | |
| Inputs reviewed | Incident timeline (TPL-09), final report draft (TPL-08), case record |

## 2. Ground rules (read out at the start)

- [ ] We assume everyone acted in good faith with the information they had at the time.
- [ ] We look for causes in systems, processes and tools, not in people.
- [ ] Every voice counts, whatever the role or seniority.
- [ ] What is said here is used to improve, not for performance reviews.
- [ ] We leave with actions that have one owner and one due date each.

## 3. Incident summary

Two minutes, read by the incident lead: what happened, impact, key times.

| Summary |
|---|
| |

| Measure | Value | Target |
|---|---|---|
| Time to detect | | |
| Time to contain | | |
| Time to recover | | |

## 4. Walk through the timeline

Go through TPL-09 in order. At each key point ask: what did we know, what did we do, what would have helped?

| Point in the timeline | What we knew | What we did | What would have helped |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

## 5. Questions to answer

| Question | Answer |
|---|---|
| Could we have prevented it? What control was missing or failed? | |
| Could we have detected it earlier? Which signal was there but missed or not collected? | |
| Did the alert reach the right person fast enough? | |
| Did the playbook fit the incident? What steps were missing, wrong or slow? | |
| Did people have the access and tools they needed when they needed them? | |
| Were decisions made quickly and by the right people? | |
| Was communication clear, on time and to the right audience? | |
| Was evidence collected and preserved correctly? | |
| Did automation help or get in the way? | |
| Did any third party (vendor, provider) help or slow us down? | |

## 6. What went well

| Item | Keep doing by |
|---|---|
| | |
| | |
| | |

## 7. What did not go well

| Item | Root cause (why did this happen?) |
|---|---|
| | |
| | |
| | |

> TIP: For each item, ask "why" until the answer is something you can change: a process, a tool, a missing log, a missing permission, a missing skill. Usually that takes three to five whys.

## 8. Actions

| No. | Action | Type (prevent, detect, respond, recover, communicate) | Owner | Due date | Tracking reference |
|---|---|---|---|---|---|
| A1 | | | | | |
| A2 | | | | | |
| A3 | | | | | |
| A4 | | | | | |
| A5 | | | | | |

Actions to consider: new or tuned detection rule (TPL-21), playbook update, new log source (TPL-26), access or tool for responders, training, control change, contract change with a vendor, risk acceptance (TPL-24) where nothing will be changed.

## 9. Documents to update

- [ ] Playbook used
- [ ] SOPs used
- [ ] Escalation and contact matrix
- [ ] Detection register and ATT&CK coverage
- [ ] Risk register
- [ ] Training material (add this incident as a case study)

## 10. Follow-up

| Item | Entry |
|---|---|
| Action review date (check progress) | |
| Review shared with | |
| Review stored at | |
| Facilitator sign-off | |
