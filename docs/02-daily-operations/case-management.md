# Case Management

When an alert becomes a case, how to name it, group it, work it and close it, so any analyst can pick it up at any hour and an auditor can follow it a year later.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2 / L3, incident leads
    - Time to read: 10 minutes
    - Outcome: your cases are complete, linked, and pass a quality review

## Alert, case, incident

| Term | Meaning |
|---|---|
| Alert | One detection from one tool |
| Case | A record of investigation work holding one or more related alerts |
| Incident | A case confirmed as a real security incident |
| Observable | An indicator or entity stored in the case: IP, domain, hash, user, host |
| Task | A piece of work inside a case with its own owner |

## When to open a case

| Situation | Case? |
|---|---|
| True positive that needs more than closing the alert | Yes |
| Undetermined alert escalated to L2 | Yes |
| Several related alerts (same user, host or indicator) | Yes, **one** case for all |
| Report from a user, IT, a vendor or law enforcement | Yes |
| Threat hunt finding | Yes |
| False positive or benign positive closed in triage | No, the triage note is enough |
| Blocked attack with no follow-on (blocked scan) | No, close as TP blocked |

!!! tip "Search before you create"
    Before opening a case, search open cases for the same user, host and indicator. One attack spread over ten cases is the most common case-management failure.

## Naming

```text
<Type> - <main entity> - <short description>

Account compromise - jdoe@example.com - login from new country after MFA push spam
Malware - WS-0142 - infostealer executed from Downloads folder
Web attack - shop.example.com - SQL injection attempts with 500 responses
```

## Mandatory fields

| Field | Content |
|---|---|
| Severity | P1 to P4 |
| Classification | Phishing, account compromise, malware, data loss, denial of service, insider, policy violation, other |
| Owner | One named analyst |
| TLP / PAP | Traffic Light Protocol (how widely the case may be shared), Permissible Actions Protocol (what may be done with its indicators) |
| MITRE ATT&CK | Techniques seen, when known |
| Playbook | The playbook being followed |
| Affected assets | Hosts, users, applications, data |
| Detection source | Rule or report that started it |

## Status lifecycle

```text
New -> In progress -> Contained -> Resolved -> Closed
            |  ^
            v  |
          Waiting (blocked on another team or the user: note who and since when)
```

## Writing work notes

Write for a stranger reading it later. Every note says what you looked at, how, and what you found.

| Weak note | Strong note |
|---|---|
| Checked logs, nothing found | Searched proxy logs 2026-11-04 08:00 to 12:00 UTC for WS-0142 (query saved as CASE-1042-Q3): 0 connections to the 3 IOC domains |
| User is fine | Called J. Doe on directory number 10:14 UTC; confirms the 02:14 login was not theirs; password reset and sessions revoked 10:20 |

## Closing a case

- [ ] Final classification: TP incident, TP blocked, benign positive, FP, or duplicate
- [ ] Final severity, with any changes recorded
- [ ] Root cause, or "unknown" with the reason
- [ ] All tasks closed or moved to a follow-up ticket with an owner
- [ ] Confirmed IOCs submitted to the threat intelligence platform
- [ ] Containment reversed where needed (host released, account re-enabled)
- [ ] Incident report and post-incident review for P1 and P2
- [ ] Tuning or detection gap tickets raised
- [ ] Three-to-five sentence resolution summary

P1 and P2 cases are closed by the incident lead or SOC lead.

## Tools

| Tool | Type | Notes |
|---|---|---|
| TheHive | Open source case management | Cases, tasks, observables, Cortex analysers for enrichment |
| DFIR-IRIS | Open source | Strong for forensic-heavy cases and timelines |
| Splunk Enterprise Security / Splunk SOAR | Commercial | Notables and investigations |
| Microsoft Sentinel | Commercial | Incidents with built-in classification and comments |
| IBM QRadar | Commercial | Offenses; IBM QRadar SOAR for full case management |
| Jira Service Management, ServiceNow SecOps | Commercial ticketing | Common when the SOC shares tooling with IT |

## Case metrics queries

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | where CreatedTime > ago(30d)
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | extend HoursToClose = datetime_diff('hour', ClosedTime, CreatedTime)
    | summarize Cases = count(), AvgHoursToClose = avg(HoursToClose),
                StillOpen = countif(Status != "Closed") by Severity
    ```

=== "Splunk SPL"

    ```spl
    `notable` earliest=-30d
    | stats count as cases count(eval(status_label="Closed")) as closed by urgency
    | eval open = cases - closed
    ```

=== "IBM QRadar"

    ```bash
    # Offenses closed in the last 30 days with their closing reason
    curl -s -H "SEC: $QRADAR_TOKEN" \
      "https://QRADAR/api/siem/offenses?filter=status%3DCLOSED&fields=id,magnitude,start_time,close_time,closing_reason_id"
    ```

=== "TheHive"

    ```text
    Cases > filter: status = Open, sort by updatedAt ascending
    Cases with no update for 5+ days go to the weekly review
    ```

## Common mistakes

- One alert, one case, so a single attack ends up in ten cases.
- Cases left "In progress" for weeks with no note.
- Closing without the root cause or without undoing containment.
- Passwords or full customer data pasted into notes.

## Downloads

- [SOP-08 Case Management (Word)](../downloads/soc-kit/sop/SOP-08-case-management.docx)
- [TPL-08 Incident Report: Final (Word)](../downloads/soc-kit/tpl/TPL-08-incident-report-final.docx)
- [TPL-09 Incident Timeline and Decision Log (Word)](../downloads/soc-kit/tpl/TPL-09-incident-timeline-and-decision-log.docx)

## Related pages

- [Alert triage](alert-triage.md)
- [Severity and SLA](severity-and-sla.md)
- [Shift handover](shift-handover.md)
- [Incident report template](../09-templates/incident-report.md)
