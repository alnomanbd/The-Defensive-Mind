# Investigation Cheat Sheet

The questions you ask mid-investigation, each with a ready query idea and, where useful, a live-response one-liner. Keep this open while you work a case. Swap the field names for your own SIEM's.

!!! abstract "At a glance"
    - Audience: any analyst, mid-investigation
    - Time to read: use it as a lookup, not a read-through
    - Outcome: a fast answer to "how do I check X?" for the most common questions

!!! note "Field names vary"
    Queries use common fields (`user`, `src_ip`, `host`). Splunk uses SPL, Microsoft Sentinel and Defender use KQL tables, Elastic uses ECS. Keep a one-page mapping from these to your own data.

## Identity and accounts

| Question | Where and how |
|---|---|
| Did this login succeed or fail? | Windows 4624 (success) / 4625 (failure); IdP sign-in result field |
| Where did the user log in from (IPs, countries)? | Sign-in logs grouped by user, last 7 to 30 days |
| Any login after failures (brute-force success)? | 4624 after a run of 4625 for the same user and source |
| New or changed MFA method? | IdP audit log: MFA registration or change events |
| New admin account or privilege grant? | Windows 4720, 4728, 4732, 4756; cloud IAM create or policy events |
| Is this account active or disabled, and whose is it? | Directory lookup; is the user a current employee or a leaver? |
| Impossible travel? | Two sign-ins too far apart in time for the distance |

### Successful logon after failures (Windows)

=== "Microsoft Sentinel KQL"

    ```kql
    SecurityEvent
    | where TimeGenerated > ago(1d) and EventID in (4624, 4625)
    | summarize fails = countif(EventID == 4625), success = countif(EventID == 4624),
        firstFail = minif(TimeGenerated, EventID == 4625), firstSuccess = minif(TimeGenerated, EventID == 4624)
        by Account, IpAddress
    | where fails >= 5 and success > 0 and firstSuccess > firstFail
    ```

=== "Splunk SPL"

    ```spl
    index=wineventlog (EventCode=4624 OR EventCode=4625) earliest=-1d
    | stats count(eval(EventCode=4625)) as fails count(eval(EventCode=4624)) as success
        min(eval(if(EventCode=4625,_time,null))) as firstFail by Account_Name, Source_Network_Address
    | where fails>=5 AND success>0
    ```

## Endpoints and processes

| Question | Where and how |
|---|---|
| What did this process do (children, network, files)? | EDR process tree; Sysmon 1 (process), 3 (network), 11 (file) |
| Where did this file come from? | Browser download history; Zone.Identifier `HostUrl`; mail logs |
| Is this hash known malicious? | Hash lookup (do not upload confidential files) |
| Is the same file on other hosts? | EDR file-event search by hash across the fleet |
| New persistence (autorun, task, service)? | Sysmon 13 (registry), Windows 4698 (task), 7045 (service) |
| What is connecting out, and to where? | EDR network events; Sysmon 3; firewall and proxy by host |

### Live: processes with outbound connections (osquery)

```sql
SELECT p.pid, p.name, p.path, s.remote_address, s.remote_port
FROM processes p JOIN process_open_sockets s USING (pid)
WHERE s.remote_address NOT IN ('', '0.0.0.0', '127.0.0.1', '::');
```

### Live: quick Windows state capture (save to external media)

```bat
tasklist /v > E:\triage\tasklist.txt
netstat -anob > E:\triage\netstat.txt
schtasks /query /fo LIST /v > E:\triage\schtasks.txt
wmic service get name,pathname,startmode,state > E:\triage\services.txt
```

### Live: quick Linux state capture

```bash
ps auxwwf > /mnt/evidence/ps.txt
ss -tupan > /mnt/evidence/ss.txt
last -Faiwx > /mnt/evidence/last.txt
crontab -l > /mnt/evidence/cron_root.txt; ls -la /etc/cron.* >> /mnt/evidence/cron_root.txt
find / -xdev -mtime -7 -type f 2>/dev/null > /mnt/evidence/modified_7d.txt
```

## Network

| Question | Where and how |
|---|---|
| Who talked to this IP, and when? | Firewall, proxy, sign-in logs filtered to the IP; first and last seen |
| Is this domain suspicious? | Age, registrar, reputation; newly registered domains are a flag |
| Unusual outbound volume (exfiltration)? | Per-host bytes-out against that host's baseline |
| DNS tunnelling? | Many long, high-entropy subdomains to one parent domain |
| Beaconing (regular callbacks)? | Connections to one destination at a steady interval |

### Everything that touched one IP across sources

=== "Splunk SPL"

    ```spl
    (index=auth OR index=proxy OR index=firewall OR index=web)
      (src_ip=203.0.113.45 OR dest_ip=203.0.113.45 OR clientip=203.0.113.45) earliest=-7d
    | stats count min(_time) as first max(_time) as last values(user) as users values(host) as hosts by index, sourcetype
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT LOGSOURCENAME(logsourceid) AS source, sourceip, destinationip, username,
      MIN(starttime) AS first_seen, MAX(starttime) AS last_seen, COUNT(*) AS n
    FROM events
    WHERE sourceip = '203.0.113.45' OR destinationip = '203.0.113.45'
    GROUP BY logsourceid, sourceip, destinationip, username LAST 7 DAYS
    ```

## Email

| Question | Where and how |
|---|---|
| Who else got this phishing email? | Message trace by sender, subject, or attacker IP |
| Did the user click or reply? | URL-click logs; sent-items for a reply |
| Any mailbox rule or forwarding change? | M365 audit: New-InboxRule, Set-Mailbox, forwarding fields |
| Was the mailbox accessed from an odd place? | MailItemsAccessed by IP; sign-in logs for the mailbox |

## Cloud

| Question | Where and how |
|---|---|
| What did this key or identity do? | Cloud audit logs filtered to the key or principal, all regions |
| New identity, key, or privilege? | CreateUser, CreateAccessKey, role or policy changes |
| Was logging turned off? | StopLogging, DeleteTrail, diagnostic setting deleted |
| Data accessed or made public? | Storage access logs; bucket or container policy changes |

## Scoping and timeline

| Question | Where and how |
|---|---|
| What happened on this asset around the key event? | Search the asset 30 minutes before and after the event |
| Has this indicator been here before? | Search 30 to 90 days of logs for the IP, domain or hash |
| What is the full timeline? | Build a table: time (UTC), event, source, finding, as you pivot |

!!! tip "Write the pivot down before you make it"
    Before each new search, note in the case what you have and what you expect to find. It keeps the investigation honest and lets the next person follow your reasoning.

## Related pages

- [L1 analyst](l1-analyst.md)
- [L2 analyst](l2-analyst.md)
- [Alert triage](../02-daily-operations/alert-triage.md)
- [Evidence handling](../03-incident-response/evidence-handling.md)
- [Playbooks](../04-playbooks/index.md)
