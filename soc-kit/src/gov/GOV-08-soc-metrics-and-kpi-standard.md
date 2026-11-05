---
id: GOV-08
title: SOC Metrics and KPI Standard
owner: SOC Manager
audience: SOC team, leadership
review: Every 12 months
summary: The metrics the SOC measures and reports, defined the same way every time, so trends are real and leadership sees outcomes rather than activity.
---
## 1. Purpose

This standard defines the metrics the SOC of [ORGANISATION] measures and reports. Consistent definitions make trends meaningful. The focus is on outcomes (how fast real incidents are caught and contained) not on vanity numbers (how many alerts were closed).

> WARNING: Measuring the team on alert volume or alerts closed rewards speed over correctness, including closing real alerts as benign to clear the queue. Measure outcomes, not activity.

## 2. Core metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Time to acknowledge (MTTA) | Time from an alert arriving to a human taking ownership | Shows whether the queue is keeping up |
| Time to respond or contain (MTTR) | Time from detection to the threat being contained | The number leadership cares about most |
| False positive rate | Share of alerts that were not real or not malicious | Shows noise and tuning backlog |
| SLA attainment | Share of alerts and incidents handled within the GOV-03 times | Shows whether commitments are met |
| Detection coverage | Techniques reliably detected, mapped to ATT&CK | Shows blind spots near real risk |
| Escaped incidents | Real incidents found late or by someone else | The honest measure of what was missed |

## 3. How each metric is calculated

Define each the same way every time. For example:

- **MTTA** = median time from alert creation to first ownership, over the period.
- **MTTR** = median time from detection to containment for confirmed incidents, by severity.
- **False positive rate** = false-positive closures divided by total alerts closed.
- **SLA attainment** = alerts and incidents meeting their GOV-03 time divided by the total, by severity.

Use the median, not the average, for time metrics; a few long outliers distort the average.

## 4. Supporting metrics

| Metric | Shows |
|---|---|
| Alerts per analyst per shift | Whether the queue is humanly workable |
| Top 10 noisiest rules | The tuning backlog |
| Alerts auto-closed or grouped | How much automation is helping |
| Post-incident review actions closed on time | Whether lessons turn into change |
| Log source health (silent sources) | Blind spots in collection |

## 5. Reporting cadence

| Audience | Cadence | Content |
|---|---|---|
| SOC team | Weekly | Queue health, noisiest rules, SLA trend |
| SOC manager | Weekly | All core metrics |
| Leadership | Monthly | Outcomes, trends, risks and needs (one page) |
| Executives | Quarterly | Posture, maturity, major incidents |

## 6. Using metrics well

- [ ] Report trends, not single numbers; direction matters more than a point.
- [ ] Tie metrics to decisions: staffing, tuning, tooling.
- [ ] Never use metrics to blame individuals; they measure the system.
- [ ] Review definitions yearly so "better numbers" always means "better security".

## 7. Review

Reviewed every 12 months.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
