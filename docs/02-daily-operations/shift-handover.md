# Shift Handover

How to pass open work from one shift to the next so nothing is dropped, forgotten or done twice. Most incidents that go wrong in a Security Operations Center (SOC) go wrong at a shift change.

!!! abstract "At a glance"
    - Audience: every SOC analyst, shift leads, on-call staff
    - Time to read: 8 minutes
    - Outcome: you can run a written and spoken handover in 10 minutes and know exactly what you own afterwards

## The four rules

| Rule | Why |
|---|---|
| Written **and** spoken | The form is the record; the conversation catches what the form misses |
| The outgoing analyst owns the work until the incoming analyst says "accepted" | No gap where nobody owns an incident |
| Every open item has one named owner after handover | "The team" is not an owner |
| Nothing High or Critical is handed over by message only | Chat at 03:00 gets missed |

## Timeline of a handover

| Before shift end | Outgoing analyst | Incoming analyst |
|---|---|---|
| 30 min | Stop taking new Low alerts unless the queue is empty | |
| 20 min | Fill in the handover form | Arrives, logs in, reads the form |
| 10 min | Spoken handover, incidents and High/Critical first | Repeats each next step back in their own words |
| 0 | | Reassigns cases in the case tool, posts acceptance |
| +15 min | Stays reachable for questions | Runs the start-of-shift health check |

## What goes on the form

1. **Ongoing incidents:** ID, severity, incident lead, phase, next action and time, next stakeholder update.
2. **Open cases:** ID, severity, what was done, the **exact** next step, deadline, new owner.
3. **Pending actions on other teams:** who, what, since when, how to chase.
4. **Platform health:** anything Amber or Red, with ticket numbers.
5. **Watch list:** suspicious activity that is not an alert yet, planned changes tonight, expected noise.
6. **Queue state:** waiting alerts per severity and the oldest alert age.

!!! example "Good and bad next steps"
    | Bad | Good |
    |---|---|
    | Monitor | Re-run the beacon query at 22:00; if WS-0142 calls 203.0.113.10 again, isolate it (approval already given by IT lead, see case note 14) |
    | Follow up with IT | Chase ticket INC-5521 with the IT on-call (ext. 4400) at 21:00 for the firewall block; escalate to IT lead if not done by 23:00 |
    | Check user | Call J. Doe on the number in the directory at 08:30 to confirm the 02:14 login from Germany |

## Acceptance message

Post one line in the SOC channel when you accept:

```text
Handover accepted 20:00. 4 cases taken (1 High), 1 incident ongoing (INC-1042, lead: <name>, next update 21:00). Queue: 0 Critical, 2 High, 17 Medium, 40 Low, oldest 3h.
```

## Handover of a major incident

1. The current lead writes a situation report (sitrep).
2. Both leads join the incident bridge; the outgoing lead hands over in front of the team.
3. The new lead says "I have the incident" on the bridge and in the incident channel.
4. The scribe records the time and names in the incident timeline.

## Queue snapshot queries

Run these just before the handover to fill in the queue state.

=== "Splunk SPL"

    ```spl
    `notable` | search status_label IN ("New","In Progress")
    | eval age_h = round((now() - _time) / 3600, 1)
    | stats count max(age_h) as oldest_h by urgency
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityIncident
    | summarize arg_max(TimeGenerated, *) by IncidentNumber
    | where Status in ("New", "Active")
    | summarize Open = count(), OldestHours = max(datetime_diff('hour', now(), CreatedTime)) by Severity
    ```

=== "Elastic Security"

    ```text
    Alerts page > filter: kibana.alert.workflow_status : "open" > group by kibana.alert.severity
    ```

=== "IBM QRadar"

    ```bash
    # Open offenses with magnitude and start time (API)
    curl -s -H "SEC: $QRADAR_TOKEN" \
      "https://QRADAR/api/siem/offenses?filter=status%3DOPEN&fields=id,magnitude,start_time,assigned_to"
    ```

=== "Wazuh"

    ```text
    Dashboard query on wazuh-alerts-*, last 12 hours:  rule.level >= 7
    Visualise: count split by rule.level
    ```

## When the next analyst does not arrive

1. Do not leave.
2. Phone the incoming analyst, then the shift lead, then the SOC lead.
3. No cover in 30 minutes: the SOC lead decides on extending the shift, calling on-call, or reduced coverage.
4. Record the gap in the daily report.

## Common mistakes

- "Nothing to hand over" with 40 alerts in the queue.
- Leaving before the incoming analyst confirms.
- Forgetting requests to other teams, so nobody chases them.
- Handing over an incident in chat with no call.

## Checklist

- [ ] Every ongoing incident has a lead and a next update time
- [ ] Every open High and Critical case has a next step with a time
- [ ] Pending actions show who is waited on and since when
- [ ] Cases reassigned in the case tool
- [ ] Acceptance posted in the SOC channel

## Downloads

- [SOP-06 Shift Handover (Word)](../downloads/soc-kit/sop/SOP-06-shift-handover.docx)
- [TPL-02 Shift Handover form (Word)](../downloads/soc-kit/tpl/TPL-02-shift-handover.docx)
- [TPL-11 Situation Report (Word)](../downloads/soc-kit/tpl/TPL-11-situation-report.docx)

## Related pages

- [Daily routine](daily-routine.md)
- [Case management](case-management.md)
- [Shift handover template](../09-templates/shift-handover-template.md)
- [Severity and SLA](severity-and-sla.md)
