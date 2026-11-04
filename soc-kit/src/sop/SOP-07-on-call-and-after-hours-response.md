---
id: SOP-07
title: On-Call and After-Hours Response
owner: SOC Lead
audience: On-call analysts, SOC engineers, shift leads
review: Every 12 months, and after any missed after-hours page
summary: How the SOC covers nights, weekends and holidays when nobody is watching the screen: who carries the phone, what pages them, how fast they respond and how the work is handed back.
---
## 1. Purpose

Attackers prefer nights, weekends and public holidays because they expect nobody to be watching. A SOC without 24-hour staff still needs a reliable way to detect and respond to serious attacks outside office hours. This procedure defines the on-call model.

## 2. Scope

- All hours not covered by staffed shifts.
- Alerts of P1 and P2 severity, and P3 alerts from rules marked "page after hours".
- Out of scope: routine triage of P3 and P4 alerts, which wait for the next shift.

## 3. On-call model

| Item | Standard |
|---|---|
| Rotation | One primary and one secondary on-call analyst per week, handover at a fixed day and time |
| Escalation backup | Incident lead or SOC Lead on a separate rotation |
| Paging tool | A paging or on-call tool with phone call and app alerts (for example PagerDuty, Opsgenie, Grafana OnCall, or a SOAR flow that calls a phone). Chat messages alone are not enough |
| Equipment | Company laptop, VPN, MFA device, phone charged, access to all SOC consoles tested before the week starts |
| Fitness | On-call staff stay sober and within reach of their laptop. Swap shifts if you cannot |
| Rest | After a night with more than 2 hours of work, the analyst may start late the next day |

## 4. What pages the on-call analyst

| Source | Pages after hours |
|---|---|
| Any alert or incident rated P1 or P2 | Yes |
| Named high-risk rules (for example success after brute force, ransomware behaviour, new domain admin, EDR tamper, mass file rename) | Yes, whatever their default severity |
| Critical log sources silent for more than 2 hours (domain controllers, firewalls, identity provider, EDR) | Yes |
| SOC platform down | Yes |
| Calls from IT operations, the service desk, or management about a suspected attack | Yes |
| Everything else | No, waits for the next shift |

> TIP: Review the paging list every quarter. Too many pages burn people out and they start ignoring them; too few and attacks go unseen.

## 5. Response times

| Step | P1 | P2 |
|---|---|---|
| Acknowledge the page | 10 minutes | 15 minutes |
| Start working (logged into consoles) | 20 minutes | 30 minutes |
| Triage decision | 45 minutes | 1 hour 30 minutes |
| If primary does not acknowledge | Secondary is paged automatically at 10 minutes | Secondary at 15 minutes |
| If secondary does not acknowledge | Incident lead or SOC Lead at 20 minutes | At 30 minutes |

## 6. Procedure

### 6.1 Start of the on-call week

1. Receive the handover from the previous on-call analyst (TPL-02).
2. Test: VPN, MFA, SIEM, EDR, case tool and paging app. Send yourself a test page.
3. Confirm in the SOC channel: `On-call this week: primary <name>, secondary <name>, backup <name>.`
4. Open a new On-Call Log (TPL-28).

### 6.2 When paged

1. Acknowledge in the paging tool so the timer stops.
2. Log in and triage using SOP-03. Severity using SOP-05.
3. False positive or not urgent: close or leave for the next shift with a clear note. Record in TPL-28.
4. Confirmed P1 or P2: escalate per SOP-05 by phone. Do not wait until morning.
5. Take only the containment actions the playbook allows the on-call analyst to take alone (for example isolate one laptop, disable one user account, block one IP). Anything with business impact needs the approval named in the playbook.

### 6.3 If you cannot handle it

Call the secondary or backup. Being on call does not mean being alone. It is always correct to escalate at 3 a.m. when unsure about a P1 or P2.

### 6.4 Handing back to the day shift

1. Before the first shift starts, write a short summary in TPL-28 and the shift handover.
2. Hand over every open item in person or by call at shift start (SOP-06).
3. Hours worked go into the on-call log for time-off and payment.

### 6.5 End of the on-call week

1. Hand over to the next on-call analyst with TPL-02.
2. Send TPL-28 to the SOC Lead.
3. List noisy pages for tuning (SOP-10).

## 7. Holidays and special days

- Publish the on-call rota for public holidays at least 4 weeks ahead.
- Before long holidays, the SOC Lead checks with threat intelligence for known holiday campaigns and briefs on-call staff.
- During major business events (product launch, year-end close), consider staffed shifts instead of on-call.

## 8. Records

- TPL-28 On-Call Log for every week: each page, time acknowledged, action, outcome, hours worked.
- Paging tool reports (acknowledge times).

## 9. Metrics

| Metric | Target |
|---|---|
| Pages acknowledged within the target time | 95 percent or more |
| Pages escalated to secondary because primary missed | Under 5 percent |
| Pages per week that were false positives | Falling; above 50 percent triggers a tuning review |
| After-hours P1 and P2 with response started on time | 100 percent |

## 10. Common mistakes

- Paging by chat message that nobody hears at night.
- An on-call analyst whose VPN or MFA does not work, found out at 2 a.m.
- Paging on every Medium alert, so staff mute the app.
- Containing with high business impact without approval, or not containing at all because "it is night".
- No handback in the morning, so the day shift does not know what happened.

## 11. Related documents

- SOP-03 Alert Triage and Classification, SOP-05 Severity Assignment and Escalation, SOP-06 Shift Handover, SOP-19 Host Isolation and Release, SOP-25 Account Disable and Session Revocation
- TPL-28 On-Call Log, TPL-02 Shift Handover, GOV-04 Escalation and Contact Matrix
