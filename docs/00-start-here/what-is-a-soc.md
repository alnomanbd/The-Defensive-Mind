# What Is a SOC?

A Security Operations Center (SOC) watches for attacks, decides which signals matter, and drives the response until risk is contained. This page shows what that means on a real shift, how to structure the team, and how to check that your SOC works.

!!! abstract "At a glance"
    - Audience: L1/L2/L3 analysts, SOC leads, SOC managers
    - Time to read: 15 minutes
    - Outcome: you know who does what on a shift, which team and sourcing model fits, and five checks to run today to prove the SOC is healthy

## What the SOC does, by function

| Function | What you actually do | Main tool | Output |
|----------|----------------------|-----------|--------|
| Monitoring and triage | Work the alert queue, enrich, close or escalate | Security Information and Event Management (SIEM), case tool | Triaged alerts, cases |
| Incident response (IR) | Contain, eradicate, recover | Endpoint Detection and Response (EDR), identity console, firewall | Closed incidents, lessons learned |
| Detection engineering | Write, test, tune rules | SIEM, Sigma, Git | Rules, coverage map |
| Threat hunting | Search for what no rule caught | SIEM, EDR telemetry | Hunt reports, new rules |
| Threat intelligence (TI) | Apply indicators and adversary knowledge | TI platform, feeds | Enrichment, blocklists, briefs |
| Exposure insight | Track what is exposed and exploitable | Vulnerability scanner, attack surface tools | Risk tickets to owners |
| Platform engineering | Keep logs flowing and tools connected | Log shippers, Security Orchestration, Automation and Response (SOAR) | Healthy pipeline |
| Reporting | Metrics and management reports | Dashboards | Monthly report |

!!! warning "Common mistake: the SOC as fixer"
    The SOC detects, alerts, contains urgent threats and coordinates. System owners patch and remediate. If analysts start patching servers, the alert queue stops being worked.

## Who does what on a shift

| Time | L1 does | L2 does | L3 does | Manager / lead does |
|------|---------|---------|---------|---------------------|
| Shift start | Read handover, check queue age, run log-health check | Review open investigations | Check overnight escalations | Confirm staffing, check SLA breaches |
| During shift | Triage alerts with playbooks, enrich, close false positives with reason, escalate | Investigate escalations, scope impact, start containment | Lead incidents, hunt, tune noisy rules | Unblock, approve high-impact containment, talk to stakeholders |
| Incident | Collect first facts, open case, notify L2 | Scope hosts/users, isolate, collect evidence | Root cause, eradication plan, forensics | Business decisions, communication, legal/regulatory clock |
| Shift end | Write handover: open cases, pending actions | Update case timelines | Note detection gaps found | Review metrics, sign off handover |

## Five checks to prove your SOC works today

Run these on day one in any SOC. Each takes under 10 minutes.

### 1. Is any log source silent?

=== "Splunk SPL"

    ```spl
    | tstats latest(_time) as last_seen where index=* by index, sourcetype
    | eval hours_silent=round((now()-last_seen)/3600,1)
    | where hours_silent > 2
    | sort - hours_silent
    ```

=== "Microsoft KQL (Sentinel)"

    ```kql
    union withsource=TableName *
    | summarize last_seen=max(TimeGenerated) by TableName
    | extend hours_silent = datetime_diff('hour', now(), last_seen)
    | where hours_silent > 2
    | order by hours_silent desc
    ```

=== "Elastic (ES|QL)"

    ```sql
    FROM logs-*
    | STATS last_seen = MAX(@timestamp) BY data_stream.dataset
    | EVAL hours_silent = DATE_DIFF("hour", last_seen, NOW())
    | WHERE hours_silent > 2
    | SORT hours_silent DESC
    ```

=== "Wazuh"

    ```bash
    # Get an API token, then list agents that are disconnected or never connected
    TOKEN=$(curl -sk -u "$WUSER:$WPASS" -X POST \
      "https://wazuh-manager.example.com:55000/security/user/authenticate?raw=true")
    curl -sk -H "Authorization: Bearer $TOKEN" \
      "https://wazuh-manager.example.com:55000/agents?status=disconnected,never_connected&select=name,lastKeepAlive"
    ```

**Action:** any critical source (identity, EDR, email, firewall) silent more than 2 hours is a P2 platform incident. Open a ticket to the owner the same day.

### 2. How old is the oldest unworked alert?

=== "Splunk SPL"

    ```spl
    index=notable status="new"
    | stats min(_time) as oldest count by urgency
    | eval age_hours=round((now()-oldest)/3600,1)
    ```

=== "Microsoft KQL (Sentinel)"

    ```kql
    SecurityIncident
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | where Status == "New"
    | summarize count(), oldest=min(CreatedTime) by Severity
    | extend age_hours = datetime_diff('hour', now(), oldest)
    ```

**Target:** no high-severity alert older than 1 hour, no medium older than 8 hours. See [Severity and SLA](../02-daily-operations/severity-and-sla.md).

### 3. What share of alerts lead to action?

Pull last 30 days of closed cases with their closure reason. If more than 85-90% are "false positive", the SOC is drowning in noise. Take the top 5 rules by false positives to the detection engineer this week.

### 4. Can you answer "who logged in from where" in under 2 minutes?

=== "Microsoft KQL (Entra ID)"

    ```kql
    SigninLogs
    | where UserPrincipalName == "j.doe@example.com" and TimeGenerated > ago(7d)
    | project TimeGenerated, IPAddress, Location, AppDisplayName, ResultType
    ```

=== "Splunk SPL"

    ```spl
    index=auth user="j.doe@example.com" earliest=-7d
    | table _time src_ip src_country app action
    ```

If this query does not exist or takes 20 minutes to write, identity logging is your first gap.

### 5. Is there a named person for every open case?

Unassigned cases are lost cases. Filter the case tool for `owner = empty`. Target: zero.

## Team models

| Model | How it works | Fits | Watch out for |
|-------|--------------|------|---------------|
| Tiered (L1->L2->L3) | Hand-off by skill level | 10+ analysts, high volume | Context lost at each hand-off, L1 burnout |
| Pod / squad | Mixed-skill team owns alerts end to end | 8-30 people | Needs good leads per pod |
| Follow-the-alert | Whoever picks it up keeps it, senior on call | 3-6 people | Seniors get interrupted often |
| Automation-first | SOAR enriches and auto-closes known-benign; humans judge | High volume, mature tooling | Bad automation hides real attacks |

!!! tip "What works in practice"
    Keep L1/L2/L3 as a skills ladder, not as rigid hand-offs. Let an analyst keep a case as far as their skill allows and pull in a named senior. Fewer hand-offs means faster, better cases.

## Sourcing: in-house, MSSP/MDR, hybrid

| Factor | In-house | Managed Security Service Provider (MSSP) / Managed Detection and Response (MDR) | Hybrid |
|--------|----------|-------------------|--------|
| Time to start | 6-12 months | 4-12 weeks | 2-6 months |
| Business context | Deep | Shallow | Deep where it matters |
| 24x7 coverage | Needs 8-12 people | Included | Provider covers nights/weekends |
| Detection control | Full | Provider content | Shared |
| Containment authority | Full | Often "notify only" | Defined in joint runbook |

| Your situation | Choose |
|----------------|--------|
| Under ~500 staff, no security team | MSSP/MDR + one internal owner |
| 2-5 security staff, need 24x7 | Hybrid: in-house day, provider night |
| Regulated, strong IT, custom apps | In-house, plus forensics retainer |

!!! warning "Common mistake: outsourcing accountability"
    With a provider you still need someone internal (0.5-1 full-time) to approve containment, give business context and check the provider's work. Test them: send a simulated phishing click and time how long until you hear about it.

## Healthy vs. unhealthy signals

| Area | Healthy | Unhealthy |
|------|---------|-----------|
| Alert quality | 30-60% of alerts lead to an action or finding | Over 90% false positives |
| Speed | High-severity acknowledged in under 15 min | Critical alerts sit for hours |
| Log health | Silent-source alert fires within 1 hour | Source dead for weeks, nobody noticed |
| Coverage | ATT&CK coverage map reviewed quarterly | Nobody knows what is covered |
| Learning | Every major incident yields at least one rule or playbook fix | Same incident repeats |
| People | Turnover under ~20%/year, training time booked | Constant hiring |

!!! example "Two SOCs, same budget"
    SOC A ingests 400 GB/day, runs 600 rules, closes 95% as false positive. SOC B ingests 80 GB/day from identity, endpoint, email and edge, runs 120 tuned rules, and acts on half its alerts. SOC B catches more attacks.

## Copy-paste checklist: is this a working SOC?

- [ ] Silent-source check runs automatically at least hourly
- [ ] Every open case has an owner
- [ ] Severity levels and response times are written and measured
- [ ] Top 10 alert types each have a playbook
- [ ] Containment authority (isolate host, disable account) is written down
- [ ] Noisy rules are reviewed every week
- [ ] Management gets a monthly report with 5-8 metrics

## Related pages

- [Alert triage](../02-daily-operations/alert-triage.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
- [Operating model](../01-build-a-soc/operating-model.md)
- [Team and roles](../01-build-a-soc/team-and-roles.md)
- [Incident response lifecycle](../03-incident-response/ir-lifecycle.md)
