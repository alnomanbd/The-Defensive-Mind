# A Day as an L1 SOC Analyst

The L1 analyst is the first human to look at every alert. Your job: decide fast and correctly whether an alert is benign, a false positive, or something that needs L2, and leave a note anyone can follow.

!!! abstract "At a glance"
    - Audience: L1 (tier 1) SOC analysts, new joiners, interns
    - Time to read: 35 minutes
    - Outcome: you can run a shift, triage the 10 most common alerts with real queries, write a triage note and an escalation, and plan your first 90 days

## The shift, hour by hour

Example: a 08:00-16:00 day shift in a 24x7 SOC. Adjust times to your rota.

| Time | What you do | Tool / output |
|---|---|---|
| 07:50 | Log in, check VPN (Virtual Private Network), SIEM, EDR (Endpoint Detection and Response), ticketing and chat all work | Login check, report broken tools *now*, not at 10:00 |
| 08:00 | Handover with the night shift: open cases, anything "watch for", any outages | [Shift handover](../09-templates/shift-handover-template.md) |
| 08:15 | Read the handover note again; acknowledge each open item in the ticket | Ticket comment "Taken over by j.doe 08:15 UTC" |
| 08:20 | Health check: are all log sources reporting? (see query below) | SIEM dashboard / query |
| 08:30 | Work the queue: oldest Critical/High first, then by age | Queue view sorted by severity, then created time |
| 10:30 | Short break. Never leave a Critical untouched for the break: hand it over in chat | Team chat |
| 10:45 | Queue. Check threat-intel feed / team channel for new advisories | TI (Threat Intelligence) platform, vendor bulletins |
| 12:30 | Lunch (staggered: at least one analyst always on the queue) | Rota |
| 13:15 | Queue. Re-check cases waiting on users ("pending reply") | Ticket filter "pending > 4 h" |
| 14:30 | Learning block (30 min) if the queue is under control: a lab, a playbook, a case review | [Walkthroughs](walkthroughs/index.md) |
| 15:00 | Queue. Chase your escalations: has L2 picked them up? | Ticket view "escalated by me" |
| 15:30 | Write the handover: open cases, status, next step, anything odd | Handover template |
| 15:50 | Verbal handover to the next shift; answer questions | Call / chat |
| 16:00 | Log off only after the next analyst confirms they have it |, |

### Log source health query (08:20)

```spl
| tstats latest(_time) as last_seen where index=* by index, sourcetype
| eval minutes_silent = round((now() - last_seen)/60, 0)
| where minutes_silent > 60
| sort - minutes_silent
```

```kql
union withsource=TableName *
| where TimeGenerated > ago(24h)
| summarize LastSeen = max(TimeGenerated) by TableName
| extend MinutesSilent = datetime_diff('minute', now(), LastSeen)
| where MinutesSilent > 60
| order by MinutesSilent desc
```

!!! warning "A silent log source is an alert"
    If the firewall or the domain controllers stopped sending logs at 02:00, every "no alerts overnight" statement is false. Raise a ticket for the platform team and tell your lead.

## Working the queue

1. **Sort**: severity first (Critical -> High -> Medium -> Low), then oldest first. See [Severity and SLA](../02-daily-operations/severity-and-sla.md).
2. **Assign to yourself** before you start, so nobody duplicates work.
3. **Time-box**: aim for 10-15 minutes per alert. At 20 minutes with no answer, escalate or ask a colleague.
4. **Group duplicates**: 40 alerts for the same host and same rule are one case. Link them, work one.
5. **Close with a note** every time. "FP" alone is not a note.

| Severity | Typical SLA to start triage | Typical SLA to decide (close / escalate) |
|---|---|---|
| Critical | 15 min | 30 min |
| High | 30 min | 2 h |
| Medium | 4 h | 8 h |
| Low | 24 h | 3 days |

## Triage of the 10 most common alerts

For each: what it means, the checks (with query), and the close/escalate rule. Field names are examples.

### 1. Multiple failed logins (possible brute force)

**Means:** many failed authentications for one account or from one source IP in a short window.

**Checks**

1. How many failures, how many accounts, over how long?
2. Any success from the same source after the failures? (most important)
3. Is the source internal (misconfigured service) or external? Reputation?
4. Is the account real, enabled, privileged?

```spl
index=auth (action=failure OR action=success) src_ip=203.0.113.45 earliest=-24h
| stats count(eval(action="failure")) as fails count(eval(action="success")) as success dc(user) as users values(user) as user_list by src_ip
```

```kql
SigninLogs
| where TimeGenerated > ago(24h) and IPAddress == "203.0.113.45"
| summarize Fails = countif(ResultType != "0"), Success = countif(ResultType == "0"), Users = dcount(UserPrincipalName), UserList = make_set(UserPrincipalName, 20) by IPAddress
```

```text
Wazuh: rule.groups:authentication_failed AND data.srcip:203.0.113.45   (then same filter with authentication_success)
```

**Rule:** failures only, external IP, no success, no privileged account -> close as "blocked attempt", consider IP block per policy. **Any success after failures -> escalate High.** Internal source with a service account -> contact owner, close as misconfiguration. See [Brute force playbook](../04-playbooks/brute-force.md).

### 2. Login from unusual country / impossible travel

**Means:** user signed in from a location far from the previous one in too short a time.

**Checks**

1. Both sign-ins: IP, country, device, app, MFA (Multi-Factor Authentication) result.
2. Is one IP a known VPN / corporate egress / mobile carrier?
3. Did the user travel? (HR travel calendar, manager, user, via a known phone number, not email.)
4. What happened after the suspicious login (mailbox rules, downloads, MFA change)?

```spl
index=auth user="j.doe@example.com" action=success earliest=-48h
| iplocation src_ip
| table _time user src_ip Country City app mfa_result user_agent
| sort _time
```

```kql
SigninLogs
| where TimeGenerated > ago(48h) and UserPrincipalName == "j.doe@example.com" and ResultType == "0"
| project TimeGenerated, IPAddress, Location = tostring(LocationDetails.countryOrRegion), AppDisplayName, AuthenticationRequirement, MfaDetail, UserAgent
| order by TimeGenerated asc
```

**Rule:** explained by VPN / travel and same device -> close with the evidence. Unknown device + new country + no explanation -> escalate High. See [Account compromise](../04-playbooks/account-compromise.md).

### 3. User reported phishing

**Means:** a user clicked "report phish" or forwarded an email.

**Checks**

1. Headers: sender, Return-Path, SPF/DKIM/DMARC (Sender Policy Framework / DomainKeys Identified Mail / Domain-based Message Authentication, Reporting and Conformance) results.
2. URLs and attachments: reputation, sandbox detonation (do not open on your workstation).
3. How many users received it? Who clicked?
4. Did anyone enter credentials (sign-in from new IP right after the click)?

```spl
index=email subject="Invoice overdue*" earliest=-7d
| stats count dc(recipient) as recipients values(recipient) as who by sender, subject
```

```kql
EmailEvents
| where Timestamp > ago(7d) and Subject startswith "Invoice overdue"
| summarize Recipients = dcount(RecipientEmailAddress), Who = make_set(RecipientEmailAddress, 50) by SenderFromAddress, Subject
```

```kql
UrlClickEvents
| where Timestamp > ago(7d) and Url has "login-example-support.com"
| project Timestamp, AccountUpn, Url, ActionType, IsClickedThrough
```

**Rule:** marketing / simulation / clean -> close, reply to the user with thanks. Malicious, nobody clicked -> purge from mailboxes, block sender/URL, close. **Anyone clicked and entered credentials, or opened an attachment -> escalate High.** See [Phishing playbook](../04-playbooks/phishing.md).

### 4. Malware detected by EDR / antivirus

**Means:** endpoint agent detected (and maybe blocked) a malicious file or behaviour.

**Checks**

1. Action taken: blocked / quarantined / **detected only**?
2. File hash, path, parent process, how it arrived (download, USB, email).
3. Hash reputation (multi-engine scanner, internal allow-list).
4. Same hash on other hosts?

```spl
index=edr file_hash="d41d8cd98f00b204e9800998ecf8427e" earliest=-30d
| stats count values(host) as hosts values(action) as actions min(_time) as first max(_time) as last by file_name
```

```kql
DeviceFileEvents
| where Timestamp > ago(30d) and SHA256 == "<sha256>"
| summarize Hosts = make_set(DeviceName), First = min(Timestamp), Last = max(Timestamp) by FileName, FolderPath
```

**Rule:** quarantined, single host, adware/PUP (Potentially Unwanted Program) -> close, note. **Detected-only, ran successfully, credential stealer, remote-access tool, or more than one host -> escalate High.** See [Infostealer playbook](../04-playbooks/malware-infostealer.md).

### 5. Suspicious PowerShell / encoded command

**Means:** PowerShell started with `-enc`, `-nop -w hidden`, download cradles, or unusual parent.

**Checks**

1. Decode the command (Base64 -> UTF-16LE). What does it do?
2. Parent process: Office, browser, script host? Or an admin tool?
3. User and host: admin running a known script?
4. Network connections right after?

```bash
# decode on your analysis VM, never execute
echo 'SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkA' | base64 -d | iconv -f UTF-16LE -t UTF-8
# -> IEX (New-Object Net.WebClient)
```

```spl
index=edr process_name=powershell.exe (process_cmdline="*-enc*" OR process_cmdline="*-EncodedCommand*") earliest=-24h
| table _time host user parent_process_name process_cmdline
```

```kql
DeviceProcessEvents
| where Timestamp > ago(24h) and FileName =~ "powershell.exe"
| where ProcessCommandLine has_any ("-enc", "-EncodedCommand", "FromBase64String")
| project Timestamp, DeviceName, AccountName, InitiatingProcessFileName, ProcessCommandLine
```

**Rule:** known management tool (documented, same hash, same parent every day) -> close, ask for tuning. **Parent is Office/browser, or decoded content downloads/executes -> escalate High.**

### 6. New local / domain admin account or group change

**Means:** someone was added to a privileged group (Windows Event ID 4728/4732/4756) or an account was created (4720).

```spl
index=wineventlog EventCode IN (4720,4728,4732,4756) earliest=-24h
| table _time host EventCode SubjectUserName TargetUserName MemberName Group_Name
```

```kql
SecurityEvent
| where TimeGenerated > ago(24h) and EventID in (4720, 4728, 4732, 4756)
| project TimeGenerated, Computer, EventID, SubjectAccount, TargetAccount, MemberName, TargetUserName
```

**Checks:** who made the change, is there a change ticket, is the actor an admin, at what hour. **Rule:** matching approved change -> close with ticket number. No ticket, odd hour, or actor is not in the admin team -> escalate High, do not wait.

### 7. Outbound connection to known-bad IP / domain (TI match)

**Checks:** age and confidence of the indicator; is it a shared hosting / CDN (Content Delivery Network) IP; bytes sent; process that made the connection; how many hosts.

```spl
index=proxy dest_domain="bad-cdn-example.net" earliest=-7d
| stats count sum(bytes_out) as bytes_out dc(src_ip) as hosts values(user) as users by dest_domain, http_user_agent
```

```kql
DeviceNetworkEvents
| where Timestamp > ago(7d) and RemoteUrl has "bad-cdn-example.net"
| summarize Count = count(), Hosts = dcount(DeviceName), Procs = make_set(InitiatingProcessFileName) by RemoteUrl
```

**Rule:** stale indicator on a CDN IP, browser traffic only, blocked by proxy -> close, flag indicator for review. Non-browser process, repeated beaconing, or blocked=false with data out -> escalate.

### 8. Web application attack (WAF / IDS)

**Checks:** was the request blocked; HTTP status returned (200 vs 403/404); single scanner or targeted; did it hit a real path.

```spl
index=web src_ip=198.51.100.23 earliest=-24h
| stats count by status, uri_path
| sort - count
```

```kql
AzureDiagnostics
| where TimeGenerated > ago(24h) and clientIp_s == "198.51.100.23"
| summarize count() by httpStatus_d, requestUri_s
```

**Rule:** blocked or 404s from a known scanner -> close (block IP per policy). **HTTP 200 on a sensitive path (`/.env`, `/backup.zip`, admin panel) -> escalate High.** See [Web application attack](../04-playbooks/web-application-attack.md) and [Case 04](walkthroughs/case-04-web-secret-file-probing.md).

### 9. Data upload / large outbound transfer

**Checks:** user, destination (sanctioned cloud vs personal), volume vs user's 30-day baseline, file names, is the user leaving (HR flag).

```spl
index=proxy user="j.doe" earliest=-30d
| bin _time span=1d
| stats sum(bytes_out) as out by _time
| eventstats avg(out) as avg stdev(out) as sd
| eval z = round((out-avg)/sd, 1)
| where z > 3
```

```kql
DeviceNetworkEvents
| where Timestamp > ago(30d) and InitiatingProcessAccountName == "j.doe"
| summarize SentBytes = sum(tolong(AdditionalFields.bytes_sent)) by bin(Timestamp, 1d)
| order by Timestamp asc
```

**Rule:** sanctioned destination, business explanation from manager -> close. Personal storage, leaver, or sensitive file names -> escalate (quietly, see [Insider threat](../04-playbooks/insider-threat.md)).

### 10. Cloud: console login without MFA / root use / new access key

```spl
index=cloudtrail eventName=ConsoleLogin earliest=-24h
| spath "additionalEventData.MFAUsed" output=mfa
| where mfa="No"
| table _time userIdentity.arn sourceIPAddress mfa responseElements.ConsoleLogin
```

```kql
AWSCloudTrail
| where TimeGenerated > ago(24h) and EventName == "ConsoleLogin"
| extend MFA = tostring(parse_json(AdditionalEventData).MFAUsed)
| where MFA == "No"
| project TimeGenerated, UserIdentityArn, SourceIpAddress, MFA
```

**Checks:** is it root; source IP known; what API calls followed. **Rule:** any root use, or new access key from unknown IP -> escalate High. See [Cloud account compromise](../04-playbooks/cloud-account-compromise.md).

## Writing a triage note

Use the same five headings every time: **What, Checked, Found, Decision, Next.**

!!! example "Filled triage note"
    ```text
    Case: SOC-2026-10412   Rule: Multiple failed logins followed by success
    Analyst: j.doe (L1)    Time worked: 08:41-08:58 UTC

    WHAT
    23 failed sign-ins then 1 success for a.khan@example.com from 203.0.113.45
    between 07:12 and 07:19 UTC.

    CHECKED
    1. SIEM sign-in history 24h for user and IP (query saved in case).
    2. IP reputation: hosting provider, listed on 2 abuse feeds, first seen today.
    3. User normal locations 30d: 10.20.0.0/16 (office) and home ISP, same country.
    4. Activity after success: 07:20 mailbox accessed via legacy IMAP client.
    5. MFA: not required for IMAP (legacy auth).

    FOUND
    Successful password guess from external hosting IP, no MFA challenge,
    mailbox accessed. User not travelling (manager confirmed on phone 08:52).

    DECISION
    True positive - likely account compromise. Escalated to L2 as HIGH at 08:58.

    NEXT
    L2 to decide on password reset + session revoke. Evidence: saved search
    "SOC-2026-10412-signins", IP enrichment screenshot attached.
    ```

## Escalation message

Post in the case **and** ping L2 in the team channel for High/Critical.

!!! example "Escalation message"
    ```text
    @L2-oncall ESCALATION HIGH - SOC-2026-10412
    Likely account compromise: a.khan@example.com
    - 23 fails + 1 success from 203.0.113.45 (hosting, abuse-listed) 07:12-07:19 UTC
    - No MFA (legacy IMAP), mailbox read at 07:20
    - User not travelling (manager confirmed)
    Not yet done: no containment, no contact with user.
    Ask: decide reset/revoke. Full note + queries in the ticket.
    ```

## What NOT to do

!!! danger "Common L1 mistakes"
    - Closing as "FP" without a note, or with "looks fine".
    - Opening a suspicious attachment or URL on your own workstation. Use a sandbox.
    - Emailing a user who might be compromised ("did you log in?"), the attacker reads the mailbox. Phone them on a known number.
    - Blocking, disabling or wiping anything without the approval your runbook requires.
    - Searching only the last 1 hour. Always widen to 24 h, then 7 days.
    - Trusting one source: one log says "blocked", another shows the request succeeded.
    - Sitting on an alert for an hour because you are not sure. Ask at 20 minutes.
    - Copying sensitive data (passwords, customer data) into chat or tickets in clear text.

## Daily checklist

- [ ] All tools work (SIEM, EDR, ticketing, chat, sandbox)
- [ ] Handover read, every open item acknowledged
- [ ] Log source health checked; gaps reported
- [ ] No Critical/High older than its SLA in my queue
- [ ] Every closed alert has a five-part note
- [ ] Every escalation acknowledged by L2
- [ ] Tuning ideas logged (rule, reason, example alert)
- [ ] Handover written and verbally confirmed

## Skills to build in your first 90 days

| Days | Focus | Proof you have it |
|---|---|---|
| 1-30 | Tools and data: log in, find any event by user/host/IP; know your top 10 rules; Windows event IDs 4624/4625/4688/4720/4728; email headers | Triage 10 alerts with a senior shadowing, notes accepted without changes |
| 31-60 | Speed and judgement: 15-min triage, decode Base64, read a process tree, use sandbox and reputation tools; know the playbooks for phishing, brute force, malware | Work a full shift alone; zero missed SLAs for a week |
| 61-90 | Depth: write SPL *and* KQL from scratch; Linux auth logs; cloud audit logs; one walkthrough per week; suggest one tuning change with evidence | Lead one escalation end to end with L2; present one case review to the team |

## Related pages

- [Investigation cheat sheet](investigation-cheatsheet.md)
- [Alert triage](../02-daily-operations/alert-triage.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Shift handover template](../09-templates/shift-handover-template.md)
- [L2 analyst](l2-analyst.md)
- [Walkthroughs](walkthroughs/index.md)
- [Phishing playbook](../04-playbooks/phishing.md), [Brute force playbook](../04-playbooks/brute-force.md)
