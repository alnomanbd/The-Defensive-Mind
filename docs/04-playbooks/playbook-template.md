# Playbook Template

Copy this page to create a new playbook. Keep every heading; write "Not applicable" rather than deleting a section, so all playbooks stay comparable.

!!! abstract "At a glance"
    - Audience: playbook authors
    - Time to read: 5 minutes
    - Outcome: a playbook that any analyst can follow under pressure

---

# Playbook: <Incident Type>

| Field | Value |
|:---|:---|
| **ID** | PB-XX |
| **Default severity** | Low / Medium / High / Critical (see [Severity and SLA](../02-daily-operations/severity-and-sla.md)) |
| **Escalate to Critical when** | Condition that raises severity |
| **MITRE ATT&CK** | Txxxx Technique name, ... |
| **Typical alerts** | Detection names / log sources that start this playbook |
| **Owner** | Role responsible for keeping this playbook current |
| **Last reviewed** | YYYY-MM-DD |

## 1. Summary

Two to four sentences: what the attack is, why it matters, what success looks like for the defender.

## 2. Triggers and detection

- Alerts and log sources that indicate this incident
- What a true positive usually looks like
- Common false positives and how to rule them out

## 3. Triage (first 15-30 minutes)

- [ ] Step with a clear yes/no outcome
- [ ] ...

Decision: true positive, continue; false positive, close with reason; unsure, escalate.

## 4. Investigation

Questions to answer, with where to look (log source, query idea):

| Question | Where to look |
|:---|:---|
| Who / what is affected? | ... |
| When did it start? | ... |
| How did the attacker get in? | ... |
| What else did they touch? | ... |

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| ... | SOC / IT / Cloud | ... |

## 6. Eradication and recovery

- [ ] Remove the cause
- [ ] Restore from known-good state
- [ ] Monitor for recurrence (how long, which alerts)

## 7. Communication

Who must be informed, when, and by whom. Link to [Escalation and Communication](../03-incident-response/escalation-and-communication.md).

## 8. Evidence to keep

Logs, files, screenshots, hashes, and where they are stored. Follow [Evidence Handling](../03-incident-response/evidence-handling.md).

## 9. Lessons learned

Questions for the [Post-Incident Review](../03-incident-response/post-incident-review.md), and detections or controls that should be added.

## Related pages

- Links to related playbooks, detections and templates
