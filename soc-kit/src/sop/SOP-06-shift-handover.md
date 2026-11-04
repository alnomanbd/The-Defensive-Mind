---
id: SOP-06
title: Shift Handover
owner: SOC Lead
audience: All SOC analysts, shift leads, on-call staff
review: Every 6 months
summary: How open work passes from one shift to the next without anything being dropped, forgotten or done twice.
---
## 1. Purpose

Most incidents that go wrong in a SOC go wrong at a shift change: a containment step nobody finished, a case nobody owned overnight, a warning nobody passed on. This procedure makes the handover written, spoken and confirmed every time.

## 2. Scope

- Every change of shift, including the start and end of on-call cover and weekend handovers.
- Handover of a single major incident between incident leads (section 6.5).

## 3. Principles

- Written and spoken. The written handover is the record; the spoken handover catches what the form does not.
- The outgoing analyst owns the work until the incoming analyst says "accepted".
- Every open item has one named owner after handover. "The team" is not an owner.
- Nothing of High or Critical severity is handed over by message only.

## 4. Roles and responsibilities

| Role | Responsibility |
|---|---|
| Outgoing analyst | Prepares TPL-02 at least 20 minutes before shift end, leads the spoken handover, stays 15 minutes for questions |
| Incoming analyst | Reads TPL-02 before the meeting, asks questions, confirms acceptance, runs SOP-01 |
| Outgoing shift lead | Checks that every High and Critical item has an owner and a next step |
| Incoming shift lead | Accepts ongoing incidents, reassigns work across the new shift |
| On-call analyst | Receives a handover at the start of cover and gives one back at the end |

## 5. Timing

| Time before shift end | Step |
|---|---|
| 30 minutes | Stop picking up new Low alerts unless the queue is empty |
| 20 minutes | Complete TPL-02 |
| 10 minutes | Spoken handover with the incoming analyst or shift lead |
| 0 | Incoming analyst confirms acceptance in the case tool and SOC channel |
| Plus 15 minutes | Outgoing analyst stays reachable |

## 6. Procedure

### 6.1 Prepare the written handover (outgoing)

1. Open TPL-02 Shift Handover.
2. Fill in platform health: anything Amber or Red, with ticket numbers.
3. List every open case you own: case number, severity, status, the exact next step and any deadline.
4. List pending actions waiting on others: who, what, since when, how to chase.
5. List ongoing incidents with the current incident lead and the next update time.
6. Add watch items: suspicious activity not yet an alert, planned changes tonight, expected noise, threat advisories.
7. Add queue state: alerts waiting by severity and the oldest alert age.

### 6.2 Spoken handover (both)

1. Go through ongoing incidents and High or Critical cases first, then the rest.
2. For each item, the outgoing analyst says what it is, what was done, and what must happen next.
3. The incoming analyst repeats the next step back in their own words.
4. Agree any change of owner there and then and update the case tool during the call.

> TIP: For a remote team, use a short video call. Typing a handover in chat is not a spoken handover.

### 6.3 Confirm acceptance (incoming)

1. Reassign every accepted case to yourself (or the agreed owner) in the case tool.
2. Post in the SOC channel, for example: `Handover accepted 20:00. 4 cases taken (1 High), 1 incident ongoing (INC-1042, lead: A. Rahman, next update 21:00).`
3. Sign TPL-02 (name and time).
4. Start SOP-01 Shift Start and Platform Health Check.

### 6.4 When the incoming analyst does not arrive

1. The outgoing analyst does not leave.
2. Phone the incoming analyst, then the shift lead, then the SOC Lead.
3. If no cover is found within 30 minutes, the SOC Lead decides: extend the shift, call in on-call, or move to reduced coverage with the escalation matrix.
4. Record the gap in TPL-01 and in the next weekly report.

### 6.5 Handover of a major incident

1. The current incident lead writes a short situation summary (TPL-11 Situation Report).
2. Both leads join the incident bridge; the outgoing lead hands over in front of the team.
3. The new lead states "I have the incident" on the bridge and in the incident channel.
4. The incident timeline (TPL-09) records the time and the names.

## 7. Quality checks

The shift lead checks a sample of handovers each week:

- [ ] Every open High and Critical case has an owner and a next step with a time.
- [ ] Pending actions show who is waited on and since when.
- [ ] Acceptance was confirmed within 10 minutes of shift start.
- [ ] No item was lost between two handovers (compare two consecutive forms).

## 8. Records

- TPL-02 Shift Handover, one per shift, kept for at least 12 months.
- Acceptance message in the SOC channel.
- Case tool assignment history.

## 9. Metrics

| Metric | Target |
|---|---|
| Handovers completed on time | 100 percent |
| Items dropped between shifts (found in review) | Zero |
| Incoming acceptance within 10 minutes | 95 percent |

## 10. Common mistakes

- "Nothing to hand over" while the queue holds 40 alerts.
- Next steps written as "monitor" or "follow up" with no action and no time.
- Leaving before the incoming analyst confirms.
- Handing over an incident in chat at 3 a.m. with no call.
- Forgetting pending requests to other teams, so nobody chases them.

## 11. Related documents

- TPL-02 Shift Handover, TPL-01 Daily Shift Report, TPL-09 Incident Timeline and Decision Log, TPL-11 Situation Report
- SOP-01 Shift Start and Platform Health Check, SOP-07 On-Call and After-Hours Response, SOP-08 Case Management, SOP-42 Major Incident and War Room
