# Changelog

All notable changes to The Defensive Mind. Newest first.

## [0.7.0], 2026-11-05

- Detection engineering completed: testing and tuning, coverage mapping (MITRE ATT&CK)
- Threat intelligence completed: IOC management (block vs watch, confidence, expiry, sharing)

## [0.6.0], 2026-11-05

- Security Policies section complete: index, policy framework, password and MFA, acceptable use and endpoint, access control, incident reporting, employee security guide (7 pages, as adaptable templates)

## [0.5.0], 2026-11-05

- Automation and SOAR section complete: index, SOAR principles, automation catalog, alert fatigue and notifications, case deduplication (5 pages)

## [0.4.0], 2026-11-05

- Build a SOC section complete: index, roadmap, operating model, team and roles, technology stack, log source priorities, use case prioritization, maturity model, budget and staffing (9 pages)

## [0.3.0], 2026-11-05

- Playbooks section: eight new playbooks (BEC, malware and infostealer, ransomware, web application attack, data exfiltration, insider threat, DDoS, cloud account compromise), each with queries for Splunk, Sentinel, Elastic, QRadar and Wazuh plus osquery and YARA where useful
- Playbook IDs aligned with the kit catalogue (account compromise is now PB-03, credential leak PB-05)
- SOC Document Kit: 12 playbooks as Word documents (33 documents in total), generated from the site pages by `soc-kit/from_site.py`

## [0.2.0], 2026-11-05

- Daily operations section complete: shift handover, case management, alert tuning, metrics and KPIs, threat hunting (with osquery, YARA and Sigma)
- SOC Document Kit: 21 Word documents (SOP-01 to SOP-10, TPL-01 to TPL-11) and the full catalogue of 130
- SOC Training section with the 15-module plan
- IBM QRadar AQL added to the query languages
- Incident response section complete: lifecycle, classification, escalation and communication, evidence handling, post-incident review, tabletop exercises
- Plan for modern and AI-driven SOC content (T16 to T18, SOP-51 to 64, PB-41 to 46)

## [0.1.0], 2026-11-04

First public preview. The handbook grows section by section; see the [roadmap](ROADMAP.md).

- Start Here: what a SOC is, how to use the handbook, career paths, glossary
- Field guide for L1 and L2 analysts
- Daily operations: daily routine, alert triage, severity and SLA
- Playbooks: phishing, account compromise, credential leak (dark web), brute force, plus the playbook template
- Detection engineering: detection lifecycle, writing good detections, Sigma primer and 10 Sigma rules
- Threat intelligence: TI lifecycle, dark web and credential monitoring, external attack surface management
- Templates: incident report, post-incident review, shift handover, monthly SOC report, detection request, risk acceptance, tabletop exercise, log source onboarding, change request
- MkDocs Material site with search and dark mode, published to GitHub Pages
- Licenses: CC BY 4.0 for content, MIT for code and rules
