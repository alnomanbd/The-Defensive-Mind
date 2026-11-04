# Playbook: Phishing

Hands-on steps for a reported or detected phishing email: verdict, scope, purge, protect the people who clicked.

!!! abstract "At a glance"
    - Audience: SOC analyst L1/L2/L3, SOC manager
    - Time to read: 10 minutes
    - Outcome: verdict in 30 minutes, every copy purged, every clicker protected

| Field | Value |
|:---|:---|
| **ID** | PB-01 |
| **Default severity** | Medium (see [Severity and SLA](../02-daily-operations/severity-and-sla.md)) |
| **Escalate to Critical when** | Credentials were entered and the account shows new sign-ins, an attachment executed, or a privileged / finance user is affected |
| **MITRE ATT&CK** | T1566.001 Spearphishing Attachment, T1566.002 Spearphishing Link, T1566.003 Spearphishing via Service, T1598 Phishing for Information, T1204.001 Malicious Link, T1204.002 Malicious File |
| **Typical alerts** | User "Report phish" button, secure email gateway (SEG) retro-verdict, URL click protection hit, EDR: Office app spawns a script host |
| **Owner** | SOC manager |
| **Last reviewed** | 2026-10-27 |

## 1. Summary

A malicious email tries to steal credentials or run code. Find every recipient, find every click, purge all copies and protect anyone who interacted. Speed of purge is the metric.

## 2. Triggers and detection

- User report, SEG / sandbox verdict after delivery, click protection hit, Endpoint Detection and Response (EDR) alert on `winword.exe` / `excel.exe` / `outlook.exe` spawning `powershell.exe`, `mshta.exe`, `wscript.exe`, `rundll32.exe`.
- **True positive:** look-alike or new domain, `Reply-To` differs from `From`, SPF/DKIM/DMARC fail, urgency, credential page on a free host, HTML/ISO/ZIP/LNK attachment.
- **False positives:** awareness simulation (check the simulation sender list), newsletters, real e-signature / file-share notifications from a verified partner tenant.

## 3. Triage (first 15-30 minutes)

| Role | Responsibility |
|:---|:---|
| **L1** | Get the `.eml`, check headers, extract indicators, run mail trace and click search, answer the reporter, escalate on any click or execution |
| **L2/L3** | Sandbox analysis, credential-submission check, purge, account / endpoint containment, hunt for variants |
| **Manager** | Approve all-staff warning, inform CISO / finance, watch the SLA, decide on legal involvement |

- [ ] Ask for the message **as an attachment** (`.eml` / `.msg`); forwards lose headers.
- [ ] Simulation? Yes -> thank reporter, close "simulation".
- [ ] Headers: `Return-Path`, `From`, `Reply-To`, `Authentication-Results`, first external `Received` hop.
- [ ] Extract sender, sending IP, subject, URLs, attachment names and SHA-256.
- [ ] Reputation check in a sandbox / TI source (e.g. CAPE, urlscan.io, VirusTotal). Never open links on your workstation.
- [ ] Mail trace: how many recipients? Click / proxy / DNS: who visited? EDR: who opened the attachment?

```bash
grep -iE '^(from|reply-to|return-path|authentication-results|received|subject):' message.eml
sha256sum invoice_2026.zip
```

Decision: malicious, no interaction -> Medium, purge + block, click or credential entry -> High, run [Account Compromise](account-compromise.md), attachment executed -> High/Critical, run [Malware / Infostealer](malware-infostealer.md), benign -> close with reason, unsure -> L2.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Who received it? | Mail trace by sender, subject, URL domain, attachment hash, last 7 days |
| Who clicked? | Click protection, proxy, DNS logs for the phishing domain after delivery time |
| Who entered credentials? | Proxy `POST` to the phishing host; IdP sign-ins for clickers within 24 h |
| Did the attachment run? | EDR process tree for the hash / filename |
| Did the attacker use the credentials? | IdP: new IP / country / device, MFA changes, inbox rules, OAuth consent |
| Internal sender? | Treat as [Account Compromise](account-compromise.md) + [BEC](business-email-compromise.md) |

### Hunting queries

Recipients (Microsoft KQL, Defender / Sentinel):

```kql
EmailEvents
| where Timestamp > ago(7d)
| where SenderFromDomain == "examp1e.com" or Subject has "Invoice overdue"
| summarize Recipients = dcount(RecipientEmailAddress),
            Delivered = countif(DeliveryAction == "Delivered") by SenderFromAddress, Subject
```

Clickers and credential posts (Splunk SPL):

```spl
index=proxy url="*login-examp1e.com*" earliest=-7d
| stats min(_time) as first_seen values(http_method) as methods count by user src_ip
| eval cred_submitted=if(mvfind(methods,"POST")>=0,"yes","no")
| convert ctime(first_seen)
```

Same in Elastic / OpenSearch (ES|QL):

```sql
FROM logs-proxy*
| WHERE url.domain == "login-examp1e.com" AND @timestamp > NOW() - 7 days
| STATS first_seen = MIN(@timestamp), methods = VALUES(http.request.method) BY user.name, source.ip
```

Office spawning script hosts (KQL):

```kql
DeviceProcessEvents
| where Timestamp > ago(7d)
| where InitiatingProcessFileName in~ ("winword.exe","excel.exe","outlook.exe","onenote.exe")
| where FileName in~ ("powershell.exe","mshta.exe","wscript.exe","cscript.exe","rundll32.exe")
| project Timestamp, DeviceName, AccountName, InitiatingProcessFileName, ProcessCommandLine
```

### Worked example

Headers from the reported mail:

```text
From: "Accounts Payable" <billing@examp1e.com>
Reply-To: ap-team@freemail.example.net
Return-Path: <bounce@mailer.example.org>
Authentication-Results: spf=fail smtp.mailfrom=mailer.example.org; dkim=none; dmarc=fail header.from=examp1e.com
Received: from mailer.example.org (203.0.113.45)
Subject: Invoice overdue - action required today
```

Proxy log 12 minutes later:

```text
2026-10-27T09:14:02Z user=jdoe src=10.20.4.17 GET  https://login-examp1e.com/sso?u=jdoe 200
2026-10-27T09:14:31Z user=jdoe src=10.20.4.17 POST https://login-examp1e.com/sso/submit 302
```

Reading: look-alike domain, DMARC fail, `Reply-To` to free mail, and a `POST` = jdoe typed a password. Severity -> High; reset + revoke jdoe now, purge 46 copies, check IdP for sign-ins from new IPs after 09:14.

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Purge all copies (soft delete first) | L2 / Messaging | Keep one copy in the case |
| Block sender, domain, sending IP on SEG | L1/L2 | Never block a whole public webmail domain |
| Block URL / domain on proxy, DNS, click protection | L2 / Network | Check it is not a shared legitimate host |
| Block attachment hash on EDR and SEG | L2 | Low risk |
| Reset password + revoke sessions for credential submitters | Identity team | See [PB-02](account-compromise.md) |
| Isolate endpoints that executed the payload | L2 / Desktop | Tell the user |
| Remove malicious inbox rules / OAuth consents | Messaging / Identity | Export before deleting |

### Example commands

Microsoft 365 (Purview / Exchange Online PowerShell):

```powershell
New-ComplianceSearch -Name "PB01-20261027" -ExchangeLocation All `
  -ContentMatchQuery 'from:"billing@examp1e.com" AND subject:"Invoice overdue"'
Start-ComplianceSearch -Identity "PB01-20261027"
New-ComplianceSearchAction -SearchName "PB01-20261027" -Purge -PurgeType SoftDelete
New-TenantAllowBlockListItems -ListType Sender -Block -Entries "billing@examp1e.com"
```

Google Workspace: Security investigation tool -> Gmail messages -> filter by sender -> "Delete messages". Open-source mail stacks: remove from mailboxes with the server's admin tool (e.g. `doveadm expunge -A mailbox INBOX header Subject "Invoice overdue"`).

## 6. Eradication and recovery

- [ ] Re-run the search for variants (new subject / URL); purge again.
- [ ] Re-image or clean any host that executed the payload.
- [ ] Confirm clickers have new passwords, fresh MFA, no unknown devices or apps.
- [ ] Add indicators to the TI platform with a 90-day expiry.
- [ ] Watch 14 days: mail from the same infrastructure, sign-ins from attacker IPs.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Reporter | Verdict within SLA | L1 |
| Clickers | Immediately, phone / chat (not email) | L2 / IT |
| All staff | Campaign is wide or still arriving | Manager + Communications |
| CISO | High / Critical | Manager |
| Finance | Invoice / payment lure | Manager |

See [Escalation and Communication](../03-incident-response/escalation-and-communication.md). Never blame the clicker.

## 8. Evidence to keep

- Original `.eml` + SHA-256, header notes, indicator list.
- Sandbox reports and screenshots (taken in an isolated analysis VM).
- Mail trace export (recipients) and purge job output.
- Proxy / DNS / IdP extracts for clickers.

Follow [Evidence Handling](../03-incident-response/evidence-handling.md).

## 9. Lessons learned

For the [Post-Incident Review](../03-incident-response/post-incident-review.md): time from delivery to report and to purge; why the filter missed it; whether phishing-resistant MFA (FIDO2 / passkeys) would have stopped credential reuse. Add detections: retro-verdict alerting, clicks on newly registered domains, sign-in from a new IP shortly after a click.

## Related pages

- [Account Compromise](account-compromise.md), [Business Email Compromise](business-email-compromise.md), [Malware / Infostealer](malware-infostealer.md)
- [Alert Triage](../02-daily-operations/alert-triage.md), [Employee Security Guide](../08-security-policies/employee-security-guide.md)
- [Sigma rules](../05-detection-engineering/index.md#sigma-rule-library), [Incident Report template](../09-templates/incident-report.md)
