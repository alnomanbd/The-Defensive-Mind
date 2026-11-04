# SOC Training

A step-by-step training track for SOC analysts, from the first day on shift to L3 work. It is separate from the handbook: the handbook tells you how to run the SOC, the training teaches you the skills behind it.

!!! abstract "At a glance"
    - Audience: new and working SOC analysts (L1 to L3), and anyone moving into a SOC
    - Time: each module takes 4 to 10 hours, including labs
    - Outcome: the skills to work any SOC, on any common SIEM, EDR or SOAR platform

## How each module works

| Part | What you do |
|---|---|
| Lessons | Short explanations, three lines of theory at most before you do something |
| Labs | Hands-on tasks in a free lab (Wazuh, Elastic, Splunk free, Velociraptor, Sysmon, Zeek and more) |
| Query drills | The same question answered in Splunk SPL, Microsoft KQL, Elastic, IBM QRadar AQL and Wazuh, plus osquery SQL for endpoints, Sigma for portable rules and YARA for files |
| Self-check | A short quiz and a practical task to prove you can do it |
| Links to the kit | The SOPs, playbooks and forms from the [SOC Document Kit](../soc-kit/index.md) that use this skill |

## Modules

All modules are being written. They will appear in the menu one by one; see the [roadmap](https://github.com/alnomanbd/The-Defensive-Mind/blob/main/ROADMAP.md).

| Module | What you learn | Level |
|---|---|---|
| T01 SOC Foundations | What a SOC does, tiers, the alert lifecycle, true and false positives, severity, the daily rhythm and reports | L1 |
| T02 SIEM Platforms | Splunk, Microsoft Sentinel, Elastic and OpenSearch, IBM QRadar and Wazuh: how they work and how to search them | L1 to L2 |
| T03 Log Sources Every Analyst Must Know | Windows event IDs, Sysmon, Linux auth and auditd, web, firewall, proxy, DNS, email, identity and cloud audit logs | L1 to L2 |
| T04 Endpoint Security | EPP and next-generation antivirus, EDR, XDR, MDR, UEBA, NDR, DLP, host intrusion prevention, application allow-listing, device control, file integrity monitoring, Sysmon, osquery fleet queries, Wazuh agent, Velociraptor, MDM and UEM, CIS hardening | L1 to L3 |
| T05 Network Security Monitoring | Zeek, Suricata, NetFlow, packet capture basics, DNS and proxy analysis | L2 |
| T06 Email, Identity and Cloud Security | Mail flow and headers, Microsoft Entra ID and Okta sign-in logs, AWS, Azure and Google Cloud audit logs | L2 |
| T07 Threat Intelligence | The intelligence lifecycle, requirements, Cyber Kill Chain, Diamond Model, MITRE ATT&CK, Pyramid of Pain, STIX and TAXII, MISP and OpenCTI, writing intel reports | L2 to L3 |
| T08 Threat Hunting | Hypothesis, intel and analytics driven hunts, live hunting with osquery and Velociraptor, YARA sweeps, the PEAK and TaHiTI models, a hunt library by ATT&CK tactic, turning hunts into detections | L3 |
| T09 Detection Engineering | Detection as code, writing Sigma and YARA rules, converting Sigma to every SIEM, testing with Atomic Red Team, MITRE Caldera and Infection Monkey, tuning, ATT&CK coverage | L2 to L3 |
| T10 Incident Response | The incident response lifecycle in depth, containment decisions, communication, major incidents, tabletop practice | L2 to L3 |
| T11 DFIR | Windows, Linux, memory, network, cloud and email forensics, building timelines, KAPE, Velociraptor, Volatility, Plaso, chain of custody | L3 |
| T12 Malware Analysis Basics | A safe lab, static and dynamic triage, sandboxes, writing YARA rules from samples | L2 to L3 |
| T13 SOAR and Automation | What to automate, enrichment, case creation, approval steps, n8n and Shuffle examples | L2 to L3 |
| T14 SOC Management | KPIs, staffing and shifts, reporting to management, maturity, budget | Lead and manager |
| T15 Career and Interviews | Skill paths from L1 to L3, certifications, an interview question bank with model answers | All |

## Suggested order

- [ ] New to SOC: T01, T02, T03, then T04 and T10
- [ ] Moving to L2: T05, T06, T07, T09, T12
- [ ] Moving to L3: T08, T11, T13
- [ ] Leading a team: T14
- [ ] Before any interview: T15

## Related pages

- [Field guide by role](../field-guide/index.md)
- [Daily routine](../02-daily-operations/daily-routine.md)
- [SOC Document Kit](../soc-kit/index.md)
