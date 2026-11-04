---
id: SOP-10
title: False Positive Handling and Tuning Requests
owner: Detection Engineering Lead
audience: L1 analyst, L2 analyst, detection engineers, SOC Lead
review: Every 6 months
summary: How the SOC turns false positives and benign activity into fixed rules and approved exceptions, without creating blind spots.
---
## 1. Purpose

Noise is the biggest threat to a SOC's effectiveness. When analysts see the same false alert a hundred times, they stop looking, and the hundred-and-first is the real attack. This procedure makes noise reduction a routine, controlled activity: every change is requested, justified, reviewed, tested and has an expiry where needed.

## 2. Scope

- Detection rules in the SIEM, EDR or XDR custom detections, IDS signatures, email and cloud security policies the SOC controls.
- False positives (FP), benign true positives (BTP) and alert storms.
- Out of scope: switching off vendor-managed detections without the vendor's guidance.

## 3. Definitions

| Term | Meaning |
|---|---|
| Tuning | Changing a rule so it stops firing on things it should not catch (logic fix, threshold, field correction) |
| Exception (allow-list) | A narrow, documented exclusion for activity that is real but authorised |
| Suppression | Temporarily stopping repeat alerts for the same entity for a set time, without changing the rule |
| Blind spot | Activity an attacker could hide in because of an exception that is too wide |

## 4. Rules for every change

- [ ] Every exception is as narrow as possible: specific host plus specific process plus specific path or command, never a whole subnet, user group or process name alone
- [ ] Every exception has an owner and a business reason
- [ ] Every exception for a person, project or migration has an expiry date (maximum 12 months)
- [ ] Every change is tested against the last 30 days of data before going live
- [ ] Every change is recorded in the detection register and in version control where rules are kept as code
- [ ] Nobody tunes a rule only because it is noisy. The reason must be "it fires on activity that is not what it is meant to catch" or "this activity is authorised"

> WARNING: Never exclude by user name or host name alone, never exclude administrator accounts or domain controllers wholesale, and never exclude a whole parent process such as powershell.exe or cmd.exe. These are exactly what attackers use.

## 5. Roles and responsibilities

| Role | Responsibility |
|---|---|
| L1 or L2 analyst | Spots the FP or BTP pattern, raises the request with evidence |
| Detection engineer | Designs, tests and applies the change, updates the register |
| SOC Lead | Approves exceptions on critical assets and any change to Critical or High rules |
| Asset or business owner | Confirms the authorised activity in writing for BTP exceptions |
| Shift lead | Runs the weekly noisy rule review |

## 6. Procedure

### 6.1 Raise the request (analyst)

Raise a Tuning and Exception Request (TPL-23) when:

- the same FP pattern appears 3 or more times, or
- a BTP will keep happening (a scheduled job, an approved tool), or
- a rule's FP rate is above 30 percent for a week.

The request must include:

1. Rule name and ID.
2. Example alert IDs (at least 3).
3. Why it is FP or BTP, with evidence (query results, change ticket, owner confirmation).
4. Suggested change, as specific as possible.
5. Expected reduction in alert count.

### 6.2 Assess (detection engineer)

1. Confirm the root cause:

| Cause | Fix |
|---|---|
| Parsing error, wrong field mapping | Fix the parser or decoder, not the rule |
| Rule logic too broad | Rewrite the logic |
| Threshold too low for this environment | Raise the threshold, document the baseline used |
| Authorised activity (BTP) | Narrow exception with owner and expiry |
| Duplicate alerts from several tools | Correlate or deduplicate in the SIEM or SOAR |
| Rule no longer useful (source gone, technique covered better elsewhere) | Retire the rule (SOP-13) |

2. Check the blind spot risk: could an attacker produce exactly this pattern? If yes, choose a fix that keeps a lower-severity alert or a weekly summary instead of full exclusion.

### 6.3 Test

1. Run the changed rule against the last 30 days of data.
2. Confirm the FP alerts no longer fire.
3. Confirm known TP examples and test cases still fire. Use the rule's test case from Atomic Red Team or the detection test library (SOP-14) where available.
4. Record before and after counts in the request.

### 6.4 Approve and apply

| Change | Approval |
|---|---|
| Threshold or logic change on Low and Medium rules | Detection engineer (peer review by a second engineer) |
| Any change to High or Critical rules | SOC Lead |
| Exception covering a critical asset, a privileged account, or with no expiry | SOC Lead and asset owner |

Apply through the normal change process (SOP-17). Rules kept as code go through a pull request.

### 6.5 Close the loop

1. Update the detection register: change, reason, date, approver, expiry.
2. Tell the requesting analyst and close TPL-23.
3. Check the rule's alert volume one week later.

### 6.6 Emergency suppression during an alert storm

When one rule floods the queue (SOP-02 section 5.6):

1. The detection engineer or shift lead may suppress the rule for the affected entity for up to 24 hours.
2. A suppression must not hide all alerts from the rule for all entities.
3. Record it in the SOC channel and in TPL-01 with the expiry time.
4. Raise a normal tuning request the same day. The suppression expires automatically.

### 6.7 Weekly noisy rule review

Every week the shift lead and a detection engineer:

1. List the top 10 rules by alert volume and by FP rate (Appendix A).
2. Agree an action for each: tune, keep, retire, or investigate.
3. Review exceptions expiring in the next 30 days: renew with a fresh owner confirmation, or remove.
4. Record results in the weekly report (TPL-03).

## 7. Records

- TPL-23 Tuning and Exception Request for every change
- Detection register with all active exceptions and their expiry
- Version control history for rules kept as code

## 8. Metrics

| Metric | Target |
|---|---|
| FP rate across all rules | Under 30 percent, falling |
| Rules with FP rate above 50 percent | Zero for more than 2 weeks |
| Exceptions without owner or expiry | Zero |
| Expired exceptions still active | Zero |
| Tuning requests closed within 10 working days | 90 percent |

## 9. Common mistakes

- Excluding a whole server or user because "it is always that one".
- Turning a rule off instead of fixing it.
- Tuning without testing that true positives still fire.
- Exceptions that live forever because nobody owns them.
- Fixing the rule when the real problem is the parser.

## 10. Related documents

- SOP-02 Alert Queue Monitoring, SOP-03 Alert Triage and Classification, SOP-13 Detection Rule Lifecycle, SOP-14 Detection Testing, SOP-17 SOC Change Management
- TPL-23 Tuning and Exception Request, TPL-22 Detection Rule Documentation, TPL-03 Weekly SOC Report

---page---

## Appendix A. Noisy rule queries

### A.1 Top rules by volume and FP rate, last 7 days

Splunk Enterprise Security (SPL):

```spl
`notable` earliest=-7d
| stats count as alerts count(eval(disposition_label="False Positive")) as fp by rule_name
| eval fp_rate = round(100 * fp / alerts, 1)
| sort - alerts | head 10
```

Microsoft Sentinel (KQL):

```kql
SecurityIncident
| where CreatedTime > ago(7d)
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| summarize Alerts = count(), FP = countif(Classification == "FalsePositive") by Title
| extend FPRate = round(100.0 * FP / Alerts, 1)
| top 10 by Alerts desc
```

IBM QRadar (AQL, rule hit volume):

```sql
SELECT RULENAME(creeventlist) AS rule, COUNT(*) AS hits
FROM events WHERE creeventlist IS NOT NULL
GROUP BY creeventlist ORDER BY hits DESC LIMIT 10 LAST 7 DAYS
```

Combine with offense closing reasons from the Offenses API to get the FP rate.

Elastic Security (ES|QL on the alerts index):

```sql
FROM .alerts-security.alerts-default | WHERE @timestamp > NOW() - 7 days
| STATS alerts = COUNT(*) BY kibana.alert.rule.name | SORT alerts DESC | LIMIT 10
```

Wazuh (dashboard): data table of `rule.id` and `rule.description`, count, last 7 days, sorted descending. On the manager, exceptions are written as child rules with `level="0"` in `/var/ossec/etc/rules/local_rules.xml`, for example:

```xml
<rule id="100500" level="0">
  <if_sid>5710</if_sid>
  <srcip>10.10.5.20</srcip>
  <description>Exception: approved vulnerability scanner 10.10.5.20 (TPL-23 #0042, expires 2027-05-01)</description>
</rule>
```
