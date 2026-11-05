# Playbook: Data Exfiltration

How to respond when data may be leaving the organisation without permission: large uploads, transfers to personal cloud storage, unusual database exports, or data sent over DNS or other hidden channels.

!!! abstract "At a glance"
    - Audience: SOC analyst L2, incident lead, privacy and legal contacts
    - Time to read: 12 minutes
    - Outcome: confirm whether data really left, find out what data and how much, stop the channel, and give legal the facts they need for notification decisions

| Field | Value |
|:---|:---|
| **ID** | PB-13 |
| **Default severity** | P2 High (see [Severity and SLA](../02-daily-operations/severity-and-sla.md)) |
| **Escalate to Critical when** | Personal, payment, health or other regulated data left; exfiltration is still running; the volume is large; or it is part of a ransomware or extortion attack |
| **MITRE ATT&CK** | T1567.002 Exfiltration to Cloud Storage, T1048 Exfiltration Over Alternative Protocol, T1041 Exfiltration Over C2 Channel, T1071.004 DNS, T1560 Archive Collected Data, T1074 Data Staged, T1530 Data from Cloud Storage, T1114 Email Collection |
| **Typical alerts** | DLP policy match, unusual outbound volume from a host, upload to personal cloud storage, rclone or MEGA client, large archive created then transferred, long or high-entropy DNS queries, bulk download from SharePoint, Google Drive or a database, email forwarding to external addresses |
| **Owner** | Incident response lead |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

Exfiltration is the theft of data. It is done by external attackers (often just before ransomware, for double extortion), by insiders taking data to a competitor, or by accident (a user syncing work files to a personal account). Attackers usually **stage** data first (collect and compress it into archives), then send it out over a channel that looks normal: HTTPS to cloud storage, a file transfer tool, or DNS. Success for the defender: the channel is closed fast, the exact data and volume are known, and legal can decide on notification with facts, not guesses.

## 2. Triggers and detection

| Signal | Example | Log source |
|:---|:---|:---|
| Volume anomaly | A host sends 10 times its normal daily outbound bytes; uploads at night | Firewall, proxy, NetFlow, EDR network events |
| Cloud storage upload | Personal Google Drive, Dropbox, MEGA, WeTransfer, file.io | Proxy, CASB, DNS |
| Transfer tools | `rclone`, `winscp`, `curl -T`, `scp`, `ftp`, MEGAsync, Restic | EDR, Sysmon 1 |
| Staging | Large `.zip`, `.7z`, `.rar` created in Temp or a share root; `7z a -p` with password | EDR file events, Sysmon 11 |
| DNS tunnelling | Many long subdomains to one domain, high-entropy labels, many TXT queries | DNS server logs, Zeek `dns.log`, Sysmon 22 |
| SaaS bulk download | Hundreds of files downloaded from SharePoint, OneDrive, Google Drive, Box in minutes | M365 Unified Audit Log, Google Workspace audit |
| Database export | `SELECT *` on a large table, `mysqldump`, `pg_dump`, `bcp` from an unusual account | Database audit log |
| Email | Auto-forward rule to an external address, many attachments sent to a personal address | Mail logs, M365 audit |

**Common false positives:** backup jobs, OS and software updates, video calls, developers pushing to code repositories, approved file transfers to partners, cloud sync clients after a new laptop setup.

## 3. Triage (first 15 to 30 minutes)

- [ ] Who and what: which user, which host, which destination?
- [ ] Is the destination approved (company tenant, a known partner, backup provider)? Check the domain owner and the tenant ID for cloud storage.
- [ ] How much data, over what time? Compare with that host's normal baseline.
- [ ] Is it still running?
- [ ] Is the user leaving the company, recently disciplined, or on a watch list? (Ask HR quietly; see [Insider Threat](insider-threat.md).)
- [ ] Are there signs of an external attacker on the same host (malware, new admin tools, unusual logins)?

Decision: approved destination or normal business, close with a note and maybe a tuning request; unapproved destination and still running, P2, contain now; regulated data likely involved, P1, call the CISO and legal; insider suspected, follow [Insider Threat](insider-threat.md) for discretion and HR involvement.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| What exact data left? | DLP match details, file names in EDR and SaaS audit logs, archive names, database tables queried |
| How much? | Bytes out per session in firewall, proxy, NetFlow; SaaS download counts |
| When did it start and stop? | First and last transfer; staging activity before the first transfer |
| Who did it: the user, or an attacker using the user's account? | Login sources, device, MFA method, other attacker signs on the host |
| Where did it go? | Destination domain and IP, cloud tenant, recipient email; can the provider take it down? |
| Was it encrypted or password-protected? | Archive parameters, tool command lines |
| Whose data is it? | Data owner; classification; whether it contains personal, payment or health data and for how many people |

### Queries: top outbound talkers compared with their own baseline

=== "Splunk SPL"

    ```spl
    index=firewall action=allowed direction=outbound earliest=-1d
    | stats sum(bytes_out) as today by src_ip
    | join type=left src_ip [ search index=firewall action=allowed direction=outbound earliest=-15d latest=-1d
        | bin _time span=1d | stats sum(bytes_out) as daily by src_ip, _time | stats avg(daily) as baseline by src_ip ]
    | eval ratio=round(today/baseline,1)
    | where today > 1073741824 AND (ratio > 5 OR isnull(baseline))
    | sort - today
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    let baseline = CommonSecurityLog
        | where TimeGenerated between (ago(15d) .. ago(1d))
        | summarize Daily = sum(SentBytes) by SourceIP, bin(TimeGenerated, 1d)
        | summarize Baseline = avg(Daily) by SourceIP;
    CommonSecurityLog
    | where TimeGenerated > ago(1d)
    | summarize Today = sum(SentBytes) by SourceIP
    | join kind=leftouter baseline on SourceIP
    | extend Ratio = round(Today / Baseline, 1)
    | where Today > 1073741824 and (Ratio > 5 or isempty(Baseline))
    | order by Today desc
    ```

=== "Elastic"

    ```text
    Lens visualisation: sum of source.bytes (or network.bytes) by source.ip, last 1 day,
    compared with the same chart for the previous 14 days. Then filter:
    destination.domain : (*mega.nz or *dropbox.com or *wetransfer.com or *file.io or *drive.google.com)
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT sourceip, SUM(bytessent) AS bytes_out, COUNT(*) AS flows
    FROM flows
    WHERE flowdirection = 'L2R'
    GROUP BY sourceip
    HAVING SUM(bytessent) > 1073741824
    ORDER BY bytes_out DESC LAST 24 HOURS
    ```

=== "Wazuh"

    ```text
    data.win.eventdata.image:(*rclone.exe or *winscp.exe or *megasync.exe) or
    data.win.eventdata.commandLine:(*rclone* or *mega:* or *"7z a -p"*)
    ```

=== "osquery"

    ```sql
    -- Transfer tools present or running on endpoints
    SELECT name, path, cmdline FROM processes
    WHERE name IN ('rclone.exe','rclone','winscp.exe','MEGAsync.exe','restic.exe')
       OR cmdline LIKE '%rclone%' OR cmdline LIKE '%mega:%';
    ```

### DNS tunnelling check

=== "Splunk SPL"

    ```spl
    index=dns
    | eval sub=mvindex(split(query,"."),0), parent=replace(query,"^[^.]+\.","")
    | eval sublen=len(sub)
    | stats count dc(sub) as unique_subs avg(sublen) as avg_len by parent
    | where unique_subs > 200 AND avg_len > 30
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    DnsEvents
    | extend Sub = tostring(split(Name, ".")[0]), Parent = strcat_array(array_slice(split(Name, "."), 1, -1), ".")
    | summarize Unique = dcount(Sub), AvgLen = avg(strlen(Sub)) by Parent
    | where Unique > 200 and AvgLen > 30
    ```

=== "Zeek"

    ```bash
    zeek-cut query < dns.log | awk -F. '{print $(NF-1)"."$NF, length($1)}' \
      | awk '$2>30 {c[$1]++} END {for (d in c) if (c[d]>200) print c[d], d}' | sort -rn | head
    ```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Block the destination domain, IP or cloud tenant at proxy and firewall | SOC | Block the specific tenant if the provider is also used by the business |
| Isolate the host if an attacker is suspected | SOC | Collect memory first if possible |
| Suspend the user's sessions and account, or remove sharing rights | Identity team | For an insider, coordinate timing with HR and legal first |
| Remove external sharing links and auto-forward rules | SaaS / email admin | Record the links before deleting them, they are evidence |
| Kill or block the transfer tool by hash and name | SOC | EDR custom indicator |
| Ask the cloud provider to preserve and remove the data | Legal | Providers act on legal requests; speed matters |

## 6. Eradication and recovery

- [ ] Remove attacker access and tools (if external); follow [Malware and Infostealer](malware-infostealer.md) or [Account Compromise](account-compromise.md).
- [ ] Block unapproved personal cloud storage by category at the proxy or CASB.
- [ ] Turn on or extend DLP policies for the data types involved.
- [ ] Restrict who can export from the affected database or SaaS app.
- [ ] Monitor dark web and leak sites for the data for 90 days.
- [ ] Watch the user, host and destination category for 30 days.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Incident lead, SOC manager | Immediately | Analyst |
| CISO, legal, privacy officer (DPO) | As soon as regulated or confidential data may be involved: legal clocks may be running | SOC manager |
| Data owner | To confirm what the data is and how sensitive | Incident lead |
| HR | Only if an employee is suspected, and only through the agreed channel | CISO or legal |
| Regulators and affected people | As legal decides (for example 72 hours under GDPR) | Legal |

See [Escalation and Communication](../03-incident-response/escalation-and-communication.md).

## 8. Evidence to keep

- Firewall, proxy, DNS, NetFlow and SaaS audit logs covering staging and transfer.
- DLP incident details and matched content (store securely; it is the sensitive data itself).
- Names, sizes and hashes of the archives and files transferred.
- EDR timeline of the host.
- Screenshots of sharing links and forwarding rules before removal.

Follow [Evidence Handling](../03-incident-response/evidence-handling.md). Insider cases may go to court: keep the chain of custody strict.

## 9. Lessons learned

For the [Post-Incident Review](../03-incident-response/post-incident-review.md):

- Was the data classified, and did anyone know where it lived?
- Did the user or account need access to that much data?
- Why was the destination allowed? Is there a sanctioned cloud storage list?
- Did DLP or volume alerts fire, and how long before someone looked?

Detections to add or tune: per-host outbound baseline, transfer tools by name and hash, archives with passwords, SaaS mass download, DNS tunnelling, external auto-forwarding.

## Downloads

- [PB-13 Data Exfiltration (Word)](../downloads/soc-kit/pb/PB-13-data-exfiltration.docx)

## Related pages

- [Insider Threat](insider-threat.md), [Ransomware](ransomware.md), [Cloud Account Compromise](cloud-account-compromise.md), [Business Email Compromise](business-email-compromise.md)
- [Evidence Handling](../03-incident-response/evidence-handling.md)
- [Escalation and Communication](../03-incident-response/escalation-and-communication.md)
