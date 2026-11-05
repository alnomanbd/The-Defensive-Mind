---
id: GOV-07
title: Log Management and Retention Policy
owner: SOC Manager
audience: SOC team, IT, platform and cloud teams
review: Every 12 months
summary: What logs are collected, how long they are kept, how they are protected, and who may access them. Logs are the SOC's evidence and its memory; this policy keeps them trustworthy and available.
---
## 1. Purpose

This policy sets how [ORGANISATION] collects, retains, protects and accesses security logs. Without reliable logs, the SOC cannot detect, investigate or prove what happened. Without protected logs, an attacker can erase their tracks.

## 2. Scope

All security-relevant logs from covered systems (GOV-01): identity, endpoints, network, cloud, email, applications, and the SOC's own tools.

## 3. What is collected

Log sources are onboarded by priority (identity and endpoints first). The priority and the key events per source are maintained by the SOC. A current list of onboarded sources and their owners is kept in [location].

- [ ] Each source has an owner and a documented purpose.
- [ ] Only security-relevant events are collected, to control cost and noise.
- [ ] Timestamps are normalised to one timezone ([UTC recommended]).

## 4. Retention

Keep logs long enough to investigate, meet legal duties, and detect slow attacks, without paying to store what you will never query.

| Tier | Typical retention | Purpose |
|---|---|---|
| Hot (fast search) | [30 to 90 days] | Active detection and investigation |
| Warm or archive | [6 to 12 months, or as required] | Retrospective investigation, legal duties |
| Legal hold | As long as required | Preserved for a specific case or law |

Set retention to meet [ORGANISATION]'s legal, regulatory and contractual duties; some sectors require longer. Record the required minimums in [location].

> NOTE: Attackers often operate for weeks before detection. If your hot retention is 30 days and the dwell time was 60, you cannot see how they got in. Balance cost against the ability to investigate real intrusions.

## 5. Protecting logs

Logs are evidence, so their integrity matters.

- [ ] Forward logs off the source promptly, so deleting a host's local logs does not lose them.
- [ ] Restrict who can alter or delete central logs; log and alert on attempts.
- [ ] Protect audit logging from being switched off; alert on StopLogging, DeleteTrail and equivalents.
- [ ] Monitor the SOC's own platform for tampering.

> WARNING: One of the first things a capable attacker does is clear or disable logs. A policy that does not protect and monitor the logging itself leaves a blind spot exactly where you most need to see.

## 6. Access to logs

Access to logs is limited to those who need it for security or operations, and is itself logged.

- [ ] SOC analysts: read access to security logs for investigation.
- [ ] Access to logs containing personal data follows the Privacy policy (GOV-10).
- [ ] Access is reviewed per the access control process.

## 7. Monitoring log health

A silent log source is an invisible blind spot. The SOC alerts when an important source stops sending data, per the Silent Source SOP.

## 8. Review

Reviewed every 12 months, and when sources, volumes or legal duties change.

**Approved by:** [role]. **Date:** [date]. **Next review:** [date].
