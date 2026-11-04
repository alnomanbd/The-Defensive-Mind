---
id: SOP-09
title: Daily, Weekly, Monthly, Quarterly and Annual Reporting
owner: SOC Lead
audience: Shift analysts, shift leads, SOC Lead, SOC manager
review: Every 12 months
summary: Which reports the SOC produces, for whom, when, with which numbers, and where the numbers come from.
---
## 1. Purpose

Reports prove the SOC is working, show management where the risk is, and justify budget. Without a fixed reporting rhythm, numbers are collected in a rush at month end and nobody trusts them. This procedure sets the rhythm and the data sources.

## 2. Report calendar

| Report | Template | Prepared by | For | When | Length |
|---|---|---|---|---|---|
| Daily Shift Report | TPL-01 | Shift analyst | Shift lead, next shift, SOC Lead | End of every shift | 1 to 2 pages |
| Weekly SOC Report | TPL-03 | Shift lead or SOC Lead | SOC team, IT operations lead, CISO | Every Monday for the previous week | 2 pages |
| Monthly SOC Report | TPL-04 | SOC Lead | CISO, IT management, risk | By the 5th working day of the month | 4 to 6 pages |
| Quarterly Executive Report | TPL-05 | SOC Lead with CISO | Executive management, board risk committee | Within 10 working days after quarter end | 2 pages plus appendix |
| Annual SOC Report | TPL-06 | SOC Lead with CISO | Executive management, board, auditors | Within 1 month after year end | 6 to 10 pages |
| Incident reports | TPL-07, TPL-08 | Incident lead | Per SOP-43 | During and after each P1 and P2 | As needed |
| Threat advisories | TPL-17 | Threat intelligence analyst | Affected teams | When a relevant threat appears | 1 page |

## 3. What each report contains

### 3.1 Weekly SOC Report

- Alert volume and classification (TP, BTP, FP, Undetermined) against last week
- New, open and closed cases by severity; cases older than 7 days
- Top 10 noisiest rules and tuning done
- Platform health: availability, silent sources, agent coverage
- Notable incidents in two lines each
- New threats or vulnerabilities relevant to the organisation
- Actions for next week with owners

### 3.2 Monthly SOC Report

- Executive summary: five sentences a non-technical reader understands
- Key performance indicators against target (section 4), with the trend for the last 6 months
- Incidents: count by severity and type, top 3 described as short stories (what, impact, response, lesson)
- Detection: new rules, retired rules, ATT&CK coverage change, results of detection tests
- Exposure: critical vulnerabilities open on internet-facing systems, credential leaks found, attack surface changes
- Operations: staffing, training, tool changes, outages
- Risks and requests: what management must decide or fund, with the risk of not doing it

### 3.3 Quarterly Executive Report

- Security posture in one picture: better, same or worse, and why
- The 3 most important incidents or threats of the quarter
- Progress on the SOC roadmap
- Decisions or investment needed

Write for executives: no tool names, no IP addresses, every number with a "so what".

### 3.4 Annual SOC Report

- Year in numbers with trends by quarter
- Major incidents and what changed because of them
- Maturity assessment result against last year
- Achievements against last year's plan
- Plan and budget for next year

## 4. Key performance indicators

| KPI | Definition | Source |
|---|---|---|
| Alerts per day | Alerts reaching the queue, daily average | SIEM or case tool |
| True positive rate | TP divided by all triaged alerts | Case tool classifications |
| False positive rate | FP divided by all triaged alerts | Case tool classifications |
| MTTA (Mean Time To Acknowledge) | Average time from alert created to analyst assigned | Case tool timestamps |
| MTTD (Mean Time To Detect) | Average time from first malicious activity to alert. Measured on confirmed incidents | Incident timelines |
| MTTC (Mean Time To Contain) | Average time from alert to containment, P1 and P2 | Incident timelines |
| MTTR (Mean Time To Resolve) | Average time from alert to case resolved, by severity | Case tool |
| SLA compliance | Percent of alerts acknowledged and triaged within the time box | Case tool |
| Log source coverage | Percent of critical assets sending required logs | Log source register |
| Endpoint coverage | Percent of assets with a working EDR agent | EDR console against asset inventory |
| ATT&CK coverage | Percent of prioritised techniques with a tested detection | ATT&CK coverage register |
| Platform availability | Percent of time the SIEM was searchable and ingesting | Health checks |

> NOTE: Report the same KPIs in the same way every month. Changing definitions breaks the trend, and the trend is what management reads.

## 5. Procedure

### 5.1 Daily

1. The shift analyst completes TPL-01 during the last 30 minutes of the shift.
2. The shift lead reviews and signs within the next shift.

### 5.2 Weekly

1. Every Monday morning, export last week's numbers using the saved report queries (Appendix A).
2. Add up TPL-01 totals and compare with the case tool. Investigate any difference over 5 percent.
3. Write TPL-03, review in the weekly SOC meeting, send by Monday noon.

### 5.3 Monthly

1. On the first working day, export the month's KPIs.
2. Update the KPI tracker and charts.
3. Draft TPL-04, review with the CISO, send by the 5th working day.
4. Store the report and the raw data export together.

### 5.4 Quarterly and annual

1. Build from the monthly reports. Do not recalculate from scratch.
2. Rehearse the executive summary with the CISO before the meeting.

## 6. Rules for good reports

- Every number has a comparison: last period, target, or both.
- Every chart has a one-line takeaway written above it.
- Bad news goes in, with the plan to fix it.
- Do not include in-house tool details or raw indicators in executive reports.
- Keep source data for every number so it can be checked.

## 7. Records

Store all reports in the SOC document library with a fixed naming pattern, for example `SOC-RPT-M-2026-11 Monthly SOC Report.docx`, for at least 3 years.

## 8. Metrics

| Metric | Target |
|---|---|
| Reports delivered on time | 100 percent |
| Numbers corrected after sending | Zero |

## 9. Related documents

- TPL-01 to TPL-06 report templates, GOV-08 SOC Metrics and KPI Standard
- SOP-01 Shift Start and Platform Health Check, SOP-08 Case Management

---page---

## Appendix A. Reporting queries

### A.1 Alerts by day and classification, last 30 days

Splunk Enterprise Security (SPL):

```spl
`notable` earliest=-30d@d latest=@d
| eval verdict = coalesce(disposition_label, "Unclassified")
| timechart span=1d count by verdict
```

Microsoft Sentinel (KQL):

```kql
SecurityIncident
| where CreatedTime > ago(30d)
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| summarize Count = count() by bin(CreatedTime, 1d), Classification
| render columnchart
```

IBM QRadar (AQL, offenses are not in AQL; use the API for offense counts and AQL for event-based counts):

```sql
SELECT DATEFORMAT(starttime, 'yyyy-MM-dd') AS day, COUNT(*) AS rule_hits
FROM events WHERE creeventlist IS NOT NULL
GROUP BY DATEFORMAT(starttime, 'yyyy-MM-dd') ORDER BY day LAST 30 DAYS
```

Wazuh (dashboard): histogram of `rule.level >= 7` with a daily interval over the last 30 days, split by `rule.level`.

### A.2 MTTA and MTTR by severity, last 30 days

Microsoft Sentinel (KQL):

```kql
SecurityIncident
| where CreatedTime > ago(30d)
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| extend TTA = datetime_diff('minute', FirstModifiedTime, CreatedTime),
         TTR = datetime_diff('hour', ClosedTime, CreatedTime)
| summarize MTTA_min = avg(TTA), MTTR_hours = avg(TTR), Cases = count() by Severity
```

Splunk Enterprise Security (SPL):

```spl
`notable` earliest=-30d
| join type=left rule_id [| inputlookup incident_review_lookup | stats min(time) as first_review by rule_id]
| eval tta = first_review - _time
| stats avg(tta) as mtta_sec count by urgency
| eval mtta_min = round(mtta_sec / 60, 1)
```

For TheHive, DFIR-IRIS or other case tools, export cases with created, assigned, resolved and severity fields and calculate the averages in a spreadsheet.
