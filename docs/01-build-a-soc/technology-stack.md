# Technology Stack

The tools a SOC runs on, what each one is for, and how to choose without overspending. You can build a real SOC on open-source tools or on commercial ones; what matters is that the pieces fit and you can run them.

!!! abstract "At a glance"
    - Audience: SOC manager, security engineer, whoever signs off tool spend
    - Time to read: 12 minutes
    - Outcome: you know the core tool types, open-source and commercial options, and the order to buy

## The core pieces

| Tool | What it does | Can you start without it? |
|---|---|---|
| SIEM | Collects logs, correlates them, raises alerts, lets you search | No. This is the heart of the SOC |
| EDR or XDR | Detects and responds on endpoints; isolates hosts | Almost essential; endpoints are where most attacks land |
| SOAR or scripts | Automates repetitive triage and response | Later. Start by hand, automate what hurts |
| Case or ticket system | Tracks incidents and work | Yes, briefly; a shared board works to start |
| Threat intelligence platform (TIP) | Stores and applies threat data (indicators, context) | Later. A feed plus a watchlist is enough at first |

!!! note "What the acronyms mean"
    **SIEM**: security information and event management, your central log and alert platform. **EDR**: endpoint detection and response, the agent on laptops and servers. **XDR**: extended detection and response, EDR joined with network, email and cloud signals. **SOAR**: security orchestration, automation and response, the tool that runs playbooks for you. **TIP**: threat intelligence platform.

## SIEM: the heart

Everything flows into the SIEM. Choose it for what you can run and afford, not for the longest feature list.

| Option | Type | Notes |
|---|---|---|
| Wazuh | Open source | Free, includes agents, file integrity, and basic EDR features; good first SIEM for small teams |
| Elastic (ELK) and Elastic Security | Open source core, paid tiers | Powerful search; needs engineering effort to run well |
| Splunk | Commercial | Very capable; priced by data volume, can get expensive fast |
| Microsoft Sentinel | Commercial, cloud | Strong if you are a Microsoft and Azure shop; priced by data |
| Google SecOps (Chronicle) | Commercial, cloud | Large-scale, flat-ish pricing |

!!! warning "SIEM pricing is a trap"
    Most commercial SIEMs charge by how much data you send them. Sending every log "to be safe" can multiply the bill and bury real alerts in noise. Decide your log sources by detection value first ([Log source priorities](log-source-priorities.md)), then size the SIEM to that.

## EDR or XDR: where attacks land

Most intrusions touch an endpoint. A good EDR detects malicious behaviour, lets you investigate what a process did, and lets you isolate a host with one click.

| Option | Type | Notes |
|---|---|---|
| Wazuh, osquery, Velociraptor | Open source | Visibility and hunting; less automated prevention than commercial EDR |
| Microsoft Defender for Endpoint | Commercial | Strong, bundled with some Microsoft licences |
| CrowdStrike, SentinelOne | Commercial | Leading EDR and XDR; strong prevention and response |

For a small SOC, an EDR that can **isolate a host without a full investigation first** is worth a lot: it turns a two-hour containment into two minutes.

## Supporting tools

| Need | Open source | Commercial |
|---|---|---|
| Case management | TheHive, IRIS | ServiceNow SecOps, Jira with a security workflow |
| Automation (SOAR) | Shuffle, n8n, custom scripts | Tines, Splunk SOAR, Palo Alto XSOAR |
| Threat intel | MISP, OpenCTI | Recorded Future, Mandiant, Anomali |
| Forensics and DFIR | Velociraptor, KAPE, Volatility, Plaso | Magnet AXIOM, EnCase |
| Network visibility | Zeek, Suricata, Arkime | Corelight, Darktrace |
| Detection as code | Sigma, Git, CI pipelines | Vendor detection content |

## How to choose, in order

- [ ] Start from your log sources and detections, not from a product demo.
- [ ] Pick a SIEM you can actually run with the people you have. A simpler tool you operate well beats a powerful one you cannot.
- [ ] Get EDR on your important endpoints early; it gives the most detection and response value per dollar.
- [ ] Use a simple case system at first; add a proper one when volume demands it.
- [ ] Automate by hand first, then with scripts, then with a SOAR. Do not buy automation for a process you have not yet defined.
- [ ] Add a TIP only when you have alerts to enrich and people to use it.

!!! tip "Open source is a real choice, not a poor one"
    A small team can run a strong SOC on Wazuh, osquery, Velociraptor, Suricata, MISP and TheHive, all free. The cost moves from licences to engineering time. If you have the skills, open source gives you control and no per-gigabyte surprise. If you do not, pay for tools that run themselves.

## Integration matters more than any single tool

The value is in the pieces working together: an alert in the SIEM that opens a case, enriches with threat intel, and offers a one-click host isolation through the EDR. Before buying anything, check it can talk to what you already have through APIs. A best-in-class tool that integrates with nothing creates more manual work, not less.

## Related pages

- [Log source priorities](log-source-priorities.md)
- [Use case prioritization](use-case-prioritization.md)
- [Automation (SOAR)](../07-automation-soar/index.md)
- [Budget and staffing](budget-and-staffing.md)
