# Evidence Handling

How to collect, protect and record digital evidence during an incident so that it can be trusted later: by your own team, auditors, insurers, HR, or a court. Collect in the right order, hash everything, and record every hand that touches it.

!!! abstract "At a glance"
    - Audience: L2 / L3 analysts, forensic responders, incident leads
    - Time to read: 15 minutes
    - Outcome: you can collect volatile and disk evidence with free tools and keep a defensible chain of custody

## Four principles

| Principle | Meaning |
|---|---|
| Order of volatility | Collect what disappears first: memory and network state before disk, disk before logs that rotate in weeks |
| Integrity | Hash every item (SHA-256) at collection and every time it moves |
| Chain of custody | A written record of who had the evidence, when, and why, from collection to disposal |
| Minimal change | Use trusted tools from external media; never browse or "have a look" on the suspect machine first |

## Order of volatility

| Order | What | Lost when |
|---|---|---|
| 1 | Memory (RAM): processes, network connections, injected code, keys | Reboot or shutdown |
| 2 | Live system state: running processes, open connections, logged-on users, ARP and DNS cache | Minutes to hours |
| 3 | Temporary files, swap, hibernation file | Reboot, normal use |
| 4 | Disk: files, registry, event logs, browser history | Overwritten over days |
| 5 | Remote logs: SIEM, firewall, proxy, cloud audit logs | Retention period (often 30 to 90 days) |
| 6 | Backups and archives | Retention policy |

!!! danger "Before you isolate or reboot"
    EDR network isolation keeps the machine powered on, so memory survives. Rebooting or reimaging destroys layers 1 to 3. Unless damage is happening right now, collect memory first.

## Live response collection

### Windows

=== "Velociraptor"

    ```text
    Collected artifacts > New collection > target host
    Artifacts: Windows.KapeFiles.Targets (target: _SANS_Triage),
               Windows.Memory.Acquisition, Windows.Network.Netstat,
               Windows.System.Pslist, Windows.Sys.Users
    ```

=== "KAPE"

    ```bat
    REM Run from a USB drive or network share, output to external storage
    kape.exe --tsource C: --tdest E:\Case1042\WS-0142\triage --target !SANS_Triage --vhdx WS-0142 --zv false
    ```

=== "Memory with WinPmem"

    ```bat
    winpmem_mini_x64.exe E:\Case1042\WS-0142\memory.raw
    certutil -hashfile E:\Case1042\WS-0142\memory.raw SHA256
    ```

=== "Built-in commands"

    ```bat
    REM Quick state capture when no tools are available (save output to external media)
    tasklist /v > E:\Case1042\tasklist.txt
    netstat -anob > E:\Case1042\netstat.txt
    query user > E:\Case1042\users.txt
    schtasks /query /fo LIST /v > E:\Case1042\schtasks.txt
    wmic service get name,pathname,startmode,state > E:\Case1042\services.txt
    ```

### Linux

=== "Velociraptor"

    ```text
    Artifacts: Linux.Collection.UAC (or Linux.KapeFiles-style triage),
               Linux.Sys.Pslist, Linux.Network.Netstat, Linux.Sys.Users, Linux.Sys.Crontab
    ```

=== "UAC"

    ```bash
    # Unix-like Artifacts Collector, output to mounted external storage
    ./uac -p ir_triage /mnt/evidence/case1042/srv-web01
    ```

=== "Memory with AVML"

    ```bash
    sudo ./avml /mnt/evidence/case1042/srv-web01/memory.lime
    sha256sum /mnt/evidence/case1042/srv-web01/memory.lime
    ```

=== "Built-in commands"

    ```bash
    ps auxwwf > /mnt/evidence/ps.txt
    ss -tupan > /mnt/evidence/ss.txt
    who -a > /mnt/evidence/who.txt
    last -Faiwx > /mnt/evidence/last.txt
    crontab -l > /mnt/evidence/crontab_root.txt; ls -la /etc/cron.* > /mnt/evidence/cron_dirs.txt
    find / -xdev -mtime -7 -type f 2>/dev/null > /mnt/evidence/modified_7d.txt
    ```

=== "osquery"

    ```sql
    -- Quick live picture across many hosts at once
    SELECT pid, name, path, cmdline, parent FROM processes;
    SELECT * FROM process_open_sockets WHERE remote_address NOT IN ('', '0.0.0.0', '127.0.0.1', '::');
    SELECT * FROM logged_in_users;
    ```

### Cloud

| Cloud | Preserve |
|---|---|
| AWS | CloudTrail (all regions), VPC Flow Logs, GuardDuty findings, EBS snapshots of affected instances, S3 access logs |
| Azure and Microsoft 365 | Entra ID sign-in and audit logs, Unified Audit Log export, Activity Log, VM disk snapshots |
| Google Cloud | Cloud Audit Logs, VPC Flow Logs, disk snapshots |

Export cloud logs early: default retention can be as short as 7 to 90 days.

## Disk imaging

| Situation | Approach |
|---|---|
| Physical laptop or desktop | Write-blocked image with FTK Imager or `dc3dd`, or a Velociraptor/KAPE triage collection when a full image is not needed |
| Virtual machine | Snapshot the disk and export it; record the snapshot ID |
| Cloud instance | Disk snapshot, then create a volume from it in an isolated forensic account |

```bash
# Linux: image a disk with hashing, to external storage
sudo dc3dd if=/dev/sdb of=/mnt/evidence/case1042/laptop01.dd hash=sha256 log=/mnt/evidence/case1042/laptop01.log
```

## Hashing and storage

- [ ] SHA-256 for every file and image, written in the chain of custody form
- [ ] Store evidence on dedicated, encrypted storage with access limited to the investigation team
- [ ] Keep the original untouched; analyse a verified copy
- [ ] Record the storage location in the case

```bash
sha256sum memory.raw triage.vhdx > SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

## Chain of custody record

| Field | Example |
|---|---|
| Evidence ID | CASE1042-E03 |
| Description | Memory image of WS-0142 |
| Collected by, date and time (UTC) | A. Analyst, 2026-11-04 10:42 |
| Tool and version | WinPmem 4.0 |
| SHA-256 | 9f2c... |
| Storage location | Evidence share \\FOR01\case1042\ (encrypted) |
| Transfers | Each with from, to, date, time, reason, signature |

## When it may go to HR, legal or court

- [ ] Ask legal **before** collecting from an employee's device in an insider case
- [ ] Apply a legal hold: suspend deletion of the relevant logs, mailboxes and backups
- [ ] Do not let analysts interview staff unless HR and legal agree
- [ ] Consider an outside forensic firm for anything likely to reach court

## Tools summary

| Need | Free and open source | Commercial |
|---|---|---|
| Fleet live response and triage | Velociraptor, osquery | CrowdStrike RTR, Microsoft Defender Live Response, SentinelOne |
| Triage collection | KAPE, UAC, CyLR | Magnet AXIOM Cyber |
| Memory acquisition | WinPmem, AVML, LiME | Magnet RAM Capture (free), Belkasoft |
| Memory analysis | Volatility 3, MemProcFS | |
| Disk imaging | dc3dd, FTK Imager (free), Guymager | |
| Timeline | Plaso (log2timeline), Timesketch, Hayabusa, Chainsaw | |

## Downloads

- SOP-36 Evidence Collection and Chain of Custody and TPL-12 Chain of Custody Form are on the [SOC Document Kit](../soc-kit/index.md) plan.

## Related pages

- [IR lifecycle](ir-lifecycle.md)
- [Case management](../02-daily-operations/case-management.md)
- [Insider threat playbook](../04-playbooks/insider-threat.md)
