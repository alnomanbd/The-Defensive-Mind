# Daily Routine

The exact checks to run at the start, every hour and at the end of a Security Operations Center (SOC) shift, plus weekly and monthly tasks with owners. Copy the checklists into your case tool or wiki and tick them every shift.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2 / L3, shift lead, SOC manager
    - Time to read: 10 minutes
    - Outcome: you can run a shift from login to handover with saved queries for every health check

## Start of shift (first 30 minutes)

Do not pick up new Low or Medium alerts until steps 1 to 4 are done. A waiting Critical always goes first.

| Step | Task | Done when | Time |
|---|---|---|---|
| 1 | Read the written handover | You can name every open Critical/High case and its owner | 5 min |
| 2 | Verbal handover | Ownership of each open item explicitly accepted by name | 5 to 10 min |
| 3 | Run health checks (queries below) | No silent source, no ingestion error, automation ran | 5 min |
| 4 | Check the queue | No unacknowledged alert past SLA; you know the oldest item | 5 min |
| 5 | Read notices | Change calendar, maintenance windows, new advisories, VIP travel | 5 min |
| 6 | Tool access check | SIEM, Endpoint Detection and Response (EDR), case tool, chat, out-of-band channel all work | 2 min |

### Health check 1: silent log sources

Thresholds that work in most environments: 15 minutes for domain controllers, firewalls, EDR and identity provider; 60 minutes for low-volume sources; 24 hours for batch sources.

=== "Splunk SPL"

    ```spl
    | tstats latest(_time) as last_seen where index=* earliest=-24h by index, sourcetype, host
    | eval minutes_silent = round((now() - last_seen) / 60)
    | where minutes_silent > 15
    | sort - minutes_silent
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    union withsource=TableName SecurityEvent, Syslog, CommonSecurityLog, SigninLogs
    | where TimeGenerated > ago(24h)
    | summarize LastSeen = max(TimeGenerated) by TableName, Computer
    | extend MinutesSilent = datetime_diff('minute', now(), LastSeen)
    | where MinutesSilent > 15
    | order by MinutesSilent desc
    ```

=== "Elastic ES|QL"

    ```sql
    FROM logs-*
    | WHERE @timestamp > NOW() - 24 hours
    | STATS last_seen = MAX(@timestamp) BY host.name, data_stream.dataset
    | EVAL minutes_silent = DATE_DIFF("minute", last_seen, NOW())
    | WHERE minutes_silent > 15
    | SORT minutes_silent DESC
    ```

=== "Wazuh"

    ```bash
    # On the manager: list agents that are not active
    /var/ossec/bin/agent_control -l | grep -v "Active"

    # Or through the API (token obtained beforehand)
    curl -sk -H "Authorization: Bearer $TOKEN" \
      "https://wazuh-manager.example.com:55000/agents?status=disconnected,never_connected&select=name,lastKeepAlive"
    ```

!!! warning "A quiet queue is not good news until proven"
    If alert volume is 50% below the same hour last week, assume a collection problem before you assume a quiet night. Open a case for every silent critical source; a blind spot is a security issue.

### Health check 2: volume compared with last week

=== "Splunk SPL"

    ```spl
    | tstats count where index=* earliest=-1h latest=now by index
    | append [| tstats count as last_week where index=* earliest=-169h latest=-168h by index]
    | stats sum(count) as now, sum(last_week) as last_week by index
    | eval change_pct = round((now - last_week) / last_week * 100, 1)
    | where abs(change_pct) > 30
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    let now_h = Usage | where TimeGenerated > ago(1h) | summarize NowMB = sum(Quantity) by DataType;
    let last_w = Usage | where TimeGenerated between (ago(169h) .. ago(168h)) | summarize LastWeekMB = sum(Quantity) by DataType;
    now_h | join kind=fullouter last_w on DataType
    | extend ChangePct = round((NowMB - LastWeekMB) / LastWeekMB * 100, 1)
    | where abs(ChangePct) > 30
    ```

### Health check 3: the rest (manual, 2 minutes)

- [ ] SIEM: no red banners, search head responsive, disk under 80%.
- [ ] Automation (Security Orchestration, Automation and Response, SOAR, or workflow engine): last run of each scheduled job succeeded.
- [ ] Threat intelligence feeds updated in the last 24 hours.
- [ ] Last notification (email, chat, pager) actually arrived.

## Every hour (5 minutes, on the hour)

- [ ] Queue: anything within 10 minutes of its acknowledgement SLA?
- [ ] My cases: anything waiting on a reply I should chase?
- [ ] Silent sources query: any new entries since last hour?
- [ ] Chat and email: unanswered requests from IT, help desk or management?
- [ ] Break: if you have watched the queue for 90 minutes straight, rotate with a colleague.

Queue age query for the hourly check:

=== "Splunk SPL (Enterprise Security)"

    ```spl
    | `notable`
    | search status_label="New"
    | eval age_min = round((now() - _time) / 60)
    | stats count, max(age_min) as oldest_min by urgency
    | sort - oldest_min
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | where Status == "New"
    | extend AgeMin = datetime_diff('minute', now(), CreatedTime)
    | summarize Count = count(), OldestMin = max(AgeMin) by Severity
    ```

=== "Wazuh"

    ```text
    Discover > index pattern wazuh-alerts-* > last 1 hour
    Query: rule.level >= 10
    Then visualise count by rule.description and agent.name
    ```

## Mid-shift (shift lead, once)

- [ ] Every open case has correct severity, owner and a written next step.
- [ ] No analyst holds more than 5 active investigations; rebalance if so.
- [ ] Every case waiting on another team has had a reply, or has been chased.

## End of shift (last 30 minutes)

| Step | Task | Output |
|---|---|---|
| 1 | Stop picking up new Low alerts | No half-finished work |
| 2 | Bring each open case to a clean state | Notes current, next step written, evidence attached |
| 3 | Write the handover | [Shift handover template](../09-templates/shift-handover-template.md) filled in |
| 4 | Record shift stats | Alerts in / closed / escalated; cases opened / closed; SLA breaches |
| 5 | Verbal handover | Incoming analyst names each item they now own |
| 6 | Close privileged sessions | No admin sessions left open on shared consoles |

## Who does what on shift

| Moment | L1 | L2 | L3 | Shift lead / manager |
|---|---|---|---|---|
| Start | Health checks, queue | Review own open cases | Review active incidents | Confirms staffing, reads all handovers |
| Hourly | Hourly checklist | Chase pending replies | Check hunts running | Watches SLA timers |
| Mid-shift | Keep queue moving | Escalation review | Coach on hard cases | Rebalance work |
| End | Stats, handover notes | Case summaries | Incident status update | Signs off the handover |

## Weekly tasks

| Task | Owner | Day | Output |
|---|---|---|---|
| Top 10 noisiest rules | L3 / detection engineer | Mon | Decision per rule (see [Alert tuning](alert-tuning.md)) |
| Review all false-positive and benign closures | Shift lead | Mon | Tuning tickets, coaching notes |
| Quality review of 5 to 10 closed cases | SOC manager or L3 | Wed | Scores per [Case management](case-management.md) |
| Coverage check: new, missing or degraded sources | Detection engineer | Wed | Ticket per gap |
| Expiring suppressions and allowlist entries | Detection engineer | Thu | Renewed with reason or deleted |
| Hunt planning | L3 | Thu | One or two hypotheses for next week |
| Paging and out-of-band channel test | Shift lead | Any | Proof the on-call phone rings |
| Team sync (30 min) | SOC manager | Fri | Blockers, lessons, upcoming changes |

## Monthly tasks

| Task | Owner | Output |
|---|---|---|
| Monthly SOC report | SOC manager | [Monthly SOC report](../09-templates/monthly-soc-report.md) |
| Metrics against targets | SOC manager | Actions for every off-target metric ([Metrics and KPIs](metrics-and-kpis.md)) |
| MITRE ATT&CK coverage review | Detection engineering | Top three gaps with owners |
| SOC tool access review | SOC manager | Leavers removed, least privilege confirmed |
| Review 2 or 3 playbooks | L3 | Updated playbook with change log |
| One tabletop or purple-team exercise | SOC manager | Findings ([Tabletop exercises](../03-incident-response/tabletop-exercises.md)) |
| Overdue post-incident actions | SOC manager | Escalation list |
| Restore test of rules, dashboards, playbooks | Platform owner | Proof of restore |

!!! danger "Common mistakes"
    - Health checks done "by eye" on a dashboard instead of with a saved query that lists silent sources.
    - Everyone on lunch at the same time, queue unowned for 45 minutes.
    - Weekly tasks with no named owner, so they silently stop after a month.
    - Shift stats recorded in a different format each shift, so trends cannot be built.

## Copy-paste shift checklist

```text
START  [ ] handover read  [ ] verbal done  [ ] silent sources  [ ] volume vs last week
       [ ] automation OK  [ ] TI feeds OK  [ ] queue checked   [ ] notices read  [ ] tools OK
HOURLY [ ] 08 [ ] 09 [ ] 10 [ ] 11 [ ] 12 [ ] 13 [ ] 14 [ ] 15 [ ] 16 [ ] 17 [ ] 18 [ ] 19
END    [ ] cases tidy  [ ] handover written  [ ] stats recorded  [ ] verbal done  [ ] logged out
```

## Related pages

- [Alert triage](alert-triage.md)
- [Severity and SLA](severity-and-sla.md)
- [Shift handover](shift-handover.md)
- [Alert tuning](alert-tuning.md)
- [Metrics and KPIs](metrics-and-kpis.md)
- [Shift handover template](../09-templates/shift-handover-template.md)
- [Monthly SOC report template](../09-templates/monthly-soc-report.md)
