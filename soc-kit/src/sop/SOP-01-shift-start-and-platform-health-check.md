---
id: SOP-01
title: Shift Start and Platform Health Check
owner: SOC Lead
audience: L1 analyst, L2 analyst, shift lead
review: Every 6 months, and after any monitoring outage
summary: The first 30 minutes of every shift. Confirm the SOC can see, read the handover, and know what is open before touching the alert queue.
---
## 1. Purpose

A SOC that cannot see is worse than no SOC, because everyone believes they are protected. This procedure makes sure that at the start of every shift the monitoring platform is up, data is flowing from every critical source, automation is running, and the incoming analyst knows exactly what is open.

> WARNING: Never skip the health check, even when the queue is busy. A quiet dashboard can mean a quiet network or a broken pipeline. Only the health check tells you which.

## 2. Scope

- Every shift: day, evening, night, weekend and on-call start.
- The core SOC platforms: SIEM, EDR or XDR console, SOAR or automation platform, case management, threat intelligence platform, ticketing and the notification channels (chat, email, phone).
- Out of scope: fixing platform faults. The analyst detects, records and escalates. The platform owner fixes.

## 3. Roles and responsibilities

| Role | Responsibility |
|---|---|
| Incoming analyst (L1) | Runs every step in this procedure and records the result in the Daily Shift Report (TPL-01) |
| Outgoing analyst | Stays available for questions for 15 minutes after handover |
| Shift lead or L2 | Reviews any amber or red result, decides on escalation |
| SOC engineer or platform owner | Fixes platform faults, confirms when fixed |
| SOC Lead | Reviews health trends weekly, owns this procedure |

## 4. Prerequisites

- [ ] Working accounts on all SOC tools, with multi-factor authentication (MFA).
- [ ] Access to the health dashboard (one screen that shows the checks in section 6).
- [ ] The list of critical log sources with the maximum allowed silence for each (from the Log Source Register).
- [ ] The current escalation and contact matrix (GOV-04).
- [ ] The Daily Shift Report form (TPL-01) for today.

## 5. Trigger and frequency

| When | What |
|---|---|
| Start of every shift | Full check, sections 6.1 to 6.7 |
| Every 2 hours during the shift | Quick check: sections 6.2 and 6.3 only |
| After any platform change or outage | Full check |
| On-call start (after hours) | Sections 6.1, 6.2 and 6.6 from the mobile or remote console |

## 6. Procedure

### 6.1 Read the handover (5 minutes)

1. Open the Shift Handover (TPL-02) from the previous shift.
2. Read the open cases, ongoing incidents and pending actions.
3. Ask the outgoing analyst about anything unclear. Do this before they leave, not after.
4. Note every item you now own in your Daily Shift Report.

### 6.2 Platform status (5 minutes)

Check each component and record Green, Amber or Red.

| Component | Green | Amber | Red |
|---|---|---|---|
| SIEM search and dashboards | Loads, searches return in normal time | Slow searches, partial panels | Cannot log in or search |
| SIEM indexing and storage | Disk free above 25 percent | Disk free 15 to 25 percent | Disk free below 15 percent or indexing stopped |
| EDR or XDR console | Loads, agents reporting | Delayed telemetry | Console down |
| SOAR or automation | Last scheduled runs succeeded | Some failed runs | Engine down or all runs failing |
| Case management | Loads, new cases created by automation | Slow | Down |
| Threat intelligence feeds | Updated within expected time | One feed stale | All feeds stale |
| Notification channels | Test message received | Delayed | Not received |

> TIP: Build one health dashboard with a panel for each row in this table. The check should take minutes, not half an hour.

### 6.3 Data flow and silent sources (10 minutes)

1. Run the event volume query (Appendix A.1) for the last hour and compare with the same hour yesterday.
2. Run the silent source query (Appendix A.2). List every critical source that has sent nothing for longer than its allowed silence.
3. Check endpoint agent coverage: agents active against agents expected (Appendix A.3).
4. Record the numbers in TPL-01: events last hour, silent sources, agents active and total.

Decision:

- A drop of more than 30 percent in volume with no known reason: treat as Amber and tell the shift lead.
- A critical source silent beyond its limit: open a case with severity Medium (P3) and notify the source owner.
- Domain controllers, firewalls, identity provider or EDR all silent at once: Red. Escalate to the shift lead and platform owner immediately. An attacker may be disabling logging.

### 6.4 Overnight high-severity review (5 minutes)

1. List all alerts of High and Critical severity since the end of your last shift (Appendix A.4).
2. Confirm each one has an owner and a case, or was closed with a written reason.
3. Any High or Critical alert with no owner: take it now, before the normal queue.

### 6.5 Automation and integrations

1. Open the SOAR or automation run history. Count failed runs since the last shift.
2. Check that enrichment works: open one new alert and confirm reputation, geolocation and asset data were added.
3. Record failed runs in TPL-01 and raise a ticket for repeated failures.

### 6.6 Notification test

1. Send a test message to the SOC alert channel and the on-call channel.
2. Confirm it arrived. If not, use the backup channel (phone) until fixed.

### 6.7 Record and start the queue

1. Fill in the health section of TPL-01.
2. Post a one-line status in the SOC channel, for example: `Shift start 08:00, health GREEN, 0 silent sources, 412 of 415 agents, 3 open cases taken over.`
3. Start the alert queue (SOP-02, SOP-03).

## 7. Escalation

| Result | Action | Within |
|---|---|---|
| All Green | Record and continue | |
| Any Amber | Tell the shift lead, raise a ticket to the platform owner | 30 minutes |
| Any Red | Phone the shift lead and platform owner, start SOP-49 (SOC Business Continuity) if monitoring is blind | 15 minutes |
| Several critical sources silent together | Treat as a possible security incident (defence evasion). Open a case, severity High | 15 minutes |

## 8. Records

- Daily Shift Report (TPL-01), health section, every shift.
- Tickets raised for platform faults, with the ticket number in TPL-01.
- Keep records for at least 12 months. Auditors ask for proof that monitoring was checked.

## 9. Metrics

| Metric | Target |
|---|---|
| Health checks completed on time | 100 percent of shifts |
| Mean time to detect a silent critical source | Under 1 hour |
| Platform availability (SIEM searchable) | 99.5 percent per month |
| Endpoint agent coverage | 98 percent or more of expected agents active |

## 10. Common mistakes

- Starting the queue first and "doing health later". Later never comes on a busy shift.
- Checking only that the SIEM loads, not that data is arriving.
- Treating a silent source as a platform problem only. Log loss can be an attack.
- Not writing down the numbers. Without numbers there is no trend and no proof.

## 11. Related documents

- TPL-01 Daily Shift Report, TPL-02 Shift Handover
- SOP-02 Alert Queue Monitoring, SOP-03 Alert Triage and Classification, SOP-06 Shift Handover
- SOP-12 Log Source Health and Silent Source Response, SOP-49 SOC Business Continuity
- GOV-04 Escalation and Contact Matrix, Log Source Register

---page---

## Appendix A. Health queries

Index, table and field names are examples. Map them to your own platform and save each query as a named search, for example `HEALTH-01 Event volume`.

### A.1 Event volume, last hour against same hour yesterday

Splunk (SPL):

```spl
| tstats count where index=* earliest=-1h latest=now by index
| append [| tstats count where index=* earliest=-25h latest=-24h by index | eval period="yesterday"]
| eval period=coalesce(period,"now")
| chart sum(count) over index by period
```

Microsoft Sentinel (KQL):

```kql
union withsource=Table *
| where TimeGenerated > ago(25h)
| summarize Now=countif(TimeGenerated > ago(1h)), Yesterday=countif(TimeGenerated between (ago(25h) .. ago(24h))) by Table
| extend ChangePct = round(100.0 * (Now - Yesterday) / iif(Yesterday == 0, 1, Yesterday), 1)
| order by ChangePct asc
```

Elastic (ES|QL):

```sql
FROM logs-* | WHERE @timestamp > NOW() - 1 hour
| STATS events = COUNT(*) BY data_stream.dataset | SORT events ASC
```

IBM QRadar (AQL):

```sql
SELECT LOGSOURCENAME(logsourceid) AS source, COUNT(*) AS events
FROM events GROUP BY logsourceid ORDER BY events ASC LAST 1 HOURS
```

Wazuh (dashboard query on `wazuh-alerts-*`, then visualise count by `agent.name`):

```text
Time range: last 1 hour    Field: agent.name    Metric: count
```

### A.2 Silent sources (no events in the last 4 hours)

Splunk (SPL):

```spl
| tstats latest(_time) as last_seen where index=* by host, sourcetype
| eval silent_hours = round((now() - last_seen) / 3600, 1)
| where silent_hours > 4 | sort - silent_hours
```

Microsoft Sentinel (KQL):

```kql
union withsource=Table *
| where TimeGenerated > ago(7d)
| summarize LastSeen = max(TimeGenerated) by Computer, Table
| where LastSeen < ago(4h)
| extend SilentHours = datetime_diff('hour', now(), LastSeen)
| order by SilentHours desc
```

Elastic (ES|QL):

```sql
FROM logs-* | WHERE @timestamp > NOW() - 7 days
| STATS last_seen = MAX(@timestamp) BY host.name
| WHERE last_seen < NOW() - 4 hours | SORT last_seen ASC
```

IBM QRadar (AQL):

```sql
SELECT LOGSOURCENAME(logsourceid) AS source, MAX(starttime) AS last_seen
FROM events GROUP BY logsourceid
HAVING MAX(starttime) < NOW() - 14400000 LAST 7 DAYS
```

QRadar also raises the built-in health notification "Log source stopped sending events". Make sure it routes to the SOC queue.

Wazuh (command line on the manager):

```bash
/var/ossec/bin/agent_control -l | grep -v Active
```

### A.3 Endpoint agent coverage

Wazuh API:

```bash
curl -sk -H "Authorization: Bearer $TOKEN" "https://WAZUH-MANAGER:55000/agents/summary/status"
```

Microsoft Defender for Endpoint (KQL, advanced hunting):

```kql
DeviceInfo
| where Timestamp > ago(1d)
| summarize arg_max(Timestamp, *) by DeviceId
| summarize Total = count(), Active = countif(Timestamp > ago(1h))
```

Compare the result with the asset inventory count. A gap means unprotected machines.

### A.4 High and Critical alerts since the last shift

Splunk (SPL):

```spl
index=notable urgency IN ("high","critical") earliest=-12h
| table _time, rule_name, src, dest, user, owner, status
```

Microsoft Sentinel (KQL):

```kql
SecurityIncident
| where TimeGenerated > ago(12h) and Severity in ("High", "Critical")
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| project IncidentNumber, Title, Severity, Status, Owner = tostring(Owner.assignedTo)
```

IBM QRadar: open Offenses, filter Magnitude 7 or more, last 12 hours, and check the Assigned To column.

Wazuh (dashboard query):

```text
rule.level >= 12
```
