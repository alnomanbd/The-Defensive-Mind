# T03: Log Sources Every Analyst Must Know

You cannot investigate what you cannot see. This module teaches the log sources a SOC lives on: what each contains, the key events, and how to read them. Know these and most investigations become straightforward.

!!! abstract "At a glance"
    - Level: L1 to L2
    - Time: 6 to 8 hours with labs
    - Outcome: you know the top log sources, their key events, and what each one lets you detect

## Learning objectives

- [ ] Name the priority log sources and what each is for.
- [ ] Recognise the key Windows event IDs and Sysmon events.
- [ ] Read Linux auth and auditd logs.
- [ ] Read web, firewall, proxy and DNS logs.
- [ ] Read email, identity and cloud audit logs.
- [ ] Know which source answers which investigation question.

## Lessons

1. **Why log sources are ranked.** Identity and endpoints first; the [log source priorities](../../01-build-a-soc/log-source-priorities.md) order and why.
2. **Windows.** Logon events (4624, 4625), Kerberos (4768, 4769, 4771), account and group changes (4720, 4728, 4732), process creation (4688), scheduled tasks (4698), services (7045).
3. **Sysmon.** Process creation (1), network (3), file create (11), registry (13), DNS (22), and why Sysmon beats default logging.
4. **Linux.** `auth.log` and `secure` for logins and sudo, auditd for deeper tracking, shell history, cron.
5. **Network and web.** Firewall allow and deny, proxy, DNS queries, and web access logs (status codes and sizes).
6. **Email, identity and cloud.** Message trace and inbox rules, sign-in and audit logs, cloud control-plane logs.
7. **Mapping questions to sources.** "Did they log in" to identity; "what did the process do" to endpoint; "what left" to proxy and firewall.

## Lab

- [ ] Turn on Sysmon with a community configuration on a Windows VM.
- [ ] Create a new local admin account; find the 4720 and 4732 events.
- [ ] Run an encoded PowerShell command; find it in Sysmon event 1.
- [ ] On a Linux VM, make a failed and then successful SSH login; find both in `auth.log`.
- [ ] For each, write which field tells you the user and the source.

## Self-check

1. Which Windows event tells you a logon succeeded, and which that it failed?
2. Why is Sysmon worth adding when Windows already logs?
3. You need to know what a suspicious process connected to. Which log source?

??? note "Answers"
    1. 4624 is a successful logon; 4625 is a failed logon.
    2. Sysmon logs rich process, network, file and registry events that default Windows logging does not, with consistent detail that detections rely on.
    3. Endpoint telemetry: Sysmon event 3 (network connection) or EDR network events, and the proxy or firewall for the destination.

## Links to the handbook and kit

- [Log source priorities](../../01-build-a-soc/log-source-priorities.md)
- [Investigation cheat sheet](../../field-guide/investigation-cheatsheet.md)
- [Threat hunting](../../02-daily-operations/threat-hunting.md)

## Next module

[T04 Endpoint Security](../t04-endpoint-security/index.md).
