# A Day as an L2 Analyst / Incident Handler

L2 takes what L1 escalates and answers three questions: how big is it, how do we stop it, and who needs to know. You own the case from escalation to closure.

!!! abstract "At a glance"
    - Audience: L2 analysts, incident handlers, senior L1s preparing to step up
    - Time to read: 30 minutes
    - Outcome: you can accept an escalation, scope it by pivoting, build a timeline, drive containment with the right approvals, and close with lessons

## The day, hour by hour

| Time | What you do | Output |
|---|---|---|
| 08:00 | Handover: open incidents, containment still in place, pending approvals | Handover note acknowledged |
| 08:20 | Review overnight escalations; re-prioritise by impact, not by arrival order | Updated case priorities |
| 08:40 | Check L1 closures from the night (sample 5) for quality | Feedback to L1 in chat or 1:1 |
| 09:00 | Work the top incident: scope -> timeline -> containment decision | Case notes, timeline table |
| 10:30 | Status update to stakeholders on any open High/Critical | Status message (template below) |
| 11:00 | Coordinate with IT / DevOps on approved actions (reset, isolate, rotate) | Change tickets, confirmations |
| 13:00 | New escalations; support L1 with questions ("is this worth escalating?") | Coaching, faster decisions |
| 14:30 | Evidence work: export logs, hashes, screenshots; chain of custody where needed | Evidence folder |
| 15:30 | Close or hand over each case with a clear next step | Closure notes, lessons items |
| 15:50 | Handover to next L2; brief on anything that might wake people up tonight | Handover note |

## Taking an escalation

Within 15 minutes of an L1 escalation (High) or 5 minutes (Critical):

1. **Acknowledge** in the case and the chat: "Taken by m.silva (L2), 09:04 UTC".
2. **Re-read the L1 note.** Re-run one key query yourself, never build on an unverified finding.
3. **Set the severity** using impact, not the rule's default. See [Severity and SLA](../02-daily-operations/severity-and-sla.md).
4. **Open the timeline table** in the case (even with only two rows).
5. **Decide the first question**: "Is the attacker still active right now?" That decides how fast containment must be.

!!! tip "Ask L1 one question back"
    Something like "Did you check activity *after* the success?" teaches more than rewriting their note.

## Scoping: pivot by user, host, IP, hash, time

Start from what you know, find a new indicator, pivot on it, repeat. Write each pivot in the case.

| You have | Pivot to find | Example query idea |
|---|---|---|
| User | Hosts they logged on to, IPs they came from, apps used, mailbox changes | Sign-ins + endpoint logons for the user, ±48 h |
| Host | Users on it, processes, outbound connections, new files, persistence | EDR timeline for the host |
| IP | Every user and host that talked to it, first/last seen | Proxy, firewall, sign-in logs for the IP |
| Hash | Every host with that file, where it came from | EDR file events by hash |
| Domain / URL | Who resolved or visited it, emails containing it | DNS, proxy, email logs |
| Time window | Everything on the asset 30 min before and after the key event | "Around this time" search |

### Pivot: all activity for an IP across sources

```spl
(index=auth OR index=proxy OR index=firewall OR index=web) (src_ip=203.0.113.45 OR dest_ip=203.0.113.45 OR clientip=203.0.113.45) earliest=-7d
| stats count min(_time) as first max(_time) as last values(user) as users values(host) as hosts by index, sourcetype
| convert ctime(first) ctime(last)
```

```kql
let ip = "203.0.113.45";
union
  (SigninLogs | where IPAddress == ip | project TimeGenerated, Source="SignIn", Who=UserPrincipalName),
  (DeviceNetworkEvents | where RemoteIP == ip | project TimeGenerated, Source="Endpoint", Who=DeviceName),
  (CommonSecurityLog | where SourceIP == ip or DestinationIP == ip | project TimeGenerated, Source="Firewall", Who=DeviceName)
| summarize First=min(TimeGenerated), Last=max(TimeGenerated), Count=count(), Who=make_set(Who, 50) by Source
```

```text
Elastic (KQL syntax in Discover):  source.ip:"203.0.113.45" or destination.ip:"203.0.113.45"
```

### Pivot: what happened on a host around a time

```spl
index=edr host="LAPTOP-0231" earliest="10/27/2026:09:10:00" latest="10/27/2026:09:50:00"
| table _time event_type user parent_process_name process_name process_cmdline dest_ip file_path
| sort _time
```

```kql
let t = datetime(2026-10-27 09:30:00);
union DeviceProcessEvents, DeviceNetworkEvents, DeviceFileEvents, DeviceRegistryEvents
| where DeviceName == "laptop-0231" and Timestamp between ((t - 20m) .. (t + 20m))
| project Timestamp, ActionType, InitiatingProcessFileName, FileName, ProcessCommandLine, RemoteIP, RemoteUrl, FolderPath
| order by Timestamp asc
```

## Building the timeline

Keep one table in the case. Times in UTC. Each row has a source, so anyone can verify it.

| Time (UTC) | Event | Source | Confidence |
|---|---|---|---|
| 07:02 | Phishing email delivered to 14 users | Email gateway | Confirmed |
| 07:15 | a.khan clicks link | URL click log | Confirmed |
| 07:16 | Credentials posted to fake login page | Proxy (POST to phishing domain) | Likely |
| 07:31 | Sign-in from 203.0.113.45, MFA approved by push | Identity provider | Confirmed |
| 07:34 | Inbox rule "RSS" created moving mail with "invoice" | Mailbox audit | Confirmed |

!!! note "Confidence column"
    "Confirmed" = seen in a log. "Likely" = strongly implied. "Assumed" = gap you still need to fill. Reviewers love this column; it stops guesses becoming facts.

## Containment decisions and approvals

Decide using impact of the action vs risk of waiting. Pre-approved actions are written in the playbook; everything else needs a named approver.

| Action | Typical approval | Speed | Side effect |
|---|---|---|---|
| Revoke user sessions / tokens | Pre-approved for SOC | Minutes | User signs in again |
| Force password reset | Pre-approved for SOC (standard users) | Minutes | User locked out until reset |
| Disable account | SOC lead; for executives also their office / HR | Minutes | User cannot work |
| Isolate endpoint via EDR | Pre-approved for workstations; servers need system owner | Minutes | Host offline (except EDR channel) |
| Block IP/domain at firewall/proxy | SOC lead | Minutes-hours | Possible business impact if shared IP |
| Rotate cloud keys / secrets | Service owner + DevOps | Hours | App outage if not coordinated |
| Take a production server offline | Incident manager + business owner | Hours | Revenue / service impact |

Record each approval like this:

```text
11:05 UTC Approval: Isolate LAPTOP-0231 via EDR. Approved by R. Ortiz (SOC lead) in chat #ir-2026-10412. Executed 11:07 by m.silva. Verified 11:08 (EDR status: isolated).
```

!!! warning "Before you contain"
    Collect volatile evidence you will lose (running processes, network connections, memory if needed) **if** time allows. If the attacker is actively moving or encrypting, contain first and document why.

## Working with IT and DevOps

- Give them **one clear ask per message**: what, which asset, by when, how to verify.
- Never paste secrets into tickets. Say "rotate the key ending `...7QXA`".
- Agree a verification step ("send me the new key's creation time from the console").
- Thank them in the case, you will need them again tonight.

!!! example "Request to IT"
    ```text
    Hi Service Desk - SOC incident IR-2026-10412 (High).
    Please reset password and revoke all sessions for a.khan@example.com now.
    Do NOT contact the user by email (mailbox may be compromised); call +x-xxx on file.
    Reply here with the reset time. Questions: m.silva, SOC L2, ext 4410.
    ```

## Communicating status

Cadence: Critical every 1 hour, High every 4 hours or at each milestone, Medium daily.

!!! example "Status update"
    ```text
    IR-2026-10412 | HIGH | Status 10:30 UTC | Owner: m.silva
    What happened: 1 user's credentials phished; attacker signed in and created a mail rule.
    Impact so far: 1 mailbox; no evidence of other accounts or data sent out.
    Done: sessions revoked, password reset, rule removed, phishing email purged (14 mailboxes).
    Next: check 13 other recipients for clicks (by 12:00); block phishing domain (pending approval).
    Asks: none. Next update 14:30 UTC.
    ```

## Closing with lessons

1. Confirm containment still holds (no new sign-ins, no re-infection) for an agreed period (24-72 h).
2. Fill the root cause: how did they get in, why did detection catch it (or late).
3. Write 1-3 lessons, each with an owner and a ticket: detection gap, process gap, control gap.
4. Close with the [incident report](../09-templates/incident-report.md) for High/Critical.

## Worked mini example

**Escalation (09:02):** L1 reports EDR alert "Credential dumping tool" on server `APP-SRV-07`, action *detected only*.

| Step | What L2 did | Finding |
|---|---|---|
| 09:04 | Acknowledged, re-ran EDR query | Process `procdump64.exe -ma lsass.exe` run by `svc_backup` at 08:51 |
| 09:10 | Pivot: user `svc_backup` logons, 7 days | Interactive RDP (Remote Desktop Protocol) logon from `10.30.4.18` at 08:40, service account never logs on interactively |
| 09:15 | Pivot: host `10.30.4.18` | Workstation of contractor; EDR shows `rclone.exe` executed 08:20 |
| 09:20 | Decision: active intrusion, Critical. Paged SOC lead | Lead approves isolation of both hosts |
| 09:24 | Isolated workstation and server (server owner approved by phone) | EDR confirms isolation |
| 09:30 | Disabled `svc_backup`, reset its password via IT | Backup jobs paused, accepted by owner |
| 10:30 | Status update; L3 asked to analyse the dump file and rclone config | Rclone config points to external storage; no upload seen yet in proxy logs |
| Day 2 | Root cause: contractor laptop infected via cracked software | Lessons: block interactive logon for service accounts; alert on rclone |

## Common mistakes

!!! danger "L2 pitfalls"
    - Containing one host and declaring victory without scoping the rest.
    - Resetting the password but not revoking sessions / tokens (attacker stays signed in).
    - Taking a server down without the owner's approval, you become the incident.
    - Status updates full of jargon; managers need impact, actions, next update time.
    - Closing without lessons, so the same alert comes back next month.

## L2 checklist

- [ ] Escalation acknowledged within SLA; severity re-assessed on impact
- [ ] Key L1 finding re-verified
- [ ] Pivots done: user, host, IP, hash/domain, ±time window
- [ ] Timeline table up to date with source and confidence
- [ ] Every containment action has approver, time, executor, verification
- [ ] Status updates sent on cadence
- [ ] Evidence saved (exports, hashes, screenshots)
- [ ] Lessons logged with owners; report filed for High/Critical

## Related pages

- [L1 analyst](l1-analyst.md), [L3 analyst](l3-analyst.md)
- [Investigation cheat sheet](investigation-cheatsheet.md)
- [Account compromise playbook](../04-playbooks/account-compromise.md)
- [Ransomware playbook](../04-playbooks/ransomware.md)
- [Data exfiltration playbook](../04-playbooks/data-exfiltration.md)
- [Incident report template](../09-templates/incident-report.md)
- [Walkthroughs](walkthroughs/index.md)
