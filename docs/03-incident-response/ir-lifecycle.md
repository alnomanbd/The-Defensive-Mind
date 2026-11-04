# IR Lifecycle

How to run an incident from the moment it is declared to the moment it is closed. Based on the phases in NIST SP 800-61 (preparation, detection and analysis, containment, eradication and recovery, post-incident activity), written as the actions an incident lead actually takes.

!!! abstract "At a glance"
    - Audience: incident leads, L2 / L3 analysts
    - Time to read: 15 minutes
    - Outcome: you can lead an incident through every phase and know what "done" means for each

## Phase 0: Preparation (before anything happens)

You cannot prepare during an incident. Have these ready:

- [ ] Severity scale and escalation matrix, with phone numbers that work at night
- [ ] Playbooks for your top incident types
- [ ] Access for responders: EDR isolation, account disable, firewall block, cloud console, backup restore
- [ ] An out-of-band channel (phone bridge, a chat workspace not tied to your main identity provider) in case email and chat are compromised
- [ ] Forensic tools and storage ready (see [evidence handling](evidence-handling.md))
- [ ] Contracts and contacts: incident response retainer, cyber insurer, legal counsel, law enforcement contact
- [ ] Backups that are offline or immutable, and a tested restore
- [ ] Logs kept long enough to investigate (90 days searchable as a minimum)

## Phase 1: Declare (first 15 minutes)

1. Confirm it is an incident, not just an alert (true positive with impact or clear intent).
2. Set **severity** ([classification](incident-classification.md)).
3. Name the **incident lead** and a **scribe**.
4. Open the **case**, the **incident channel** and, for P1/P2, a **bridge call**.
5. Start the **timeline** and record the declaration time.
6. Escalate per the matrix ([escalation and communication](escalation-and-communication.md)).

## Phase 2: Scope (investigate)

Answer these, in this order:

| Question | Typical evidence |
|---|---|
| What is the first known malicious activity? | EDR process tree, authentication logs, email logs |
| Which accounts are involved? | Identity provider sign-ins, Windows 4624/4625/4768/4769, VPN |
| Which hosts are involved? | EDR, Sysmon, network flows, lateral movement events (4624 type 3 and 10) |
| Is the attacker still active? | Recent connections to suspicious IPs, new logins, new processes |
| What data was accessed or taken? | File access logs, proxy and firewall egress volume, cloud storage logs |
| How did they get in? | First host, first account, email or exploit evidence |

### Scoping sweeps

Once you have indicators (IP, domain, hash, user), sweep everything:

=== "Splunk SPL"

    ```spl
    index=* ("203.0.113.10" OR "evil.example" OR "jdoe") earliest=-30d
    | stats count min(_time) as first max(_time) as last values(host) as hosts by sourcetype
    | convert ctime(first) ctime(last)
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    search in (SigninLogs, DeviceNetworkEvents, DeviceProcessEvents, CommonSecurityLog, OfficeActivity)
        "203.0.113.10" or "evil.example" or "jdoe"
    | where TimeGenerated > ago(30d)
    | summarize Count = count(), First = min(TimeGenerated), Last = max(TimeGenerated) by $table
    ```

=== "Elastic"

    ```text
    KQL in Discover, last 30 days:
    source.ip : "203.0.113.10" or destination.ip : "203.0.113.10" or dns.question.name : "evil.example" or user.name : "jdoe"
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT LOGSOURCENAME(logsourceid) AS source, sourceip, destinationip, username,
      MIN(starttime) AS first_seen, MAX(starttime) AS last_seen, COUNT(*) AS n
    FROM events
    WHERE sourceip = '203.0.113.10' OR destinationip = '203.0.113.10' OR username = 'jdoe'
    GROUP BY logsourceid, sourceip, destinationip, username LAST 30 DAYS
    ```

=== "Wazuh"

    ```text
    data.srcip:"203.0.113.10" or data.dstip:"203.0.113.10" or data.srcuser:"jdoe" or data.dstuser:"jdoe"
    ```

=== "osquery"

    ```sql
    -- Live: which endpoints are talking to the IOC right now
    SELECT p.name, p.path, s.remote_address, s.remote_port
    FROM process_open_sockets s JOIN processes p USING (pid)
    WHERE s.remote_address = '203.0.113.10';
    ```

## Phase 3: Contain

Stop the spread **without destroying evidence** and with the right approval.

| Situation | Short-term containment | Who approves |
|---|---|---|
| Malware on a laptop | EDR network isolation (keeps the host on for forensics) | On-call analyst may act alone |
| Compromised user account | Disable account, revoke sessions and refresh tokens, reset MFA | On-call analyst may act alone |
| Compromised server | Isolate or move to a quarantine VLAN; snapshot first if virtual | Incident lead plus system owner |
| Attacker C2 server | Block IP and domain at firewall, proxy and DNS | Incident lead |
| Data leaving now | Block destination, disable the exfil account, cut the link if needed | Incident lead; executive if business impact |
| Ransomware spreading | Isolate affected segments, disable compromised admin accounts, stop file shares if needed | Incident lead plus executive sponsor |
| Compromised cloud keys | Deactivate keys, attach deny policy, rotate secrets | Incident lead plus cloud owner |

!!! warning "Contain quietly when you can"
    If the attacker is still active and you contain one host at a time, they may notice and change tactics. For a confirmed active intrusion, plan containment of **all** known footholds at the same moment.

!!! danger "Do not"
    Do not reboot, reimage or power off a compromised machine before collecting volatile evidence (memory, running processes, network connections), unless damage is happening right now.

## Phase 4: Eradicate

- [ ] Remove malware, persistence (scheduled tasks, services, run keys, cron, new accounts, OAuth apps, mailbox rules)
- [ ] Reset every credential the attacker could have touched; for domain compromise, reset the KRBTGT account twice
- [ ] Patch or reconfigure the weakness used to get in
- [ ] Re-sweep with all indicators to confirm nothing is left

## Phase 5: Recover

- [ ] Restore from known-good backups or rebuild from clean images
- [ ] Bring systems back in stages, most important first, with extra monitoring
- [ ] Watch for re-infection for at least 2 to 4 weeks (add temporary detections for this attacker's indicators and behaviours)
- [ ] Release containment (un-isolate hosts, re-enable accounts) and record it

## Phase 6: Close and learn

- [ ] Final report for P1 and P2 within 10 working days
- [ ] Post-incident review ([page](post-incident-review.md))
- [ ] Actions tracked to completion
- [ ] New detections and playbook updates in place

## Phase exit criteria

| Phase | Done when |
|---|---|
| Declare | Severity set, lead named, channel open, first notification sent |
| Scope | You can list affected hosts, accounts and data, and the entry point, with evidence |
| Contain | No new attacker activity for an agreed period while monitoring |
| Eradicate | All persistence removed, credentials reset, entry point closed, clean re-sweep |
| Recover | Business service normal, monitoring in place |
| Close | Report and review done, actions owned |

## Related pages

- [Incident classification](incident-classification.md)
- [Escalation and communication](escalation-and-communication.md)
- [Evidence handling](evidence-handling.md)
- [Playbooks](../04-playbooks/index.md)
