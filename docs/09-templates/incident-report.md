# Incident Report Template

A fill-in template for the formal written record of a confirmed security incident. Use it while the incident is being handled and finalise it at closure.

!!! abstract "At a glance"
    - Audience: SOC analyst / incident handler / SOC lead
    - Time to read: 5 minutes (30-90 minutes to complete)
    - Outcome: a complete, factual incident record that management, legal teams and auditors can rely on

!!! tip "How to use"
    - Start the report as soon as an event is confirmed as an incident, not at the end.
    - Write facts with timestamps. Mark assumptions clearly as "Assumption:".
    - Use Coordinated Universal Time (UTC) for every timestamp.
    - Keep evidence in your evidence store and reference it by ID here; do not paste raw malware or credentials.
    - Have a second person review the report before it is marked final.

---

## Incident report: `<INC-YYYY-NNNN>`, `<short title>`

### Document control

| Field | Value |
|---|---|
| Incident ID | `<INC-YYYY-NNNN>` |
| Report version | `<1.0>` |
| Classification | `<TLP:AMBER / Confidential>` |
| Author | `<name, role>` |
| Reviewer | `<name, role>` |
| Status | `<Draft / In review / Final>` |
| Last updated | `<YYYY-MM-DD HH:MM UTC>` |

### Summary

| Field | Value |
|---|---|
| Incident type | `<Phishing / Malware / Account compromise / Data exposure / Denial of service / Other>` |
| Severity | `<Critical / High / Medium / Low>` |
| Current status | `<Open: containment / Open, eradication / Recovery / Closed>` |
| Detected at | `<YYYY-MM-DD HH:MM UTC>` |
| Detected by | `<SIEM rule name / EDR alert / user report / third party>` |
| First malicious activity | `<YYYY-MM-DD HH:MM UTC or Unknown>` |
| Contained at | `<YYYY-MM-DD HH:MM UTC>` |
| Closed at | `<YYYY-MM-DD HH:MM UTC>` |
| Incident lead | `<name>` |

**Executive summary (3-5 sentences, no jargon):**

> `<What happened, what was affected, what the business impact is, what has been done, and what is still open.>`

### Scope and impact

| Item | Details |
|---|---|
| Affected users | `<count and list or reference>` |
| Affected hosts | `<hostnames, e.g. ws-0142.example.com>` |
| Affected applications / services | `<names>` |
| Data involved | `<type of data, volume, whether exfiltration is confirmed>` |
| Business impact | `<downtime, financial, customer, regulatory>` |
| Personal data involved? | `<Yes / No / Under investigation>` |
| Regulatory notification needed? | `<Yes / No: decided by <role> on <date>>` |

### MITRE ATT&CK mapping

| Tactic | Technique ID | Technique name | Evidence reference |
|---|---|---|---|
| `<Initial Access>` | `<T1566.001>` | `<Spearphishing Attachment>` | `<EV-001>` |
| `<...>` | `<...>` | `<...>` | `<...>` |

### Timeline

| Time (UTC) | Source | Event | Actor |
|---|---|---|---|
| `<YYYY-MM-DD HH:MM>` | `<mail gateway log>` | `<Phishing email delivered to 4 users>` | Attacker |
| `<YYYY-MM-DD HH:MM>` | `<EDR>` | `<Macro spawned PowerShell on ws-0142>` | Attacker |
| `<YYYY-MM-DD HH:MM>` | `<SIEM>` | `<Alert raised, triaged by analyst>` | SOC |
| `<YYYY-MM-DD HH:MM>` | `<EDR console>` | `<Host isolated>` | SOC |

### Indicators of Compromise (IOCs)

| Type | Value (defanged) | First seen | Context | Shared? |
|---|---|---|---|---|
| Domain | `<bad-example[.]com>` | `<date>` | `<Command and control>` | `<Yes, threat intel platform>` |
| IP address | `<203.0.113[.]45>` | `<date>` | `<Payload download>` | `<No>` |
| File hash (SHA-256) | `<hash>` | `<date>` | `<Dropper>` | `<Yes>` |

### Response actions

| Phase | Action | Owner | Time (UTC) | Result |
|---|---|---|---|---|
| Containment | `<Isolated ws-0142 via EDR>` | `<name>` | `<time>` | `<Done>` |
| Containment | `<Disabled account jdoe, revoked sessions>` | `<name>` | `<time>` | `<Done>` |
| Eradication | `<Removed persistence, reimaged host>` | `<name>` | `<time>` | `<Done>` |
| Recovery | `<Restored user access with new credentials>` | `<name>` | `<time>` | `<Done>` |

### Root cause

- **Root cause:** `<the underlying weakness, e.g. macros allowed from internet files>`
- **Contributing factors:** `<missing control, delayed alert, gap in logging>`
- **How detection worked or failed:** `<which control caught it, and how quickly>`

### Evidence register

| Evidence ID | Description | Location | Collected by | Hash |
|---|---|---|---|---|
| `<EV-001>` | `<Email with headers (.eml)>` | `<evidence store path>` | `<name>` | `<SHA-256>` |
| `<EV-002>` | `<Memory image of ws-0142>` | `<path>` | `<name>` | `<SHA-256>` |

### Communications

| Time (UTC) | Audience | Channel | Message summary | Sent by |
|---|---|---|---|---|
| `<time>` | `<CISO>` | `<phone>` | `<Initial notification>` | `<name>` |

### Follow-up actions

| ID | Action | Owner | Due date | Ticket |
|---|---|---|---|---|
| `<A-1>` | `<Block macros from internet files via policy>` | `<team>` | `<date>` | `<CHG-...>` |
| `<A-2>` | `<New detection for this behaviour>` | `<detection team>` | `<date>` | `<DET-...>` |

### Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Incident lead | `<name>` | `<date>` | `<Approved>` |
| SOC lead | `<name>` | `<date>` | `<Approved>` |

---

## Worked example

??? example "Filled-in report: INC-2026-0042, Phishing leads to mailbox takeover"
    | Field | Value |
    |---|---|
    | Incident type | Account compromise (via phishing) |
    | Severity | High |
    | Status | Closed |
    | Detected at | 2026-03-14 09:12 UTC |
    | Detected by | SIEM rule "New inbox rule forwarding to external domain" |
    | First malicious activity | 2026-03-14 08:41 UTC (credential entry on fake login page) |
    | Contained at | 2026-03-14 09:58 UTC |
    | Closed at | 2026-03-17 16:00 UTC |

    **Executive summary:** A finance user entered their password on a fake sign-in page sent by email. The attacker logged in from abroad and created a rule forwarding invoices to an outside address. The SOC detected the rule 31 minutes after the login, disabled the account and removed the rule within 46 minutes of the alert. Twelve emails were forwarded; none contained card or personal data. Multi-factor authentication (MFA) was not enforced for this user because of an old exception.

    | Time (UTC) | Source | Event |
    |---|---|---|
    | 08:37 | Mail gateway | Email "Invoice overdue" delivered to 6 finance users |
    | 08:41 | Proxy | User jdoe visits `login-example[.]net`, posts form |
    | 08:52 | Identity provider | Sign-in for jdoe from 198.51.100.23, no MFA |
    | 09:05 | Mail audit log | Inbox rule "sync" forwards "invoice" mails to external address |
    | 09:12 | SIEM | Alert raised; L1 analyst picks up at 09:15 |
    | 09:40 | SOC | Escalated to L2, incident declared High |
    | 09:58 | Identity provider | Account disabled, sessions revoked, rule removed |
    | 10:30 | Mail gateway | Same email purged from 5 other mailboxes |

    | Type | Value | Context |
    |---|---|---|
    | Domain | `login-example[.]net` | Credential phishing page |
    | IP address | `198.51.100[.]23` | Attacker sign-in |
    | Email address | `billing@invoice-example[.]org` | Forwarding destination |

    **ATT&CK:** T1566.002 Spearphishing Link, T1078 Valid Accounts, T1114.003 Email Forwarding Rule.

    **Root cause:** MFA exception left on the account after a 2024 device issue. **Contributing:** no alert on sign-ins from new countries for finance users.

    | ID | Action | Owner | Due |
    |---|---|---|---|
    | A-1 | Remove all stale MFA exceptions | Identity team | 2026-03-28 |
    | A-2 | Detection: risky sign-in followed by inbox rule within 1 hour | Detection engineering | 2026-04-04 |
    | A-3 | Block external auto-forwarding by default | Messaging team | 2026-04-11 |

## Checklist

- [ ] All timestamps in UTC and in order
- [ ] Executive summary readable by a non-technical manager
- [ ] IOCs defanged and shared where allowed
- [ ] Evidence referenced with hashes and storage location
- [ ] Follow-up actions have owners and due dates
- [ ] Post-incident review scheduled

## Related pages

- [Post-incident review template](post-incident-review-template.md)
- [Shift handover template](shift-handover-template.md)
- [Detection request](detection-request.md)
- [Templates overview](index.md)
