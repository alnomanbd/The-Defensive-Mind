# Post-Incident Review

How to run a blameless review after an incident and turn it into changes that actually happen. An incident without a review is a lesson paid for and thrown away.

!!! abstract "At a glance"
    - Audience: SOC managers, incident leads, anyone who took part in the incident
    - Time to read: 10 minutes
    - Outcome: you can facilitate a 60 to 90 minute review and leave with owned, dated actions

## When to hold one

| Incident | Review |
|---|---|
| P1 and P2 | Always, within 10 working days of resolution |
| P3 with a useful lesson, a near miss, or a repeat | Short review (30 minutes) |
| Any incident where the SOC missed something for more than a day | Always |
| Tabletop exercises | Yes, same format |

## Blameless means

- We assume people acted in good faith with what they knew then.
- We look for causes in systems, processes and tools, not people.
- Nobody is punished for what they say in the review.
- "Human error" is never a root cause; ask why the system made the error easy.

## Agenda (60 to 90 minutes)

| Time | Item | Led by |
|---|---|---|
| 5 min | Ground rules and purpose | Facilitator (not the incident lead) |
| 10 min | Summary: what happened, impact, key times | Incident lead |
| 30 min | Walk the timeline: at each key point, what did we know, what did we do, what would have helped | Everyone |
| 15 min | What went well, what did not | Everyone |
| 15 min | Root causes and actions | Facilitator |
| 5 min | Owners, dates, follow-up date | Facilitator |

## Questions that find real causes

| Area | Question |
|---|---|
| Prevention | Which control was missing or failed? |
| Detection | Which signal existed but was missed, not collected, or not alerted on? How much earlier could we have known? |
| Triage | Did the alert reach the right person fast enough? Was the severity right? |
| Response | Did the playbook fit? Which steps were missing, wrong or slow? |
| Access | Did responders have the access and tools they needed at the time? |
| Decisions | Were decisions made by the right people, quickly enough? |
| Communication | Did the right people know at the right time? |
| Evidence | Was evidence collected and preserved correctly? |
| Third parties | Did a vendor or provider help or slow us down? |

## Five whys example

```text
Problem: the attacker was inside for 9 days before detection.
Why? No alert fired on the attacker's logins.
Why? Logins came through the VPN, which did not send logs to the SIEM.
Why? The new VPN was installed in March without a log onboarding step.
Why? The change process has no security monitoring checklist.
Action: add "log source onboarded and alert tested" as a required step in the change process for any internet-facing system.
```

## Good actions

| Weak action | Strong action |
|---|---|
| Improve monitoring | Onboard VPN logs to SIEM and enable the "VPN login from new country" rule, owner: SOC engineer, due 2026-12-01 |
| Train users | Run a 15-minute session on MFA push fatigue for finance staff, owner: awareness lead, due 2026-12-15, measured by the next phishing test |
| Be faster | Give the on-call analyst EDR isolation rights without approval for laptops, owner: SOC manager, due 2026-11-20 |

Every action has one owner, one due date, and a tracking reference. Review progress after 30 days.

## Measuring whether reviews work

| Metric | Target |
|---|---|
| P1 and P2 incidents with a review held | 100 percent |
| Review actions closed by due date | 80 percent or more |
| Repeat incidents with the same root cause | Zero |

## Downloads

- [TPL-10 Post-Incident Review (Word)](../downloads/soc-kit/tpl/TPL-10-post-incident-review.docx)
- [TPL-08 Incident Report: Final (Word)](../downloads/soc-kit/tpl/TPL-08-incident-report-final.docx)

## Related pages

- [Post-incident review template](../09-templates/post-incident-review-template.md)
- [IR lifecycle](ir-lifecycle.md)
- [Tabletop exercises](tabletop-exercises.md)
- [Detection lifecycle](../05-detection-engineering/detection-lifecycle.md)
