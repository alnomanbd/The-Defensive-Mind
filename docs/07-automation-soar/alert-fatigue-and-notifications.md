# Alert Fatigue and Notifications

How to stop drowning your analysts in alerts, and how to send the right alert to the right place at the right time. Alert fatigue is when there are so many alerts, most of them noise, that people stop paying attention, and the real one slips through. It is the most common way a SOC fails while looking busy.

!!! abstract "At a glance"
    - Audience: SOC lead, SOC manager, detection engineer
    - Time to read: 10 minutes
    - Outcome: ways to cut alert volume and a sane notification design

!!! danger "Alert fatigue is a security failure, not a people problem"
    When analysts miss a real alert in a flood of noise, the fix is not "pay more attention". It is to cut the noise. A queue nobody can keep up with is a queue nobody is really watching. Treat alert volume as a top operational risk.

## Why fatigue happens

| Cause | Example |
|---|---|
| Too many low-value detections at high severity | Every blocked scan raised as "critical" |
| No deduplication | One attack creates 500 separate tickets |
| Untuned rules | A noisy rule nobody fixed, firing all day |
| No prioritisation | A real P1 sits in the same flat list as noise |
| Notifying everything everywhere | Every alert pinged to a channel until people mute it |

## Cut the volume at the source

The best alert is the one you never had to look at because it was never raised as noise.

- [ ] Tune noisy rules. One rule firing thousands of times is a tuning job, not an analyst job ([Alert tuning](../02-daily-operations/alert-tuning.md)).
- [ ] Set severity by real impact. Blocked, failed, external-only scanning is usually low, not critical.
- [ ] Deduplicate. Group related alerts into one case ([Case deduplication](case-deduplication.md)).
- [ ] Auto-close tight benign patterns (your own scanners, health checks).
- [ ] Suppress known, accepted conditions with a documented, time-limited exception, not by deleting the rule.

!!! warning "Suppress with a reason and a review date"
    Silencing an alert is sometimes right, but an undocumented, permanent suppression is how blind spots are born. Every suppression needs a reason, an owner and a review date, so "we turned that off" does not become "we never see that attack".

## Design notifications properly

Not every alert needs a notification, and not every notification needs to interrupt a human. Match the channel to the urgency.

| Severity | Where it goes | How loud |
|---|---|---|
| P1 Critical | Phone call or page to on-call, plus the incident channel | Interrupt, now |
| P2 High | Direct message or ticket to the owner; channel post | Prompt, within SLA |
| P3 Medium | Queue and a quiet channel | Looked at in the daily round |
| P4 Low | Queue only, or a daily digest | No live notification |

Principles:

- [ ] One event, one notification. Deduplicate before you notify.
- [ ] Route by severity. Do not send everything to one channel until people mute it.
- [ ] Make notifications actionable: who, what, where, and a link to the case, not just "alert fired".
- [ ] Digest the low stuff. A single daily summary beats a hundred pings.
- [ ] Protect out-of-hours. Only genuine P1 and P2 should wake someone.

## The notification trap

A channel that gets a message for every alert is a channel people stop reading within a week. Once muted, even the real P1 is missed. Send fewer, better notifications. If a notification does not need action, it does not need to interrupt anyone; put it in a digest or the queue.

## Measure fatigue

| Metric | What it tells you |
|---|---|
| Alerts per analyst per shift | Is the queue humanly workable? |
| False positive rate | How much of the queue is noise |
| Percentage of alerts auto-closed or grouped | How much automation is helping |
| Time alerts sit unacknowledged | Whether the queue is really being worked |
| Top 10 noisiest rules | Your tuning backlog |

Review the noisiest rules every week and fix the top few. A small, steady tuning habit keeps the queue workable far better than an occasional big cleanup.

## A healthy queue

You know fatigue is under control when:

- [ ] An analyst can work the whole queue in a shift without rushing.
- [ ] Most alerts are real enough to be worth looking at.
- [ ] A P1 stands out immediately; it is not buried in noise.
- [ ] Out-of-hours notifications are rare and always worth the interruption.
- [ ] The team trusts the alerts, so they act on them instead of ignoring them.

## Related pages

- [Alert tuning](../02-daily-operations/alert-tuning.md)
- [Case deduplication](case-deduplication.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
