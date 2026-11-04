---
id: SOP-03
title: Alert Triage and Classification
owner: SOC Lead
audience: L1 analyst, L2 analyst
review: Every 6 months, and when a new alert source is added
summary: One repeatable method to decide, in 5 to 15 minutes, whether an alert is real, how bad it is, and what happens next.
---
## 1. Purpose

Every alert gets the same treatment, no matter who is on shift. This procedure tells the analyst what to look at, in what order, how to classify the result, and how to write it down so the next person can trust it.

## 2. Scope

- All alerts that reach the SOC queue: SIEM correlation rules, EDR or XDR detections, email security, identity protection, network IDS, cloud security, user reports and alerts from threat intelligence.
- Out of scope: running the full investigation. Triage ends with a classification and a decision. Investigation follows the matching playbook (PB series).

## 3. Definitions

| Term | Meaning |
|---|---|
| True Positive (TP) | The alert is correct and the activity is malicious or a real policy violation |
| Benign True Positive (BTP) | The alert is correct, the activity really happened, but it is authorised or harmless (an admin running a scanner, an approved test) |
| False Positive (FP) | The alert is wrong: the activity is not what the rule thinks it is (bad parsing, wrong threshold, rule logic error) |
| Undetermined | Not enough information to decide within the triage time box. Escalate, never close |
| Enrichment | Adding context to an alert: reputation of an IP or domain, who the user is, what the host does, past alerts |
| Time box | The maximum time triage may take before the alert must be escalated |

> NOTE: The difference between BTP and FP matters. A BTP needs an exception for that activity. An FP needs the rule fixed. Mixing them up leaves broken rules in production.

## 4. Roles and responsibilities

| Role | Responsibility |
|---|---|
| L1 analyst | Triages Low and Medium alerts, first view on High, escalates Critical at once |
| L2 analyst | Confirms L1 escalations, triages High, decides on containment requests |
| L3 or incident lead | Takes Critical and Undetermined cases that L2 cannot close |
| Detection engineer | Receives FP and BTP tuning requests (SOP-10) |
| Shift lead | Watches the time boxes and the queue age |

## 5. Time boxes

| Alert severity | Acknowledge within | Triage decision within | If not decided |
|---|---|---|---|
| Critical | 5 minutes | 15 minutes | Escalate to L2 and shift lead by phone |
| High | 15 minutes | 30 minutes | Escalate to L2 |
| Medium | 1 hour | 2 hours | Escalate to L2 |
| Low | 4 hours | Next business day | Ask L2 in the next queue review |

## 6. Procedure

### 6.1 Take ownership

1. Assign the alert to yourself in the SIEM or case tool before you start. Two analysts on one alert wastes time; no analyst on one alert loses it.
2. Note the start time.

### 6.2 Understand the alert (2 minutes)

1. Read the rule name and description. What behaviour is it designed to catch?
2. Note the MITRE ATT&CK technique if the rule has one.
3. Read the raw event, not only the summary. Check that the fields were parsed correctly. Many false positives start here.

### 6.3 Answer the five questions (5 minutes)

| Question | Where to look |
|---|---|
| Who? User account, its role, is it privileged, is it a service account | Identity provider, HR or directory data, asset and identity enrichment |
| What? Process, command line, file, URL, email subject | Raw event, EDR process tree |
| Where? Host or service, how critical it is, internet facing or internal | Asset inventory, CMDB, crown jewel list |
| When? Time, business hours or not, first time or repeated | Alert history for the same user, host and rule |
| How bad could it be? Did it succeed, was data touched, was it blocked | Security control action field, follow-on events |

### 6.4 Enrich (5 minutes)

1. Indicators: check IPs, domains, URLs and file hashes against the threat intelligence platform and reputation services (SOP-04).
2. History: search 7 days back for the same user, host and indicator (Appendix A.1).
3. Neighbours: what else happened on the same host 30 minutes before and after (Appendix A.2).
4. Known activity: check the change calendar, the approved exceptions list and the known false positive list.

> WARNING: Never paste internal data, user names, or suspected malware samples into public online services. Use only the services the SOC has approved, and submit hashes, not files, unless the policy allows it.

### 6.5 Classify

Use this decision table in order. Stop at the first row that matches.

| Situation | Classification | Next step |
|---|---|---|
| Evidence of compromise, malicious tool, data theft, or success after attack attempts | TP | Raise severity if needed, open an incident case, start the playbook, escalate per section 7 |
| Activity happened and is confirmed authorised (change ticket, owner confirmed in writing) | BTP | Close with the evidence of authorisation, raise an exception request if it will repeat |
| Rule logic or parsing is wrong, activity is not what the rule claims | FP | Close, raise a tuning request (SOP-10) with the query that shows why |
| Blocked attack with no follow-on success (for example blocked internet scan) | TP, blocked | Close as TP blocked, add the source to the watch list, no incident case |
| Cannot decide inside the time box | Undetermined | Escalate to L2 with what you found. Never close |

### 6.6 Set severity

Start from the rule's default severity, then adjust:

| Raise one level if | Lower one level if |
|---|---|
| Privileged or executive account involved | Test or lab system with no real data |
| Crown jewel system, production database or domain controller | Action was blocked and there is no follow-on activity |
| Success after failures, or several hosts involved | Activity is contained to one non-critical host and fully explained |
| Data leaving the organisation | |

Severity definitions and response times are in GOV-03.

### 6.7 Write the triage note

Every closed or escalated alert gets a note in this format. A good note lets someone who was not there understand the decision in 30 seconds.

```text
Verdict: TP | BTP | FP | Undetermined
Severity: Critical | High | Medium | Low
Summary: one sentence of what happened
Evidence: the 2 to 5 facts that support the verdict (with query or event IDs)
Enrichment: reputation and context results
Action taken: closed | escalated to <name> | case <number> opened | tuning request <number>
Analyst / time spent: <name>, <minutes>
```

### 6.8 Close or hand on

1. Closed alerts: link any tuning or exception request.
2. Escalated alerts: notify the receiving analyst directly (chat or phone for High and Critical), not only by reassigning.
3. Incident cases: link the alert, attach the evidence, name the playbook.

## 7. Escalation

| Condition | Escalate to | How |
|---|---|---|
| Any confirmed TP of High or Critical | L2 and shift lead | Chat and phone |
| Undetermined at the end of the time box | L2 | Reassign plus chat |
| Several alerts that look connected (same user, host or indicator) | L2 | One case with all alerts linked |
| Possible data breach or personal data involved | Incident lead, who informs privacy or legal per GOV-06 | Phone |
| The SOC's own tools or accounts are involved | SOC Lead directly | Phone, do not write details in shared channels |

## 8. Records

- Triage note on every alert.
- Case record for every TP that becomes an incident.
- Tuning and exception requests linked to the alert.
- Daily totals in TPL-01: alerts triaged, TP, BTP, FP, Undetermined.

## 9. Metrics

| Metric | Target |
|---|---|
| Mean time to acknowledge (MTTA), Critical | Under 5 minutes |
| Alerts triaged inside the time box | 95 percent or more |
| False positive rate per rule | Under 30 percent; rules above this go to weekly tuning |
| Escalations returned by L2 for missing information | Under 10 percent |
| Quality review score (SOP-50) | 90 percent or more |

## 10. Common mistakes

- Reading the alert title and skipping the raw event.
- Closing as FP when the activity is real but authorised (that is BTP).
- Closing an alert because "it was blocked" without checking for other attempts that were not blocked.
- Triage notes that say only "checked, fine".
- Working the newest alert first. Work highest severity first, then oldest first.
- Asking the user "did you do this?" by email when the account may be compromised. Call them on a known number.

## 11. Related documents

- SOP-02 Alert Queue Monitoring, SOP-04 Alert Enrichment, SOP-05 Severity Assignment and Escalation
- SOP-08 Case Management, SOP-10 False Positive Handling and Tuning Requests, SOP-50 Quality Assurance
- GOV-03 Severity, Priority and SLA Standard
- All PB playbooks

---page---

## Appendix A. Triage queries

### A.1 Seven-day history for a user, host or indicator

Splunk (SPL):

```spl
index=* (user="jdoe" OR src="203.0.113.10" OR dest="203.0.113.10" OR host="WS-0142") earliest=-7d
| stats count min(_time) as first max(_time) as last values(sourcetype) as sources by index
| convert ctime(first) ctime(last)
```

Microsoft Sentinel (KQL):

```kql
search in (SecurityEvent, SigninLogs, DeviceNetworkEvents, CommonSecurityLog) "jdoe" or "203.0.113.10"
| where TimeGenerated > ago(7d)
| summarize Count = count(), First = min(TimeGenerated), Last = max(TimeGenerated) by $table
```

Elastic (KQL in Discover, last 7 days):

```text
user.name : "jdoe" or source.ip : "203.0.113.10" or destination.ip : "203.0.113.10" or host.name : "WS-0142"
```

IBM QRadar (AQL):

```sql
SELECT QIDNAME(qid) AS event, sourceip, destinationip, username, COUNT(*) AS n
FROM events
WHERE username = 'jdoe' OR sourceip = '203.0.113.10' OR destinationip = '203.0.113.10'
GROUP BY qid, sourceip, destinationip, username
ORDER BY n DESC LAST 7 DAYS
```

Wazuh (dashboard query on `wazuh-alerts-*`):

```text
data.srcuser:"jdoe" or data.srcip:"203.0.113.10" or agent.name:"WS-0142"
```

### A.2 Everything on one host, 30 minutes around the alert

Splunk (SPL):

```spl
index=* host="WS-0142" earliest="11/04/2026:09:30:00" latest="11/04/2026:10:30:00"
| table _time, sourcetype, user, process, CommandLine, dest, action | sort _time
```

Microsoft Defender for Endpoint (KQL):

```kql
let t = datetime(2026-11-04 10:00:00);
union DeviceProcessEvents, DeviceNetworkEvents, DeviceFileEvents, DeviceRegistryEvents
| where DeviceName =~ "ws-0142" and Timestamp between ((t - 30m) .. (t + 30m))
| project Timestamp, ActionType, FileName, ProcessCommandLine, RemoteIP, RemoteUrl, InitiatingProcessFileName
| order by Timestamp asc
```

IBM QRadar (AQL):

```sql
SELECT DATEFORMAT(starttime, 'HH:mm:ss') AS t, QIDNAME(qid) AS event, username, sourceip, destinationip
FROM events WHERE sourceip = '10.20.30.42' OR destinationip = '10.20.30.42'
START '2026-11-04 09:30' STOP '2026-11-04 10:30'
```

Wazuh (dashboard query, set the time picker to the 1-hour window):

```text
agent.name:"WS-0142"
```

### A.3 Did a login succeed after failures?

Splunk (SPL), Windows:

```spl
index=wineventlog (EventCode=4625 OR EventCode=4624) user="jdoe" earliest=-24h
| stats count(eval(EventCode=4625)) as failed count(eval(EventCode=4624)) as success
  min(_time) as first max(_time) as last by user, src
| where failed > 5 AND success > 0
```

Microsoft Entra ID (KQL):

```kql
SigninLogs
| where TimeGenerated > ago(24h) and UserPrincipalName =~ "jdoe@example.com"
| summarize Failed = countif(ResultType != "0"), Success = countif(ResultType == "0") by IPAddress, AppDisplayName
| where Failed > 5 and Success > 0
```

IBM QRadar (AQL):

```sql
SELECT username, sourceip,
  SUM(CASE WHEN QIDNAME(qid) ILIKE '%fail%' THEN 1 ELSE 0 END) AS failed,
  SUM(CASE WHEN QIDNAME(qid) ILIKE '%success%' THEN 1 ELSE 0 END) AS success
FROM events WHERE CATEGORYNAME(category) ILIKE '%auth%' AND username = 'jdoe'
GROUP BY username, sourceip LAST 24 HOURS
```

Wazuh (dashboard query), Linux SSH:

```text
rule.groups:"authentication_success" and data.srcip:"203.0.113.10"
```
