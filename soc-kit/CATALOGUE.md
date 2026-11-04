# SOC Document Kit: Catalogue

Editable Word (.docx) documents that a SOC needs to run, written for any organisation. Every document uses `[ORGANISATION]` and other bracketed placeholders, so it can be adapted in minutes.

Source files live in `soc-kit/src/`. `python soc-kit/build.py` turns them into Word files under `docs/downloads/soc-kit/`, which the website serves.

Status: **Done** = published, **Next** = in the current batch, blank = planned.

## GOV: Governance (the rules of the SOC)

| ID | Document | Status |
|---|---|---|
| GOV-01 | SOC Charter | |
| GOV-02 | Operating Model and Service Catalogue | |
| GOV-03 | Severity, Priority and SLA Standard | |
| GOV-04 | Escalation and Contact Matrix | |
| GOV-05 | SOC RACI | |
| GOV-06 | Incident Response Policy | |
| GOV-07 | Log Management and Retention Policy | |
| GOV-08 | SOC Metrics and KPI Standard | |
| GOV-09 | SOC Roadmap and Maturity Plan | |
| GOV-10 | Privacy and Data Handling in Investigations | |

## SOP: Standard Operating Procedures (how routine work is done)

| ID | Document | Area | Status |
|---|---|---|---|
| SOP-01 | Shift Start and Platform Health Check | Daily operations | Done |
| SOP-02 | Alert Queue Monitoring | Daily operations | Done |
| SOP-03 | Alert Triage and Classification (TP, FP, BTP) | Daily operations | Done |
| SOP-04 | Alert Enrichment (IP, domain, hash, user, host) | Daily operations | Done |
| SOP-05 | Severity Assignment and Escalation | Daily operations | Done |
| SOP-06 | Shift Handover | Daily operations | Done |
| SOP-07 | On-Call and After-Hours Response | Daily operations | Done |
| SOP-08 | Case Management (open, merge, close) | Daily operations | Done |
| SOP-09 | Daily, Weekly and Monthly Reporting | Daily operations | Done |
| SOP-10 | False Positive Handling and Tuning Requests | Daily operations | Done |
| SOP-11 | Log Source Onboarding | Detection and platform | |
| SOP-12 | Log Source Health and Silent Source Response | Detection and platform | |
| SOP-13 | Detection Rule Lifecycle | Detection and platform | |
| SOP-14 | Detection Testing with Atomic Red Team, MITRE Caldera and Infection Monkey | Detection and platform | |
| SOP-15 | SIEM Platform Maintenance (patching, retention, backup) | Detection and platform | |
| SOP-16 | SOC Tool Access and Account Review | Detection and platform | |
| SOP-17 | SOC Change Management | Detection and platform | |
| SOP-18 | EDR and XDR Alert Handling | Endpoint | |
| SOP-19 | Host Isolation and Release | Endpoint | |
| SOP-20 | Endpoint Agent Deployment and Health | Endpoint | |
| SOP-21 | UEBA Anomaly Review | Endpoint | |
| SOP-22 | Device Control and USB Exceptions | Endpoint | |
| SOP-23 | Reported Phishing Mailbox Handling | Email and identity | |
| SOP-24 | Email Search and Purge | Email and identity | |
| SOP-25 | Account Disable and Session Revocation | Email and identity | |
| SOP-26 | Privileged Access Monitoring | Email and identity | |
| SOP-27 | Firewall, WAF and Proxy Block Requests | Network and cloud | |
| SOP-28 | Network IDS Alert Handling (Suricata, Zeek) | Network and cloud | |
| SOP-29 | Cloud Security Alert Handling | Network and cloud | |
| SOP-30 | Critical Vulnerability and Zero-Day Response | Network and cloud | |
| SOP-31 | Threat Intelligence Feed Management | Threat intelligence | |
| SOP-32 | IOC Lifecycle (add, sweep, expire) | Threat intelligence | |
| SOP-33 | Threat Advisory and Flash Reports | Threat intelligence | |
| SOP-34 | Dark Web and Brand Monitoring | Threat intelligence | |
| SOP-35 | Threat Hunt Execution | Threat hunting | |
| SOP-36 | Evidence Collection and Chain of Custody | DFIR | |
| SOP-37 | Live Response and Triage Collection | DFIR | |
| SOP-38 | Memory Acquisition | DFIR | |
| SOP-39 | Disk Imaging | DFIR | |
| SOP-40 | Malware Sample Handling and Sandbox Analysis | DFIR | |
| SOP-41 | Log Preservation and Legal Hold | DFIR | |
| SOP-42 | Major Incident and War Room | Incident management | |
| SOP-43 | Incident Communication and Stakeholder Updates | Incident management | |
| SOP-44 | Post-Incident Review | Incident management | |
| SOP-45 | Tabletop Exercise | Incident management | |
| SOP-46 | Purple Team Exercise | Incident management | |
| SOP-47 | Analyst Onboarding | People and knowledge | |
| SOP-48 | Knowledge Base Maintenance | People and knowledge | |
| SOP-49 | SOC Business Continuity (SIEM or tooling down) | People and knowledge | |
| SOP-50 | Quality Assurance and Case Review | People and knowledge | |

## PB: Incident Response Playbooks (what to do when a specific attack happens)

| ID | Playbook | Status |
|---|---|---|
| PB-01 | Phishing | |
| PB-02 | Business Email Compromise (BEC) | |
| PB-03 | Account Compromise | |
| PB-04 | Brute Force and Password Spraying | |
| PB-05 | Credential Leak and Dark Web Exposure | |
| PB-06 | MFA Fatigue and MFA Bypass | |
| PB-07 | Impossible Travel and Suspicious Sign-in | |
| PB-08 | Malware and Infostealer | |
| PB-09 | Ransomware | |
| PB-10 | Web Shell | |
| PB-11 | Web Application Attack (SQL injection, XSS, path traversal) | |
| PB-12 | Vulnerability Exploitation and Zero-Day | |
| PB-13 | Data Exfiltration | |
| PB-14 | Insider Threat | |
| PB-15 | DDoS | |
| PB-16 | Cloud Account Compromise | |
| PB-17 | Cloud Storage Exposure | |
| PB-18 | Cryptomining and Cryptojacking | |
| PB-19 | Lateral Movement | |
| PB-20 | Privilege Escalation | |
| PB-21 | Credential Dumping | |
| PB-22 | Command and Control (C2) Beaconing | |
| PB-23 | DNS Tunnelling | |
| PB-24 | Living off the Land and Suspicious Scripts | |
| PB-25 | Log Clearing and Defence Evasion | |
| PB-26 | Rogue Admin and Unauthorised Account | |
| PB-27 | Unauthorised Scanning and Reconnaissance | |
| PB-28 | Lost or Stolen Device | |
| PB-29 | USB and Removable Media | |
| PB-30 | Supply Chain Compromise | |
| PB-31 | Secrets Leaked in Code Repositories | |
| PB-32 | API Abuse | |
| PB-33 | Container and Kubernetes Compromise | |
| PB-34 | AI and LLM Abuse (prompt injection, data leakage) | |
| PB-35 | SIM Swap | |
| PB-36 | Wiper and Destructive Attack | |
| PB-37 | Rootkit and Bootkit | |
| PB-38 | Rogue Wi-Fi and Network Device | |
| PB-39 | Third-Party and Vendor Breach | |
| PB-40 | Website Defacement | |

## TPL: Forms, Reports and Records (what the SOC fills in)

| ID | Document | Used | Status |
|---|---|---|---|
| TPL-01 | Daily Shift Report | Every shift | Done |
| TPL-02 | Shift Handover | Every shift change | Done |
| TPL-03 | Weekly SOC Report | Weekly | Done |
| TPL-04 | Monthly SOC Report | Monthly | Done |
| TPL-05 | Quarterly Executive Report | Quarterly | Done |
| TPL-06 | Annual SOC Report | Yearly | Done |
| TPL-07 | Incident Report: Initial Notification | Per incident | |
| TPL-08 | Incident Report: Final | Per incident | |
| TPL-09 | Incident Timeline and Decision Log | Per incident | |
| TPL-10 | Post-Incident Review | Per incident | |
| TPL-11 | Situation Report (sitrep) for Stakeholders | During major incidents | |
| TPL-12 | Evidence Chain of Custody Form | Per evidence item | |
| TPL-13 | Forensic Acquisition Record | Per acquisition | |
| TPL-14 | Malware Analysis Report | Per sample | |
| TPL-15 | Threat Hunt Record | Per hunt | |
| TPL-16 | Hunt Hypothesis Request | As needed | |
| TPL-17 | Threat Intelligence Flash Advisory | As needed | |
| TPL-18 | Threat Landscape Report | Quarterly | |
| TPL-19 | IOC Submission | As needed | |
| TPL-20 | Vulnerability Advisory | As needed | |
| TPL-21 | Detection Rule Request | As needed | |
| TPL-22 | Detection Rule Documentation | Per rule | |
| TPL-23 | Tuning and Exception Request | As needed | |
| TPL-24 | Risk Acceptance | As needed | |
| TPL-25 | Change Request | Per change | |
| TPL-26 | Log Source Onboarding Request | Per source | |
| TPL-27 | SOC Tool Access Request | Per request | |
| TPL-28 | On-Call Log | Per on-call week | |
| TPL-29 | Tabletop Exercise Pack | Per exercise | |
| TPL-30 | Purple Team Test Report | Per exercise | |

## SOC Training (separate module)

SOC Training is its own part of the website, apart from the handbook and this kit. Each training module has short lessons, hands-on labs, a self-check quiz and links to the matching SOPs and playbooks. It lives in `docs/training/`.

| Module | Covers |
|---|---|
| T01 SOC Foundations | What a SOC does, tiers, alert lifecycle, TP/FP/BTP, severity, the daily rhythm, reports |
| T02 SIEM Platforms | Splunk (SPL), Microsoft Sentinel (KQL), Elastic and OpenSearch, IBM QRadar (AQL), Wazuh: architecture, search basics, the same 20 questions in every query language |
| T03 Log Sources Every Analyst Must Know | Windows event IDs, Sysmon, Linux auth and auditd, web server, firewall, proxy, DNS, email, identity provider, cloud audit logs |
| T04 Endpoint Security | EPP and NGAV, EDR, XDR, MDR, UEBA, NDR, DLP, HIPS, application allow-listing, device control, FIM, Sysmon, osquery, Wazuh agent, Velociraptor, MDM and UEM, CIS hardening |
| T05 Network Security Monitoring | Zeek, Suricata, NetFlow, PCAP basics, DNS and proxy analysis |
| T06 Email, Identity and Cloud Security | Mail flow and headers, Entra ID and Okta logs, AWS, Azure and Google Cloud audit logs |
| T07 Threat Intelligence | CTI lifecycle, intelligence requirements, Kill Chain, Diamond Model, MITRE ATT&CK, Pyramid of Pain, STIX and TAXII, MISP and OpenCTI, writing intel reports |
| T08 Threat Hunting | Hunting models (hypothesis, intel, analytics driven), PEAK and TaHiTI, data you need, hunt library by ATT&CK tactic, from hunt to detection |
| T09 Detection Engineering | Detection as code, Sigma, testing with Atomic Red Team, MITRE Caldera and Infection Monkey, tuning, ATT&CK coverage |
| T10 Incident Response | IR lifecycle in depth, containment decisions, communication, major incidents, tabletop practice |
| T11 DFIR | Windows, Linux, memory, network, cloud and email forensics, timelines, KAPE, Velociraptor, Volatility, Plaso, chain of custody |
| T12 Malware Analysis Basics | Safe lab, static and dynamic triage, sandboxes, YARA |
| T13 SOAR and Automation | What to automate, enrichment, case creation, approvals, n8n and Shuffle examples |
| T14 SOC Management | KPIs, staffing and shifts, reporting to management, maturity, budget |
| T15 Career and Interviews | L1 to L3 skill paths, certifications, interview question bank with model answers |
