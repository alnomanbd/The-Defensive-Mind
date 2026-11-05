# T04: Endpoint Security

Most attacks land on an endpoint, so endpoint security is where a SOC catches and stops them. This module covers the full family of endpoint defences, what each acronym means, and the free tools you can practise with.

!!! abstract "At a glance"
    - Level: L1 to L3
    - Time: 8 to 10 hours with labs
    - Outcome: you understand the endpoint security stack and can investigate and respond on a host

## Learning objectives

- [ ] Explain the endpoint security family: EPP, EDR, XDR, MDR, UEBA, NDR, DLP, and where each fits.
- [ ] Read an EDR process tree and decide if behaviour is malicious.
- [ ] Use osquery to ask live questions across many hosts.
- [ ] Collect host triage data with Velociraptor.
- [ ] Isolate a host and understand what isolation does and does not do.
- [ ] Know the hardening basics that reduce endpoint attacks.

## Lessons

1. **The acronyms, in order.** EPP and next-generation antivirus (prevention), EDR (detect and respond on endpoints), XDR (EDR joined with network, email, cloud), MDR (a provider runs it for you).
2. **The wider family.** UEBA (user and entity behaviour analytics), NDR (network detection and response), DLP (data loss prevention), host intrusion prevention, application allow-listing, device control, file integrity monitoring.
3. **Reading an EDR.** The process tree, parent and child, network connections, file writes, and how to spot living-off-the-land.
4. **osquery.** Asking SQL questions of your fleet: processes, sockets, users, autoruns.
5. **Velociraptor.** Live response and triage collection across hosts.
6. **Response.** Host isolation (keeps memory, cuts the network), and when to isolate versus power off.
7. **Hardening.** CIS benchmarks, standard-user accounts, application control, patching, and why they cut attacks off early.

## Lab

- [ ] Install an EDR or at least Sysmon plus osquery on a Windows VM.
- [ ] Run a benign "suspicious" action (encoded PowerShell downloading a file in the lab); read the process tree.
- [ ] Use osquery to list processes with outbound connections.
- [ ] Use Velociraptor to pull a triage collection from the VM.
- [ ] Practise isolating the host (in the lab) and confirm what still works.

### osquery drill

```sql
-- Processes running from user-writable folders with network connections
SELECT p.pid, p.name, p.path, s.remote_address, s.remote_port
FROM processes p JOIN process_open_sockets s USING (pid)
WHERE (p.path LIKE '%\AppData\%' OR p.path LIKE '%\Downloads\%')
  AND s.remote_address NOT IN ('', '127.0.0.1', '::');
```

## Self-check

1. What is the difference between EDR and XDR?
2. Why does EDR isolation keep the machine powered on?
3. What does application allow-listing stop that antivirus often misses?

??? note "Answers"
    1. EDR detects and responds on the endpoint; XDR joins endpoint telemetry with network, email and cloud for a broader picture.
    2. To preserve memory (processes, keys, network state) for analysis, and to allow remote response, while cutting the attacker's network access.
    3. It stops unknown or unsigned programs from running at all, including new malware that has no signature yet.

## Links to the handbook and kit

- [Malware and infostealer playbook](../../04-playbooks/malware-infostealer.md)
- [Evidence handling](../../03-incident-response/evidence-handling.md)
- [Technology stack](../../01-build-a-soc/technology-stack.md)

## Next module

[T05 Network Security Monitoring](../t05-network-security-monitoring/index.md).
