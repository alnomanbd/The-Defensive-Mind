# Log Source Priorities

Which logs to collect first. You cannot collect everything on day one, and you should not try. This page ranks log sources by how much detection value they give for the effort, so you get the most security for the least data and cost.

!!! abstract "At a glance"
    - Audience: security engineer, SOC lead, detection engineer
    - Time to read: 10 minutes
    - Outcome: an ordered list of what to onboard first, and what each source lets you detect

!!! tip "The guiding rule"
    Collect a log only if you will **detect or investigate** with it. Data you never query is cost and noise, not safety. Start narrow and deep, not wide and shallow.

## The priority order

| Priority | Source | Why it is high value | Detects |
|---|---|---|---|
| 1 | Identity (AD, Entra ID, Okta, Google) | Almost every attack uses an account | Brute force, password spraying, impossible travel, MFA abuse, new admin, risky sign-ins |
| 2 | Endpoints (EDR, Sysmon) | Where malware and hands-on attackers land | Malware, living-off-the-land, persistence, credential theft, ransomware behaviour |
| 3 | Perimeter (firewall, VPN, proxy) | The way in and the way data leaves | External scanning, VPN logins, command and control, data exfiltration |
| 4 | Cloud control plane (AWS CloudTrail, Azure, GCP audit) | Cloud attacks use the API, not malware | Key abuse, new identities, privilege changes, logging tampering, resource hijacking |
| 5 | Email and collaboration (M365, Google Workspace) | The top delivery path for attacks | Phishing, business email compromise, mailbox rules, OAuth consent abuse |
| 6 | Web and application (web server, WAF, app logs) | Internet-facing apps are constantly attacked | Web attacks, web shells, secret-file probing, account takeover on your apps |
| 7 | DNS | Quiet but powerful signal | Command and control, tunnelling, newly registered domains |
| 8 | SaaS apps (the ones holding your data) | Your data increasingly lives here | Mass download, external sharing, admin changes |

Work down this list. Get each source flowing, write a few detections on it, then move to the next. A SOC with sources 1 to 3 done well beats one with all eight done badly.

## What "done well" means for a source

Onboarding is not just pointing logs at the SIEM. For each source:

- [ ] The right events are collected (see below), not everything and not too little.
- [ ] Timestamps are correct and in one timezone (UTC is safest).
- [ ] The source is parsed into fields you can search (user, source IP, action).
- [ ] You have a detection or two actually using it.
- [ ] You alert when the source goes silent, so a blind spot does not pass unnoticed.

!!! warning "Silent log sources are invisible blind spots"
    The most dangerous gap is a log source everyone thinks is working but stopped weeks ago. Attackers also stop logging on purpose. Build a detection that fires when any important source sends nothing for too long. A SOC that does not watch its own inputs is monitoring a guess.

## What to collect from the top sources

You rarely need every event. The high-value ones:

| Source | Collect |
|---|---|
| Windows identity | 4624, 4625 (logon success and failure), 4768, 4769, 4771 (Kerberos), 4720, 4728, 4732, 4756 (account and group changes), 4698 (scheduled task), 4688 (process creation) |
| Identity provider | Sign-ins (with result and risk), audit logs, MFA events, app consent grants |
| Endpoints | EDR alerts plus Sysmon: process creation (1), network (3), file create (11), registry (13), DNS (22) |
| Firewall and VPN | Allowed and denied connections, VPN logins, bytes out per session |
| Cloud | All management events, all regions; data-plane events for sensitive storage |
| Email | Message trace, inbox rule changes, forwarding changes, mailbox audit |

## Managing cost and noise

Collecting more is not safer; it is more expensive and noisier. Control it:

- [ ] Filter at the source: drop debug and purely informational events you will never query.
- [ ] Keep hot (fast search) data short, for example 30 to 90 days, and archive the rest cheaply.
- [ ] Review which sources actually feed detections; drop or downsample ones that feed none.
- [ ] Watch your SIEM ingest volume as a number; a sudden jump is either a misconfiguration or an attack.

## A realistic first 90 days of onboarding

| Phase | Onboard |
|---|---|
| Days 1 to 30 | Identity and endpoints (EDR). These two alone catch a large share of real attacks |
| Days 31 to 60 | Perimeter (firewall, VPN) and, if you are in the cloud, the cloud control plane |
| Days 61 to 90 | Email and collaboration, then web and application logs for your internet-facing apps |

## Related pages

- [Use case prioritization](use-case-prioritization.md)
- [Technology stack](technology-stack.md)
- [Detection engineering](../05-detection-engineering/index.md)
- [Roadmap](roadmap.md)
