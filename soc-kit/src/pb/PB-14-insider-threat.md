---
id: PB-14
title: Insider Threat
owner: SOC manager with HR and legal
audience: SOC analyst L2 / L3, SOC manager, HR and legal contacts
review: Every 12 months, and after every real incident that used this playbook
summary: "How to handle suspected harmful activity by an employee, contractor or partner who already has legitimate access: data theft before leaving, sabotage, fraud, or misuse of privileged access. These cases are different: they involve a named person, HR, legal and privacy, and a mistake can harm an innocent colleague."
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-14 |
| **Default severity** | P2 High, handled with restricted access (see Severity and SLA) |
| **Escalate to Critical when** | Sabotage of production systems, theft of regulated data, a privileged administrator is involved, or there is a risk to people's safety |
| **MITRE ATT&CK** | T1078 Valid Accounts, T1530 Data from Cloud Storage, T1567 Exfiltration Over Web Service, T1052.001 Exfiltration over USB, T1485 Data Destruction, T1098 Account Manipulation, T1136 Create Account |
| **Typical alerts** | UEBA (user and entity behaviour analytics) risk score jump, mass download before a resignation date, USB copy of many files, access to data outside the person's role, admin creating a hidden account, logs deleted by an admin, a manager or HR referral |
| **Owner** | SOC manager with HR and legal |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

Insider threats come in three kinds: **malicious** (someone deliberately steals or damages), **negligent** (someone breaks rules carelessly, for example emailing customer data to a personal address to work from home), and **compromised** (an outside attacker using an insider's account, which is really Account Compromise). The SOC's job is to collect facts, not to judge people. Success for the defender: risk is contained, evidence is collected lawfully and kept intact, only the people who need to know are told, and the decision about the person is made by HR and management with facts.

> WARNING: Rules that always apply. Do not start monitoring a named person without written approval from HR and legal (and in some countries, a works council). Do not tell the person, their team or their manager unless HR says so. Do not interview anyone. Analysts collect technical facts only. Restrict the case in the case management tool to named investigators.


## 2. Triggers and detection

| Signal | Example | Log source |
|:---|:---|:---|
| Leaver activity | Large downloads or email to personal addresses in the weeks before the last day | HR leaver list joined with DLP, proxy, SaaS audit |
| Access outside role | A sales user opening finance shares or source code repositories | File audit, SaaS audit, UEBA |
| Removable media | Thousands of files copied to USB | EDR device control, Windows 6416 and 4663 |
| Privileged misuse | Admin creates an account, grants themselves rights, disables logging, reads executives' mailboxes | AD 4720, 4728, 4732; M365 mailbox audit; cloud audit logs |
| Sabotage | Deletion of repositories, backups or VMs; logic bombs in scheduled tasks | SaaS and cloud audit, backup console, EDR |
| Referral | A manager, colleague or HR reports a concern | Phone, email, ethics hotline |

**Common false positives:** a role change (new access is legitimate), a leaver handing over files properly to a colleague, an admin doing approved work under a change ticket, project work that needs bulk exports.

## 3. Triage (first day, discreetly)

- [ ] Write down exactly what triggered the case and who knows about it.
- [ ] Inform the SOC manager. The SOC manager contacts HR and legal before anything else is done.
- [ ] Get written approval and the scope: which person, which systems, what time window.
- [ ] Check whether the activity matches a change ticket, a role change or a manager-approved task.
- [ ] Check whether the account itself may be compromised (new devices, odd sign-in locations, MFA changes). If yes, switch to Account Compromise.
- [ ] Is the person still employed, and what is their last working day?

Decision: legitimate business reason confirmed, close with a restricted note; account compromise, switch playbook; possible malicious or negligent insider, continue with HR and legal approval; sabotage in progress, contain immediately (P1), then inform HR.

## 4. Investigation

Collect facts within the approved scope only.

| Question | Where to look |
|:---|:---|
| What data did the person access, and was it normal for their role? | File server audit, SharePoint and Drive audit, database audit; compare with peers in the same team |
| What left the organisation, and how? | DLP, proxy, email to personal domains, USB events, cloud storage uploads, printing logs |
| When did the behaviour change? | UEBA timeline, activity volume per week for the last 90 days |
| Was any access abused or created? | AD and cloud admin audit logs, new accounts, permission changes, log deletion |
| Is anyone else involved? | Shared destinations, emails between accounts, the same USB device serial on other hosts |

### Queries: activity of one user before their leaving date

**Microsoft Sentinel KQL**


```kql
let user = "jdoe@example.com";
OfficeActivity
| where TimeGenerated > ago(60d) and UserId =~ user
| where Operation in ("FileDownloaded","FileSyncDownloadedFull","FileCopied","AnonymousLinkCreated","SharingInvitationCreated")
| summarize Files = count(), Sites = make_set(Site_Url, 10) by Operation, bin(TimeGenerated, 1d)
| order by TimeGenerated asc
```

**Splunk SPL**


```spl
index=o365 user="jdoe@example.com" earliest=-60d
  Operation IN ("FileDownloaded","FileSyncDownloadedFull","AnonymousLinkCreated","SharingInvitationCreated")
| timechart span=1d count by Operation
```

**Elastic**


```text
user.email : "jdoe@example.com" and event.action : ("FileDownloaded" or "FileSyncDownloadedFull" or "AnonymousLinkCreated")
(Lens: count per day, last 60 days)
```

**IBM QRadar AQL**


```sql
SELECT DATEFORMAT(starttime, 'yyyy-MM-dd') AS day, QIDNAME(qid) AS action, COUNT(*) AS n
FROM events
WHERE username = 'jdoe@example.com'
  AND (QIDNAME(qid) ILIKE '%download%' OR QIDNAME(qid) ILIKE '%sharing%')
GROUP BY day, action ORDER BY day LAST 60 DAYS
```

**Wazuh**


```text
data.office365.UserId:"jdoe@example.com" and data.office365.Operation:(FileDownloaded or FileSyncDownloadedFull or AnonymousLinkCreated)
```

**osquery**


```sql
-- USB storage devices seen on the user's laptop
SELECT vendor, model, serial, removable FROM usb_devices;
SELECT * FROM disk_events WHERE action = 'add';  -- macOS only
```

## 5. Containment

Timing is a joint decision with HR and legal. Acting too early can warn the person and destroy evidence; acting too late can lose data.

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Preserve first: legal hold on the mailbox, OneDrive or Drive, and relevant logs | Legal and IT | Before any account is disabled |
| Reduce access to sensitive data quietly (role-based) | Identity team | Coordinate with HR so it looks routine |
| Block USB storage and personal cloud for the person or the whole group | Endpoint team | Group-wide changes are less noticeable |
| Disable the account and collect devices at the HR meeting | HR with IT | Usually done at the same moment as the conversation |
| Revoke privileged access immediately if sabotage is possible | Identity team | Do not wait for HR when production is at risk |
| Recover company devices and ask for return or deletion of copied data | HR and legal | Written statement from the person |

## 6. Eradication and recovery

- [ ] Remove accounts, keys, tokens and backdoors the person created; review everything they administered.
- [ ] Rotate shared passwords and service account secrets they knew.
- [ ] Restore any deleted or changed data from backup and check integrity.
- [ ] Review the leaver process: same-day access removal, device return, data handover.
- [ ] Monitor for the person's personal accounts or devices appearing in logs for 90 days.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| SOC manager | Immediately, on any suspicion | Analyst |
| HR and legal | Before any monitoring or containment | SOC manager |
| CISO | All cases | SOC manager |
| Privacy officer | When personal data of others was taken, or monitoring of personal data is proposed | Legal |
| The person's manager | Only if HR decides | HR |
| Law enforcement | Only if legal decides | Legal |

Never discuss the case in shared channels, general tickets or team chats.

## 8. Evidence to keep

- Approval record from HR and legal with the scope and date.
- Original log exports, hashed, with chain of custody for each item.
- Forensic images of devices when the case may go to a tribunal or court (use an external forensic firm if possible).
- A factual timeline: times, actions, data, sources; no opinions about the person.

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review, with restricted attendance:

- Did the person have more access than their role required (least privilege)?
- Was there a signal earlier (UEBA, DLP, a manager's concern) that nobody acted on?
- Did the leaver process remove access on the last day?
- Were HR, legal and the SOC able to work together quickly? Is there an agreed insider procedure?

Detections to add or tune: leaver watch list joined with data movement, access outside peer group, USB mass copy, admin self-granting rights, log or backup deletion by an admin.


## Related documents

- Data Exfiltration, Account Compromise
- Evidence Handling
- Escalation and Communication
