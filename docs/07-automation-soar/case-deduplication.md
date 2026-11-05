# Case Deduplication

How to turn a flood of related alerts into one case, so analysts work the incident, not a hundred tickets about it. A single attack can fire hundreds of alerts: one per failed login, one per file encrypted, one per host scanned. Without deduplication, the SOC spends its time closing tickets instead of stopping the attack.

!!! abstract "At a glance"
    - Audience: detection engineer, automation engineer, L2
    - Time to read: 10 minutes
    - Outcome: ways to group related alerts into cases and keep the queue sane

!!! tip "One incident, one case"
    The goal is simple: everything about a single incident lives in one case. An analyst should open one case and see the whole attack, not reconstruct it from two hundred separate alerts.

## Why one attack makes many alerts

| Attack | Alerts it can fire |
|---|---|
| Password spraying | One alert per failed login, across many accounts |
| Ransomware | One per file change, per host, per shadow-copy deletion |
| Port scan | One per port or per target |
| Phishing campaign | One per recipient who got the mail |
| Web attack | One per malicious request |

Each alert on its own is noise. Together they are one story. Deduplication tells the story.

## Ways to group alerts

| Method | Groups by | Good for |
|---|---|---|
| By entity | Same user, host, or IP within a time window | Most incidents; the attacker reuses the same account or host |
| By detection plus source | Same rule, same source, within a window | A single noisy source, like one scanner |
| By campaign | Same indicator across many targets (one phishing sender, one malware hash) | Phishing and malware campaigns |
| By attack chain | Alerts that match steps of one attack on one target over time | Showing an intrusion as a sequence, not scattered events |
| By asset | Alerts touching the same important system | Watching a crown jewel |

Most SOCs start with "same entity within a time window" (for example, group all alerts about host X in the last hour) and add smarter grouping later.

## How to build it

- [ ] Decide the grouping key: usually entity (user, host, IP) plus a time window.
- [ ] Set the window: long enough to catch a slow attack, short enough not to merge unrelated events. One to a few hours is a common start.
- [ ] When a new alert arrives, check for an open case with the same key; attach it if found, open a new case if not.
- [ ] Raise the case severity to the highest of its alerts, and update it as new alerts attach.
- [ ] Show the alert count and timeline on the case, so the analyst sees the scale at a glance.

Many SIEMs and case tools can do this natively (correlation, alert grouping, entity-based cases). A SOAR or script can do it where the tools cannot.

## Keep it from hiding things

Grouping is powerful, which means it can also bury a real signal if done carelessly.

!!! warning "Do not let grouping swallow an escalation"
    If an attack starts as noise (scanning) and becomes serious (a successful login), the serious alert must stand out, not vanish into a big benign case. Make the case severity rise when any alert in it crosses a threshold, and re-notify when a case becomes critical. A case that quietly grew to P1 and nobody was told is worse than a hundred tickets.

Safeguards:

- [ ] Bump severity and re-notify when a grouped case crosses into high or critical.
- [ ] Do not auto-close a case just because its early alerts were benign; the later ones may not be.
- [ ] Keep the full alert list inside the case, so nothing is lost, only grouped.
- [ ] Set a sensible window; too long merges unrelated incidents, too short splits one incident into many.

## What good looks like

| Before deduplication | After |
|---|---|
| 500 tickets for one password-spray | One case: "password spraying, 500 attempts, 1 success", with the timeline |
| Analyst closes tickets for an hour | Analyst reads one case and acts |
| The one successful login lost in the pile | The success raises the case to high and re-notifies |
| No sense of the attack's scale | The case shows count, spread and timeline at a glance |

## Measure it

| Metric | Shows |
|---|---|
| Alerts per case | How much grouping is compressing noise |
| Cases per day vs alerts per day | The real workload after deduplication |
| Time to work a case, before and after | Whether grouping is saving time |
| Escalations missed inside grouped cases | Whether grouping is hiding anything (should be zero) |

## Related pages

- [Alert fatigue and notifications](alert-fatigue-and-notifications.md)
- [Case management](../02-daily-operations/case-management.md)
- [Automation catalog](automation-catalog.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
