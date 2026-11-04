---
id: TPL-02
title: Shift Handover
owner: SOC Lead
used: Every shift change and every on-call start and end, following SOP-06
summary: The written half of the handover. Prepare it 20 minutes before shift end, then go through it in a spoken handover.
---
## 1. Handover details

| Field | Entry |
|---|---|
| Date | |
| From shift and analyst | |
| To shift and analyst | |
| Handover time | |
| Spoken handover done (yes, no, how) | |

## 2. Ongoing incidents (discuss first)

| Incident ID | Severity | Incident lead | Current phase (triage, containment, eradication, recovery) | Next action and time | Next stakeholder update |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

## 3. Open cases handed over

| Case ID | Title | Severity | What was done | Exact next step | Deadline | New owner |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

## 4. Pending actions waiting on others

| Waiting on (team or person) | For what | Since | How to chase | Reference |
|---|---|---|---|---|
| | | | | |
| | | | | |

## 5. Platform health and known issues

| Item | Status (Green, Amber, Red) | Detail | Ticket |
|---|---|---|---|
| SIEM | | | |
| EDR or XDR | | | |
| SOAR or automation | | | |
| Log sources silent or degraded | | | |
| Other | | | |

## 6. Watch list for the next shift

Activity that is not an alert yet but should be watched, planned changes, expected noise, new advisories.

| Item | Why it matters | What to do if it happens |
|---|---|---|
| | | |
| | | |

## 7. Queue state at handover

| Severity | Alerts waiting | Oldest alert age |
|---|---|---|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |

## 8. Checklist before signing

- [ ] Every ongoing incident has a named lead and a next update time.
- [ ] Every open High and Critical case has a next step with a time.
- [ ] Pending actions show who is waited on and since when.
- [ ] Silent or broken sources are listed with tickets.
- [ ] Cases are reassigned in the case tool to the new owners.
- [ ] Incoming analyst repeated back the next steps for High and Critical items.

## 9. Acceptance

| Role | Name | Signature | Time |
|---|---|---|---|
| Outgoing analyst | | | |
| Incoming analyst (accepted) | | | |
| Shift lead (if an incident is ongoing) | | | |
