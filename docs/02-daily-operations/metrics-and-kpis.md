# Metrics and KPIs

Which numbers to measure in a Security Operations Center (SOC), how to calculate each one, where the data comes from, and how to turn them into a report management actually reads.

!!! abstract "At a glance"
    - Audience: SOC managers, shift leads, L3 analysts
    - Time to read: 12 minutes
    - Outcome: a KPI set with clear definitions, queries to calculate them, and a monthly reporting rhythm

## Measure few things, the same way, every month

A trend is worth more than any single number. Pick 8 to 12 KPIs, write down exactly how each is calculated, and never change the definition without saying so in the report.

## Core KPIs

| KPI | Formula | Good direction | Typical target |
|---|---|---|---|
| Alerts per day | Alerts reaching the queue / days | Down (after tuning) | Depends on team size; under 50 per analyst per shift is workable |
| True positive rate | TP / all triaged alerts | Up | Above 10 to 20 percent |
| False positive rate | FP / all triaged alerts | Down | Under 30 percent |
| MTTA (Mean Time To Acknowledge) | Avg(assigned time minus created time) | Down | Critical under 5 min, High under 15 min |
| MTTD (Mean Time To Detect) | Avg(first alert time minus first malicious activity), confirmed incidents only | Down | Hours, not days |
| MTTC (Mean Time To Contain) | Avg(containment time minus first alert), P1 and P2 | Down | P1 under 4 hours |
| MTTR (Mean Time To Resolve) | Avg(resolved time minus created time), by severity | Down | Set per severity |
| SLA compliance | Alerts handled inside their time box / all alerts | Up | Above 95 percent |
| Log source coverage | Critical assets sending required logs / all critical assets | Up | Above 95 percent |
| Endpoint coverage | Assets with a healthy EDR agent / all assets | Up | Above 98 percent |
| ATT&CK coverage | Priority techniques with a **tested** detection / priority techniques | Up | Grow every quarter |
| SIEM availability | Time searchable and ingesting / total time | Up | 99.5 percent |

!!! warning "Numbers that lie"
    - A falling alert count can mean better tuning **or** a broken log source. Always show coverage next to volume.
    - A high closure rate can mean analysts closing without investigating. Pair it with a quality review score.
    - MTTD needs the attack start time, which you only learn during investigation. Measure it on confirmed incidents only.

## Where the data comes from

| KPI | Source |
|---|---|
| Alert counts, TP/FP rates | Case tool or SIEM alert classification fields |
| MTTA, MTTR | Case tool timestamps (created, assigned, resolved) |
| MTTD, MTTC | Incident timelines |
| Coverage | Log source register and EDR console compared with the asset inventory |
| ATT&CK coverage | Detection register with test results |
| Availability | Health check records |

## Queries

### Alerts by classification, last 30 days

=== "Splunk SPL"

    ```spl
    `notable` earliest=-30d@d latest=@d
    | eval verdict = coalesce(disposition_label, "Unclassified")
    | timechart span=1d count by verdict
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | where CreatedTime > ago(30d)
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | summarize Count = count() by bin(CreatedTime, 1d), Classification
    | render columnchart
    ```

=== "Elastic ES|QL"

    ```sql
    FROM .alerts-security.alerts-default
    | WHERE @timestamp > NOW() - 30 days
    | STATS alerts = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp), kibana.alert.workflow_status
    | SORT day
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT DATEFORMAT(starttime, 'yyyy-MM-dd') AS day, COUNT(*) AS rule_hits
    FROM events WHERE creeventlist IS NOT NULL
    GROUP BY DATEFORMAT(starttime, 'yyyy-MM-dd') ORDER BY day LAST 30 DAYS
    ```

    Offense counts and closing reasons come from the Offenses API, not AQL.

=== "Wazuh"

    ```text
    Dashboard > histogram on wazuh-alerts-*, last 30 days, interval 1d
    Filter: rule.level >= 7   Split series: rule.level
    ```

### MTTA and MTTR by severity

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | where CreatedTime > ago(30d)
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | extend TTA_min = datetime_diff('minute', FirstModifiedTime, CreatedTime),
             TTR_h = datetime_diff('hour', ClosedTime, CreatedTime)
    | summarize MTTA_min = avg(TTA_min), MTTR_h = avg(TTR_h), Cases = count() by Severity
    ```

=== "Splunk SPL"

    ```spl
    `notable` earliest=-30d
    | join type=left rule_id [| inputlookup incident_review_lookup | stats min(time) as first_review by rule_id]
    | eval tta_min = round((first_review - _time) / 60, 1)
    | stats avg(tta_min) as mtta_min count by urgency
    ```

=== "TheHive or other case tools"

    ```text
    Export cases with: createdAt, assignee change time, resolvedAt, severity
    Calculate the averages in a spreadsheet or with a small script
    ```

### Endpoint coverage

=== "Wazuh API"

    ```bash
    curl -sk -H "Authorization: Bearer $TOKEN" "https://WAZUH-MANAGER:55000/agents/summary/status"
    ```

=== "Microsoft Defender KQL"

    ```kql
    DeviceInfo
    | where Timestamp > ago(7d)
    | summarize arg_max(Timestamp, *) by DeviceId
    | summarize Total = count(), SeenLast24h = countif(Timestamp > ago(1d)) by OSPlatform
    ```

Compare both with the asset inventory. The difference is your unprotected estate.

## Reporting rhythm

| Report | For | Focus |
|---|---|---|
| Daily | Shift lead, next shift | Health, alerts, open cases |
| Weekly | SOC team, IT operations, CISO | Trends, noisy rules, open cases older than 7 days |
| Monthly | CISO, IT management | KPIs against target with 6-month trend, top incidents as stories, decisions needed |
| Quarterly | Executives, board risk committee | Posture, three things that mattered, investment |
| Annual | Executives, board, auditors | Year in numbers, maturity, plan and budget |

## Making a chart management reads

- [ ] One message per chart, written as a sentence above it ("Containment time halved after the new isolation playbook")
- [ ] Six months of history, not one
- [ ] Target line on the chart
- [ ] No tool names, rule IDs or IP addresses in executive reports

## Downloads

- [SOP-09 Reporting calendar and KPIs (Word)](../downloads/soc-kit/sop/SOP-09-daily-weekly-monthly-reporting.docx)
- [TPL-01 Daily Shift Report](../downloads/soc-kit/tpl/TPL-01-daily-shift-report.docx), [TPL-03 Weekly](../downloads/soc-kit/tpl/TPL-03-weekly-soc-report.docx), [TPL-04 Monthly](../downloads/soc-kit/tpl/TPL-04-monthly-soc-report.docx), [TPL-05 Quarterly](../downloads/soc-kit/tpl/TPL-05-quarterly-executive-report.docx), [TPL-06 Annual](../downloads/soc-kit/tpl/TPL-06-annual-soc-report.docx)

## Related pages

- [Daily routine](daily-routine.md)
- [Monthly SOC report template](../09-templates/monthly-soc-report.md)
- [Alert tuning](alert-tuning.md)
- [Coverage mapping](../05-detection-engineering/coverage-mapping.md)
