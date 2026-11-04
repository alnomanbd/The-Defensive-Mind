# Daily Operations

The day-to-day work of a Security Operations Center (SOC): run the shift, triage alerts, hand over, run cases, cut noise, measure results and hunt. Every page is a procedure you can follow on shift, with queries for common tools.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2 / L3, shift lead, SOC manager
    - Time to read: 5 minutes
    - Outcome: you know which page to open for which daily task, and who does what

## Pages in this section

| Page | Open it when you need to... | Main users |
|---|---|---|
| [Daily routine](daily-routine.md) | Start, run and end a shift; run the weekly and monthly tasks | All tiers, shift lead |
| [Alert triage](alert-triage.md) | Decide in 5 to 15 minutes if an alert is real and what happens next | L1, L2 |
| [Severity and SLA](severity-and-sla.md) | Set severity in under a minute and know when to escalate | L1, L2, shift lead |
| [Shift handover](shift-handover.md) | Pass open work to the next shift without dropping anything | All tiers |
| [Case management](case-management.md) | Open, group, run and close a case correctly | L1, L2, L3 |
| [Alert tuning](alert-tuning.md) | Kill noise without creating blind spots | L2, L3, detection engineer |
| [Metrics and KPIs](metrics-and-kpis.md) | Measure the SOC and build the monthly report | SOC manager, shift lead |
| [Threat hunting](threat-hunting.md) | Look for attackers no rule has caught | L3, hunter |

## Who does what, every day

| Task | L1 analyst | L2 analyst | L3 analyst / hunter | SOC manager / lead |
|---|---|---|---|---|
| Watch the queue | Owns it; acknowledges within SLA | Picks up escalations | Picks up complex escalations | Checks SLA breaches daily |
| Triage | Validate, enrich, first verdict on Low/Medium | Scope, verdict on High, confirm L1 escalations | Undetermined and Critical | Reviews a sample weekly |
| Health checks | Runs start-of-shift and hourly checks | Fixes or chases broken sources | Designs silence alerts | Tracks coverage trend |
| Cases | Opens cases, documents | Runs investigation, containment | Leads incidents, forensics | Assigns, reviews quality, closes Critical |
| Tuning | Flags noisy rules with evidence | Proposes tuning with query | Implements and tests rule changes | Approves exceptions |
| Hunting | Not required | Runs hunts from the hunt library | Designs hypotheses, builds new rules | Sets hunt priorities |
| Reporting | Shift statistics | Case summaries | Hunt and detection reports | Monthly report, KPIs |

## If you only do five things

- [ ] One severity scale with response times, published ([Severity and SLA](severity-and-sla.md)).
- [ ] One queue, owned by a named person every hour of coverage.
- [ ] One triage method and note format ([Alert triage](alert-triage.md)).
- [ ] Written plus verbal handover every shift change ([Shift handover](shift-handover.md)).
- [ ] Top 10 noisiest rules reviewed every Monday ([Alert tuning](alert-tuning.md)).

## The daily loop

```text
Alert -> Triage -> Severity/SLA -> Case -> (Incident response section if confirmed)
  |                                  |
  +-- FP / benign --> Tuning ------->+--> Metrics --> Monthly report
                                     ^
Threat hunting --> new detections ---+
Daily routine + handover keep the loop running 24x7
```

## Query conventions used in this section

Queries are shown in tabs for the most common platforms. Index, table and field names are examples; map them to your own.

| Platform | Language | Example data names used here |
|---|---|---|
| Splunk | SPL | `index=wineventlog`, `index=edr`, `index=proxy` |
| Microsoft Sentinel / Defender | KQL (Kusto Query Language) | `SecurityEvent`, `SigninLogs`, `DeviceProcessEvents` |
| Elastic / OpenSearch | ES|QL, KQL or Lucene | `logs-*`, Elastic Common Schema (ECS) fields |
| Wazuh (open source) | Dashboard query (DQL/Lucene) on `wazuh-alerts-*`, plus CLI | `rule.id`, `agent.name`, `data.win.eventdata.*` |

!!! tip "Save these as shared searches"
    Every query on these pages should end up as a saved search or dashboard panel in your SIEM, named the same way across the team (for example `SOC-HEALTH-01 Silent sources`). Analysts should not be retyping queries at 03:00.

## Related pages

- [Incident response section](../03-incident-response/index.md)
- [Phishing playbook](../04-playbooks/phishing.md)
- [Testing and tuning detections](../05-detection-engineering/testing-and-tuning.md)
- [Alert fatigue and notifications](../07-automation-soar/alert-fatigue-and-notifications.md)
- [Shift handover template](../09-templates/shift-handover-template.md)
- [Monthly SOC report template](../09-templates/monthly-soc-report.md)
