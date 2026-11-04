---
id: SOP-02
title: Alert Queue Monitoring
owner: SOC Lead
audience: L1 analyst, L2 analyst, shift lead
review: Every 6 months
summary: How the SOC watches the alert queue during a shift: who owns it, which alert to pick next, and what to do when the queue grows faster than the team can work it.
---
## 1. Purpose

The alert queue is the SOC's main work list. If nobody owns it, alerts age, Service Level Agreements (SLAs) are missed, and real attacks wait behind noise. This procedure sets one owner, one picking order, and clear actions when the queue is under pressure.

## 2. Scope

- All alert queues the SOC watches: SIEM alerts or notables, EDR or XDR detections, email security, identity protection, cloud security, network IDS, user-reported phishing, and alerts created by automation.
- Every hour of SOC coverage, including on-call hours.

## 3. Roles and responsibilities

| Role | Responsibility |
|---|---|
| Queue owner (named L1 for each shift or each hour) | Watches the queue, acknowledges new alerts, assigns or picks work, raises pressure alerts |
| L1 analysts | Pick and triage alerts (SOP-03) |
| L2 analysts | Take escalations, support when the queue is under pressure |
| Shift lead | Watches SLA timers and queue age, rebalances work, calls for help |
| SOC Lead | Reviews queue metrics weekly and fixes the causes of overload |

## 4. One queue view

Before the procedure works, the SOC needs one place to see all alerts. Either all tools send their alerts to the SIEM or case tool, or the queue owner keeps every console open in a fixed order.

| Queue view must show | Why |
|---|---|
| Severity | To pick the right alert first |
| Age (time since created) | To meet the SLA |
| Owner | To avoid double work and orphans |
| Status (new, in progress, escalated, closed) | To know what is moving |
| Source tool and rule name | To spot noisy rules and broken sources |

> TIP: Sort the queue view by severity first and age second. Make this the default view for everyone.

## 5. Procedure

### 5.1 Start of queue ownership

1. Confirm in the SOC channel that you own the queue, for example: `Queue owner 08:00 to 12:00: <name>`.
2. Note the queue count and the oldest alert age in TPL-01.

### 5.2 Picking order

Always pick in this order:

1. Critical alerts, oldest first.
2. High alerts, oldest first.
3. Alerts linked to an ongoing incident (same user, host or indicator), whatever their severity.
4. Medium alerts, oldest first.
5. Low alerts, oldest first, or in batches by rule (section 5.4).

> WARNING: Do not skip to easy alerts to make the numbers look good. The oldest High alert is always more important than five quick Low alerts.

### 5.3 Acknowledge and assign

1. Acknowledge every Critical alert within 5 minutes and every High within 15 minutes, even if you cannot start it at once.
2. Assign the alert to the analyst who will work it. Never leave a started alert unassigned.
3. If an alert needs a skill you do not have (malware, cloud, a specific application), assign it to L2 with a note, do not leave it waiting.

### 5.4 Batch handling of Low alerts

Low alerts from the same rule can often be handled together:

1. Group by rule name and by the main field (source IP, user, host).
2. Triage one alert from each group fully.
3. If the rest of the group has the same pattern, close them together with one note that references the fully triaged alert.
4. If the same rule produces more than 50 Low alerts a day, raise a tuning request (SOP-10).

### 5.5 Watch the queue every 30 minutes

The queue owner checks:

- [ ] Any Critical or High alert unacknowledged
- [ ] Any alert older than its SLA
- [ ] Any alert in progress for more than 2 hours with no update
- [ ] A sudden jump in alerts from one rule or one source (possible attack or broken rule)
- [ ] Alerts assigned to people who are off shift

### 5.6 Queue pressure levels

| Level | Condition | Action |
|---|---|---|
| Normal | No alert past SLA, queue stable or falling | Continue |
| Busy | Medium alerts past SLA, or queue growing for 1 hour | Shift lead moves an L2 to help with triage, pause non-urgent project work |
| Overloaded | High alerts past SLA, or more than 2 times normal volume | Shift lead informs the SOC Lead, calls on-call or off-shift staff, batches Low alerts, starts looking for a single cause |
| Storm | One rule or one source producing hundreds of alerts | Treat the storm as one case: confirm if it is an attack or a broken rule. If broken, the detection engineer applies an emergency suppression with an expiry (SOP-10 section 6.6) |

### 5.7 End of queue ownership

1. Hand the queue to the next owner with the count, the oldest alert, and any storm or pressure in progress.
2. At shift end, the queue state goes into TPL-02 Shift Handover.

## 6. Escalation

| Condition | Escalate to | Within |
|---|---|---|
| Critical alert not acknowledged in 5 minutes | Shift lead by phone | Immediately |
| Queue at Overloaded level | SOC Lead | 30 minutes |
| Storm with unknown cause | L2 and detection engineer | 15 minutes |
| Alert tool or queue view down | Platform owner, follow SOP-49 | 15 minutes |

## 7. Records

- Queue owner announcements in the SOC channel.
- Queue counts and oldest age in TPL-01 at start and end of shift.
- Pressure level changes recorded in TPL-01 notable events.

## 8. Metrics

| Metric | Target |
|---|---|
| Mean time to acknowledge (MTTA), Critical | Under 5 minutes |
| Mean time to acknowledge, High | Under 15 minutes |
| Alerts past SLA at shift end | Zero High or Critical |
| Hours at Overloaded level per month | Falling month on month |
| Alerts closed in batch with a reference note | Tracked, reviewed weekly |

## 9. Common mistakes

- Several people watching the queue and nobody owning it.
- Picking newest first, so old alerts never get done.
- Closing Low alerts in bulk without triaging one from each group.
- Living with a storm for days instead of fixing or suppressing the rule.
- Leaving alerts assigned to an analyst who went home.

## 10. Related documents

- SOP-01 Shift Start and Platform Health Check, SOP-03 Alert Triage and Classification, SOP-05 Severity Assignment and Escalation
- SOP-10 False Positive Handling and Tuning Requests, SOP-49 SOC Business Continuity
- TPL-01 Daily Shift Report, TPL-02 Shift Handover, GOV-03 Severity, Priority and SLA Standard

---page---

## Appendix A. Queue queries

### A.1 Open alerts by severity and age

Splunk Enterprise Security (SPL):

```spl
`notable` | search status_label IN ("New","In Progress")
| eval age_min = round((now() - _time) / 60)
| stats count max(age_min) as oldest_min by urgency, owner
| sort - urgency
```

Microsoft Sentinel (KQL):

```kql
SecurityIncident
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| where Status in ("New", "Active")
| extend AgeMin = datetime_diff('minute', now(), CreatedTime)
| summarize Open = count(), OldestMin = max(AgeMin) by Severity, Owner = tostring(Owner.assignedTo)
```

IBM QRadar (Offenses tab): filter Status Open, sort by Magnitude then Start Date, and show the Assigned To column. The same list is available from the API:

```bash
curl -s -H "SEC: $QRADAR_TOKEN" "https://QRADAR/api/siem/offenses?filter=status%3DOPEN&fields=id,magnitude,start_time,assigned_to,description"
```

Elastic Security: Alerts page, filter `kibana.alert.workflow_status : "open"`, group by `kibana.alert.severity`.

Wazuh (dashboard query, last 24 hours, sort by `rule.level`):

```text
rule.level >= 7
```

### A.2 Alert storm detection: rules with a sudden jump

Splunk (SPL):

```spl
`notable` earliest=-24h
| bin _time span=1h | stats count by _time, rule_name
| eventstats avg(count) as avg stdev(count) as sd by rule_name
| where count > avg + 3*sd AND count > 20
```

Microsoft Sentinel (KQL):

```kql
SecurityAlert
| where TimeGenerated > ago(24h)
| summarize Count = count() by bin(TimeGenerated, 1h), AlertName
| summarize Avg = avg(Count), Max = max(Count) by AlertName
| where Max > 3 * Avg and Max > 20
```

IBM QRadar (AQL):

```sql
SELECT RULENAME(creeventlist) AS rule, COUNT(*) AS hits
FROM events WHERE creeventlist IS NOT NULL
GROUP BY creeventlist ORDER BY hits DESC LAST 1 HOURS
```

Wazuh (dashboard): visualise count by `rule.id` with a 1-hour interval over the last 24 hours, and look for a rule that jumps.
