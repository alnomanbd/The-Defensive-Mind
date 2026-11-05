---
id: PB-02
title: Business Email Compromise
owner: SOC lead with the finance controller
audience: SOC analyst L1 / L2, finance contacts, incident lead
review: Every 12 months, and after every real incident that used this playbook
summary: "How to respond to business email compromise (BEC): fraud where an attacker uses a real or look-alike email account to trick staff into paying money, changing bank details, or sending sensitive data. BEC causes more direct financial loss than any other cybercrime, and the first hours decide whether the money can be recovered."
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-02 |
| **Default severity** | P2 High; P3 Medium for a failed attempt (see Severity and SLA) |
| **Escalate to Critical when** | Money has been paid, an executive or finance mailbox is compromised, or customers or suppliers were defrauded from your domain |
| **MITRE ATT&CK** | T1566 Phishing, T1078.004 Cloud Accounts, T1114.002 Remote Email Collection, T1114.003 Email Forwarding Rule, T1564.008 Email Hiding Rules, T1534 Internal Spearphishing, T1656 Impersonation, T1583.001 Domains (look-alike) |
| **Typical alerts** | User or finance reports a payment change request, new inbox rule moving mail to RSS Feeds or Archive, external forwarding rule, sign-in from a new country followed by mailbox access, look-alike domain registered, email from the CEO's name with a free webmail address |
| **Owner** | SOC lead with the finance controller |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

BEC has three common forms. **Mailbox takeover**: the attacker logs into a real mailbox (often after phishing), reads ongoing invoice threads, and replies inside them with new bank details. **Supplier compromise**: a supplier's mailbox is taken over and sends you a real-looking invoice change. **Impersonation**: a look-alike domain (`examp1e.com`) or display name trick ("CEO Name" from a Gmail address) asks for an urgent payment or gift cards. Attackers hide their work with inbox rules that move replies out of sight. Success for the defender: payment recall starts within hours, every compromised mailbox is cleaned, and people in the thread are warned.

## 2. Triggers and detection

| Signal | What it means | Log source |
|:---|:---|:---|
| Payment or bank detail change request by email | The classic BEC lure | Finance report, mail |
| Inbox rule with names like `.`, `..`, `rss` or keywords like "invoice", "payment", "bank", moving to RSS Feeds, Archive, Conversation History or deleting | Attacker hiding replies | M365 audit `New-InboxRule`, `Set-InboxRule`; Google Workspace audit |
| External forwarding rule or mailbox forwarding (`ForwardingSmtpAddress`) | Silent copy of all mail | M365 audit `Set-Mailbox`, mail flow |
| `MailItemsAccessed` from an unfamiliar IP or app | Attacker reading mail | M365 audit (requires audit logging that includes it) |
| Sign-in risk then mailbox activity | Account takeover | Entra ID or Google sign-in logs |
| Look-alike domain registered or emails from it | Impersonation | Domain monitoring, mail gateway |
| Reply-to differs from From | Impersonation trick | Mail gateway headers |

**Common false positives:** users creating their own tidy-up rules, a real supplier changing banks (verify by phone), assistants managing executives' mailboxes, approved forwarding to a partner system.

## 3. Triage (first 15 to 30 minutes)

- [ ] **Has money been paid?** If yes, call finance now to start the bank recall (see section 5). Do this before anything else.
- [ ] Get the suspicious email as an attachment (`.eml` or `.msg`) with full headers.
- [ ] Is the sender our own mailbox, a supplier's real domain, or a look-alike domain?
- [ ] If our own mailbox: any recent risky sign-in, new MFA method, new inbox rule or forwarding?
- [ ] If a supplier's domain: call the supplier on a known phone number (from the contract, not the email).
- [ ] Who else received emails from the attacker in this thread or campaign?

Decision: failed attempt from a look-alike domain with no payment, P3, block domain and warn finance; our mailbox compromised, P2, run section 5 and Account Compromise; money paid, P1 if large or executive involved, start recall at once.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Is our mailbox compromised? | Sign-in logs for the user (new IP, country, device, legacy protocols), MFA changes, inbox rules |
| Which rules and forwarding exist? | `Get-InboxRule -Mailbox user`, `Get-Mailbox user` forwarding fields; Workspace audit |
| What did the attacker read? | `MailItemsAccessed`, `SearchQueryInitiated` events (searches for "invoice", "payment", "wire") |
| What did the attacker send? | Message trace for the attacker's session time window; Sent Items, Deleted Items |
| Who received fraudulent emails? | Message trace by subject, sender and attacker IP; look for internal phishing too |
| How did they get in? | Earlier phishing to the user (Phishing), infostealer (Malware), password spraying (Brute Force), AiTM token theft |
| Is a look-alike domain involved? | WHOIS, registration date, MX records; search mail logs for that domain across all users |

### Queries: suspicious inbox rules and forwarding

**Microsoft Sentinel KQL**


```kql
OfficeActivity
| where TimeGenerated > ago(30d)
| where Operation in ("New-InboxRule","Set-InboxRule","UpdateInboxRules","Set-Mailbox")
| extend P = tostring(Parameters)
| where P has_any ("ForwardTo","RedirectTo","ForwardingSmtpAddress","DeleteMessage","MoveToFolder","RSS","Archive","Conversation History")
   or P has_any ("invoice","payment","bank","wire","remittance")
| project TimeGenerated, UserId, ClientIP, Operation, P
```

**Splunk SPL**


```spl
index=o365 Workload=Exchange Operation IN ("New-InboxRule","Set-InboxRule","UpdateInboxRules","Set-Mailbox")
  ("ForwardTo" OR "RedirectTo" OR "ForwardingSmtpAddress" OR "DeleteMessage" OR "RSS" OR "invoice" OR "payment" OR "bank")
| table _time UserId ClientIP Operation Parameters{}.Name Parameters{}.Value
```

**Elastic**


```text
event.dataset : "o365.audit" and event.action : ("New-InboxRule" or "Set-InboxRule" or "Set-Mailbox")
  and o365.audit.Parameters.Name : ("ForwardTo" or "RedirectTo" or "ForwardingSmtpAddress" or "DeleteMessage" or "MoveToFolder")
```

**IBM QRadar AQL**


```sql
SELECT username, sourceip, QIDNAME(qid) AS action, UTF8(payload) AS details, starttime
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%Office 365%'
  AND (QIDNAME(qid) ILIKE '%InboxRule%' OR QIDNAME(qid) ILIKE '%Set-Mailbox%')
LAST 30 DAYS
```

**Wazuh**


```text
data.office365.Operation:(New-InboxRule or Set-InboxRule or UpdateInboxRules or Set-Mailbox)
```

**Exchange Online PowerShell**


```powershell
Connect-ExchangeOnline
Get-InboxRule -Mailbox user@example.com | Select Name, Enabled, From, SubjectOrBodyContainsWords, MoveToFolder, ForwardTo, RedirectTo, DeleteMessage
Get-Mailbox user@example.com | Select ForwardingSmtpAddress, ForwardingAddress, DeliverToMailboxAndForward
Get-MessageTrace -SenderAddress user@example.com -StartDate (Get-Date).AddDays(-10) -EndDate (Get-Date)
```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| **Call the bank to recall or freeze the payment**, then file a fraud report | Finance | Recovery chances drop sharply after 24 to 72 hours; in the US also report to IC3 for the Financial Fraud Kill Chain |
| Reset password, revoke all sessions and refresh tokens, review MFA methods | Identity team | Remove any MFA device the user did not add |
| Export, then remove malicious inbox rules and forwarding | Email admin | Export is evidence |
| Block the look-alike domain and attacker addresses at the mail gateway | SOC / Email admin | Also add to the impersonation protection list |
| Purge attacker emails from all mailboxes | Email admin | Search by sender, subject and time |
| Warn the other parties in the thread (customers, suppliers) by phone | Finance or account manager | They may be targeted next with "updated" bank details |
| Disable external auto-forwarding tenant-wide if not needed | Email admin | Strong prevention control |

## 6. Eradication and recovery

- [ ] Remove OAuth apps the attacker may have consented to on the account.
- [ ] Check other mailboxes for the same attacker IP, rules and messages.
- [ ] Enforce phishing-resistant MFA for finance and executives (FIDO2 keys or passkeys).
- [ ] Introduce or confirm the **call-back rule**: every bank detail change is confirmed by phone to a known number, never one from the email.
- [ ] Turn on mail impersonation protection for executives and key suppliers; set DMARC to `p=reject` for your own domains.
- [ ] Monitor the affected mailboxes for 30 days for new rules and sign-ins.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Finance controller | Immediately for any payment request | Analyst |
| SOC lead | Any compromised mailbox or payment | Analyst |
| CISO, legal | Money lost, executive mailbox, or data exposed in the mailbox | SOC lead |
| Affected customers and suppliers | Quickly, by phone; follow with a written note | Finance or account manager, with legal |
| Police and the bank's fraud team | When money was lost | Finance with legal |
| Insurance | When money was lost (crime or cyber policy) | Finance |

Do not email the compromised user about the investigation from their own mailbox. See Escalation and Communication.

## 8. Evidence to keep

- The fraudulent emails as `.eml` with full headers.
- Inbox rule and forwarding exports before removal.
- Sign-in logs and mailbox audit logs for the attacker's session window.
- Payment records, bank correspondence and recall reference numbers.
- Look-alike domain WHOIS and DNS records (screenshots with dates).

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review:

- Did finance follow a call-back rule? If not, why not (time pressure, seniority of the requester)?
- Was MFA in place, and how was it bypassed (push fatigue, AiTM proxy, legacy protocol)?
- How long was the attacker in the mailbox before detection?
- Did DMARC, impersonation protection and external sender tags work?

Detections to add or tune: inbox rules with financial keywords or hidden folders, external forwarding, sign-in from new country followed by rule creation, look-alike domain registrations, display name of an executive from an external address.


## Related documents

- Phishing, Account Compromise, Data Exfiltration
- Tabletop Exercises (scenario: CEO's mailbox forwarding)
- Escalation and Communication
