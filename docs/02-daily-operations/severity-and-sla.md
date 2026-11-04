# Severity and SLA

Set severity in under a minute from impact and urgency, then follow the Service Level Agreement (SLA) clock and escalation timers below. The analyst sets case severity after triage; the rule's default level is only a starting point. When in doubt, go one level higher and downgrade later.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2 / L3, shift lead, SOC manager
    - Time to read: 10 minutes
    - Outcome: you can assign and defend a severity, and you know exactly when and to whom to escalate

## Step 1: rate impact

| Impact | Pick this if... |
|---|---|
| Severe | Business-critical system or many users; regulated or sensitive data at risk; major legal or reputational exposure |
| Significant | Important system or privileged account; limited sensitive data; one business unit disrupted |
| Moderate | One standard user or host; no sensitive data confirmed at risk |
| Minor | No real damage; blocked attempt or policy violation |

## Step 2: rate urgency

| Urgency | Pick this if... |
|---|---|
| Immediate | Attacker active, spreading, data leaving, or encryption running now |
| High | Confirmed compromise, not contained, no sign of spread |
| Normal | Contained or one-off; needs investigation, no time pressure |
| Low | Informational |

## Step 3: read the matrix

| Impact \ Urgency | Immediate | High | Normal | Low |
|---|---|---|---|---|
| **Severe** | Critical | Critical | High | Medium |
| **Significant** | Critical | High | Medium | Low |
| **Moderate** | High | Medium | Medium | Low |
| **Minor** | Medium | Low | Low | Low |

## Step 4: apply modifiers (+1 level each, max Critical)

- [ ] Privileged identity involved (domain admin, cloud global admin, root, break-glass).
- [ ] Executive or high-profile target, and the attack succeeded.
- [ ] Regulated data confirmed in scope (personal, payment card, health).
- [ ] Same activity on more than 10 hosts or users.

## Real examples per level

| Severity | Examples |
|---|---|
| Critical | Ransomware encrypting file servers; domain admin credentials used by attacker; bulk customer data leaving now; remote code execution on production web app; cloud tenant admin taken over |
| High | Malware executed on a server, contained, entry point unknown; mailbox compromised and sending internal phishing; valid staff credentials on a dark web market; exploited internet-facing host, no follow-on yet; DDoS (Distributed Denial of Service) degrading a customer service |
| Medium | One workstation with commodity malware, isolated; one user clicked phishing, no credentials entered; external brute force with no success; sensitive file uploaded to personal cloud storage |
| Low | Reported phishing already blocked; internet port scan on hardened perimeter; adware on one workstation; user locked out after forgetting password |

!!! example "Scoring in practice"
    Phishing link clicked by a finance user, credentials entered, attacker signed in from 198.51.100.23 and created an inbox forwarding rule 20 minutes ago. Impact: Significant (finance mailbox). Urgency: High (compromise confirmed, not yet contained). Matrix: **High**. Modifier: none. Result: **High**, containment must start within 4 hours (in practice: revoke sessions now).

## SLA targets (24x7 SOC starting points)

| Severity | Acknowledge | Triage done | Containment started | Update cadence | Target resolution |
|---|---|---|---|---|---|
| Critical | 15 min | 30 min | 1 hour | Hourly | Contained and stable in 24 to 72 h |
| High | 30 min | 2 h | 4 h | Every 4 h | 3 to 5 days |
| Medium | 2 h | 8 h | 1 business day | Daily | 10 business days |
| Low | 1 business day | 2 business days | As needed | On closure | 30 days |

- **Acknowledge:** a named analyst owns it. Mean Time to Acknowledge (MTTA) runs from alert creation, not from pickup.
- **Containment started:** first action that limits the attacker (isolate, disable, block).
- Business-hours SOCs: keep Critical and High 24x7 through on-call; move Medium and Low to business hours.

!!! warning "Do not close early to hit a target"
    A case closed on time and reopened next week is worse than a late, correct closure. Report breaches honestly with a reason.

## Escalation timers (automatic, not a judgement call)

| Severity | Trigger | Escalate to | How |
|---|---|---|---|
| Critical | Not acknowledged in 15 min | Shift lead; on-call incident manager at 30 min | Page + phone |
| Critical | Confirmed | SOC manager, incident manager, CISO (Chief Information Security Officer) within 1 h | Phone, then written notice |
| High | Not acknowledged in 30 min | Shift lead | Page or chat mention |
| High | Not contained in 4 h | SOC manager | Phone or chat |
| Medium | Not acknowledged in 2 h | Shift lead | Chat |
| Medium | Open past 10 business days | SOC manager | Weekly review |
| Low | Open past 30 days | SOC manager | Monthly review |

Who to call and what to say: [Escalation and communication](../03-incident-response/escalation-and-communication.md).

## Who does what

| Role | Responsibility |
|---|---|
| L1 | Sets initial severity after triage; acknowledges within SLA; escalates High and Critical immediately |
| L2 | Confirms or changes severity on escalation; owns containment clock for High |
| L3 | Owns Critical technical response; downgrades only after verified containment |
| Shift lead | Watches SLA timers; reassigns stuck items; first escalation point |
| SOC manager | Owns the matrix and targets; reviews breaches and severity distribution monthly |

## SLA breach query

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | where CreatedTime > ago(30d)
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | extend AckMin = datetime_diff('minute', FirstModifiedTime, CreatedTime)
    | extend TargetMin = case(Severity == "High", 30, Severity == "Medium", 120, 1440)
    | extend Breached = AckMin > TargetMin
    | summarize Total = count(), Breaches = countif(Breached),
                MedianAckMin = percentile(AckMin, 50) by Severity
    ```

=== "Splunk SPL (Enterprise Security)"

    ```spl
    | `incident_review`
    | where _time > relative_time(now(), "-30d")
    | stats min(_time) as first_action by rule_id, urgency
    | join rule_id [| `notable` | where _time > relative_time(now(), "-30d") | rename event_id as rule_id, _time as created | fields rule_id, created]
    | eval ack_min = round((first_action - created) / 60)
    | eval target = case(urgency="critical",15, urgency="high",30, urgency="medium",120, true(),1440)
    | stats count as total, sum(eval(if(ack_min > target,1,0))) as breaches, median(ack_min) as median_ack by urgency
    ```

## Changing severity

Record time, old level, new level and a one-line reason every time.

| Raise when | Lower when |
|---|---|
| More hosts or users found | Containment verified (not just requested) |
| Privileged account involved | Scope proved smaller |
| Sensitive data confirmed | Activity proved authorised |
| Attacker active after containment | Threat removed, no recurrence for 48 h |

!!! danger "Common mistakes"
    - Copying the rule default to the case: severity is set by the analyst after triage.
    - Everything is High: expect roughly 1% Critical and 5 to 10% High; review the distribution monthly.
    - Never downgrading: Critical loses meaning and people burn out.
    - Starting the clock at pickup: hides queue delay from your metrics.
    - Different scales in SOC and IT ticketing: publish a mapping table.

## Checklist

- [ ] Matrix, modifiers and examples published and identical across teams.
- [ ] SLA timers start at alert creation and are tracked by the case tool.
- [ ] Missed-SLA escalation pages someone automatically.
- [ ] Every severity change has a reason in the case.
- [ ] Monthly review of breaches and severity distribution.

## Related pages

- [Alert triage](alert-triage.md)
- [Case management](case-management.md)
- [Metrics and KPIs](metrics-and-kpis.md)
- [Incident classification](../03-incident-response/incident-classification.md)
- [Escalation and communication](../03-incident-response/escalation-and-communication.md)
- [Alert fatigue and notifications](../07-automation-soar/alert-fatigue-and-notifications.md)
