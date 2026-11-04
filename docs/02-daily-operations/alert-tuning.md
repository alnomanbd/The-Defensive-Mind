# Alert Tuning

How to cut noise without creating blind spots. Noise is the biggest threat to a SOC: when analysts see the same false alert a hundred times, they stop looking, and the hundred-and-first is the real attack.

!!! abstract "At a glance"
    - Audience: L2 / L3 analysts, detection engineers, shift leads
    - Time to read: 12 minutes
    - Outcome: you can run a weekly tuning review and write exceptions an auditor and an attacker would both find hard to abuse

## Find the root cause first

| What you see | Real cause | Fix |
|---|---|---|
| Field values look wrong in the alert | Parser or decoder error | Fix the parser, not the rule |
| Rule fires on things it was not built for | Logic too broad | Rewrite the logic |
| Normal activity crosses the threshold | Threshold set without a baseline | Measure a 30-day baseline, set the threshold above it |
| Real, authorised activity (scanner, backup job) | Benign positive | Narrow exception with owner and expiry |
| Same event alerts from three tools | Duplicate detections | Correlate or deduplicate in the SIEM or SOAR |
| Rule's log source no longer exists | Dead rule | Retire it |

## Rules for every exception

- [ ] As narrow as possible: host **and** process **and** path or command line, never one of them alone
- [ ] An owner and a business reason
- [ ] An expiry date (maximum 12 months) for anything tied to a person, project or migration
- [ ] Tested against the last 30 days of data before going live
- [ ] Recorded in the detection register and in version control

!!! danger "Never exclude these wholesale"
    Administrator accounts, domain controllers, `powershell.exe`, `cmd.exe`, `rundll32.exe`, whole subnets, or "the IT team". These are exactly what attackers use.

## Good and bad exceptions

| Bad | Why | Good |
|---|---|---|
| Exclude host `SRV-BACKUP01` | Everything on that host is now invisible | Exclude `SRV-BACKUP01` + `C:\Program Files\BackupVendor\agent.exe` + command line contains `--nightly` |
| Exclude user `svc_scan` | A stolen service account becomes invisible | Exclude `svc_scan` from source `10.10.5.20` only, during 01:00 to 04:00, expires 2027-05-01 |
| Raise threshold from 10 to 1000 | Slow brute force now invisible | Raise to the 30-day 99th percentile (for example 35), keep a daily summary alert |

## The weekly tuning review (30 minutes)

1. List the top 10 rules by alert volume and by false positive rate (queries below).
2. For each one, agree an action: tune, keep, retire, or investigate.
3. Review exceptions expiring in the next 30 days: renew with a fresh owner confirmation, or remove.
4. Record the results in the weekly report.

### Top noisy rules, last 7 days

=== "Splunk SPL"

    ```spl
    `notable` earliest=-7d
    | stats count as alerts count(eval(disposition_label="False Positive")) as fp by rule_name
    | eval fp_rate = round(100 * fp / alerts, 1)
    | sort - alerts | head 10
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | where CreatedTime > ago(7d)
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | summarize Alerts = count(), FP = countif(Classification == "FalsePositive") by Title
    | extend FPRate = round(100.0 * FP / Alerts, 1)
    | top 10 by Alerts desc
    ```

=== "Elastic ES|QL"

    ```sql
    FROM .alerts-security.alerts-default
    | WHERE @timestamp > NOW() - 7 days
    | STATS alerts = COUNT(*) BY kibana.alert.rule.name
    | SORT alerts DESC | LIMIT 10
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT RULENAME(creeventlist) AS rule, COUNT(*) AS hits
    FROM events WHERE creeventlist IS NOT NULL
    GROUP BY creeventlist ORDER BY hits DESC LIMIT 10 LAST 7 DAYS
    ```

=== "Wazuh"

    ```text
    Dashboard > data table on wazuh-alerts-*, last 7 days
    Rows: rule.id, rule.description   Metric: count   Sort: descending
    ```

### Baseline before you change a threshold

=== "Splunk SPL"

    ```spl
    index=wineventlog EventCode=4625 earliest=-30d
    | bin _time span=10m | stats count by _time, src
    | stats perc95(count) as p95 perc99(count) as p99 max(count) as max
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityEvent
    | where TimeGenerated > ago(30d) and EventID == 4625
    | summarize Fails = count() by bin(TimeGenerated, 10m), IpAddress
    | summarize P95 = percentile(Fails, 95), P99 = percentile(Fails, 99), Max = max(Fails)
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT sourceip, COUNT(*) AS fails
    FROM events WHERE QIDNAME(qid) ILIKE '%failed%logon%'
    GROUP BY sourceip ORDER BY fails DESC LAST 30 DAYS
    ```

## Writing an exception in Wazuh

Wazuh exceptions are child rules with `level="0"` in `/var/ossec/etc/rules/local_rules.xml`:

```xml
<rule id="100500" level="0">
  <if_sid>5710</if_sid>
  <srcip>10.10.5.20</srcip>
  <description>Exception: approved vulnerability scanner 10.10.5.20 (request #0042, owner: IT security, expires 2027-05-01)</description>
</rule>
```

Put the ticket, owner and expiry in the description so the next engineer knows why it exists. Wazuh has no built-in expiry, so the weekly review must catch expired entries.

## Emergency suppression during an alert storm

When one rule floods the queue:

1. Suppress the rule **for the affected entity only**, for up to 24 hours.
2. Never suppress the rule for everything.
3. Post the suppression and its expiry in the SOC channel and daily report.
4. Raise a normal tuning request the same day.

## Metrics

| Metric | Target |
|---|---|
| False positive rate across all rules | Under 30 percent and falling |
| Rules above 50 percent FP for more than 2 weeks | Zero |
| Exceptions without owner or expiry | Zero |
| Expired exceptions still active | Zero |

## Downloads

- [SOP-10 False Positive Handling and Tuning (Word)](../downloads/soc-kit/sop/SOP-10-false-positive-handling-and-tuning.docx)
- [SOP-02 Alert Queue Monitoring, alert storms (Word)](../downloads/soc-kit/sop/SOP-02-alert-queue-monitoring.docx)

## Related pages

- [Alert triage](alert-triage.md)
- [Detection lifecycle](../05-detection-engineering/detection-lifecycle.md)
- [Testing and tuning detections](../05-detection-engineering/testing-and-tuning.md)
- [Detection request template](../09-templates/detection-request.md)
