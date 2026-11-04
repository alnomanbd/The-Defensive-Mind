---
id: TPL-01
title: Daily Shift Report
owner: SOC Lead
used: Every shift, completed by the shift analyst, reviewed by the shift lead
summary: One page per shift that proves the SOC was watching, shows what it found, and feeds the weekly and monthly reports.
---
## 1. Shift details

| Field | Entry |
|---|---|
| Date | |
| Shift (day, evening, night, weekend, on-call) | |
| Start and end time | |
| Analyst(s) on shift | |
| Shift lead | |
| Handover received from (TPL-02 reference) | |

## 2. Platform health (from SOP-01)

| Check | Green, Amber or Red | Value | Ticket or note |
|---|---|---|---|
| SIEM search and dashboards | | | |
| SIEM storage, disk free percent | | | |
| EDR or XDR console | | | |
| Endpoint agents active of total | | ___ of ___ | |
| SOAR or automation, failed runs | | | |
| Case management | | | |
| Threat intelligence feeds updated | | | |
| Notification test received | | | |
| Silent critical log sources (list) | | | |
| Events last hour against yesterday, percent change | | | |

## 3. Alert statistics for this shift

| Measure | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Alerts received | | | | | |
| Alerts triaged | | | | | |
| True Positive (TP) | | | | | |
| Benign True Positive (BTP) | | | | | |
| False Positive (FP) | | | | | |
| Undetermined, escalated | | | | | |
| Still in queue at shift end | | | | | |

| Measure | Value |
|---|---|
| Oldest alert in queue at shift end (age) | |
| Mean time to acknowledge, High and Critical (minutes) | |
| Alerts outside their time box | |

## 4. Cases and incidents

| Case or incident ID | Title | Severity | Status (new, ongoing, closed) | Owner | Next step |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

## 5. Notable events

Short description of anything management or the next shift should know: confirmed attacks, blocked campaigns, unusual activity, outages.

| Time | What happened | Action taken |
|---|---|---|
| | | |
| | | |
| | | |

## 6. Requests raised this shift

| Type (tuning, exception, block, access, change, ticket) | Reference | Raised to | Status |
|---|---|---|---|
| | | | |
| | | | |

## 7. Threat intelligence and advisories reviewed

| Source or advisory | Relevant to us (yes, no) | Action (sweep, block, none) |
|---|---|---|
| | | |
| | | |

## 8. Proactive work

| Activity (hunt, tuning, documentation, training) | Time spent | Result |
|---|---|---|
| | | |
| | | |

## 9. Issues and improvement ideas

| Issue or idea | Suggested fix | Raised to |
|---|---|---|
| | | |
| | | |

## 10. Sign-off

| Role | Name | Signature | Time |
|---|---|---|---|
| Shift analyst | | | |
| Shift lead (reviewed) | | | |

> NOTE: Keep every daily report for at least 12 months. The totals in section 3 are summed into the Weekly SOC Report (TPL-03) and the Monthly SOC Report (TPL-04).
