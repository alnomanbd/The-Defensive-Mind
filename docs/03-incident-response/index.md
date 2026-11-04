# Incident Response

What the SOC does once an alert is confirmed as a real incident: classify it, escalate it, contain it, collect evidence, communicate, recover, and learn. These pages are the method; the [playbooks](../04-playbooks/index.md) are the attack-specific steps.

!!! abstract "At a glance"
    - Audience: L2 / L3 analysts, incident leads, SOC managers, IT and business staff who join incidents
    - Time to read: 5 minutes
    - Outcome: you know which page to open at each stage of an incident

## Pages in this section

| Page | Open it when you need to... | Main users |
|---|---|---|
| [IR lifecycle](ir-lifecycle.md) | Run an incident from declaration to closure, phase by phase | Incident lead, L2, L3 |
| [Incident classification](incident-classification.md) | Decide what type of incident it is and how severe | L1, L2, incident lead |
| [Escalation and communication](escalation-and-communication.md) | Tell the right people, at the right time, in the right words | Incident lead, SOC manager |
| [Evidence handling](evidence-handling.md) | Collect and preserve evidence so it stands up later | L2, L3, forensics |
| [Post-incident review](post-incident-review.md) | Turn the incident into real improvements | SOC manager, incident lead |
| [Tabletop exercises](tabletop-exercises.md) | Practise an incident before it happens | SOC manager, CISO |

## The incident in one picture

```text
Alert -> Triage -> Declare incident (severity, lead, channel)
                      |
          +-----------+-----------+
          |                       |
     Investigate  <------>   Contain        (evidence collected throughout)
          |                       |
          +-----> Eradicate -> Recover -> Close -> Post-incident review
                                                        |
                      Detections, playbooks, controls <-+
```

## Roles during an incident

| Role | Job | Usually |
|---|---|---|
| Incident lead (incident commander) | Owns the incident, makes or obtains decisions, sets priorities | L3 or SOC lead |
| Investigators | Find scope and root cause | L2, L3, forensics |
| Responders | Carry out containment and recovery | IT operations, cloud, network, application teams |
| Scribe | Keeps the timeline and decision log | Any analyst |
| Communications lead | Writes updates for staff, management, customers | CISO office or communications team |
| Executive sponsor | Business decisions: shutdowns, notifications, legal | CISO or senior executive |
| Legal and privacy | Notification duties, privilege, law enforcement | Legal counsel, privacy officer |

!!! tip "One lead, always"
    Every incident has exactly one named lead at any moment. When the lead changes, it is said on the bridge and written in the timeline.

## Downloads

- [TPL-07 Incident Report: Initial Notification](../downloads/soc-kit/tpl/TPL-07-incident-report-initial-notification.docx)
- [TPL-08 Incident Report: Final](../downloads/soc-kit/tpl/TPL-08-incident-report-final.docx)
- [TPL-09 Incident Timeline and Decision Log](../downloads/soc-kit/tpl/TPL-09-incident-timeline-and-decision-log.docx)
- [TPL-10 Post-Incident Review](../downloads/soc-kit/tpl/TPL-10-post-incident-review.docx)
- [TPL-11 Situation Report](../downloads/soc-kit/tpl/TPL-11-situation-report.docx)
- [SOP-05 Severity Assignment and Escalation](../downloads/soc-kit/sop/SOP-05-severity-assignment-and-escalation.docx)

## Related pages

- [Playbooks](../04-playbooks/index.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Case management](../02-daily-operations/case-management.md)
