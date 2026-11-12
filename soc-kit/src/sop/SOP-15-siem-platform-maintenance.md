---
id: SOP-15
title: SIEM Platform Maintenance
owner: SOC Engineer
audience: SOC engineers, platform team
review: Every 12 months
summary: How to keep the SIEM healthy: patching, retention, backup, capacity and its own security. A SIEM that falls over or fills up blinds the whole SOC.
---
## 1. Purpose

The SIEM is the heart of the SOC. If it stops ingesting, fills its disk, or is compromised, the SOC goes blind. This procedure keeps the platform healthy, patched, backed up and secured.

> WARNING: The SIEM holds logs from across the organisation and has broad access. Treat it as a crown jewel: patch it, protect it, restrict access to it, and monitor it like any high-value target.

## 2. Scope

The SIEM and its supporting components (collectors, indexers, dashboards, pipelines) for [ORGANISATION].

## 3. Routine checks

### Daily (part of the health check, SOP-01)

- [ ] Core services running (manager, indexer, dashboard, collectors).
- [ ] Ingest is flowing at a normal rate; no flat line.
- [ ] Disk free above the threshold ([20 percent]).
- [ ] No critical platform errors overnight.

### Weekly

- [ ] Review ingest volume trend; a sudden rise is a misconfiguration or an attack.
- [ ] Check index or storage health.
- [ ] Review any failed collectors or pipelines.

### Monthly

- [ ] Apply platform and security updates in a controlled window (see change management, SOP-17).
- [ ] Review retention against policy (GOV-07); archive or expire as planned.
- [ ] Test that a backup restores.
- [ ] Review capacity against growth.

## 4. Patching

1. Track SIEM and component versions and known vulnerabilities.
2. Apply security updates promptly, following change management.
3. Test in a non-production or staged way where possible before production.
4. Have a rollback plan; the SIEM going down is itself an incident.

> NOTE: A SIEM is also software with vulnerabilities. Keep it current. An unpatched, internet-exposed security platform is a high-value target, and its compromise hands an attacker your logs, your detections and broad access.

## 5. Retention and capacity

- [ ] Keep hot (searchable) and archive tiers per GOV-07.
- [ ] Watch disk and index growth; plan capacity ahead of need.
- [ ] Control volume at the source (SOP-11) rather than only adding storage.

## 6. Backup and recovery

- [ ] Back up configuration, detections, and the data that must survive a failure.
- [ ] Store backups so a compromise of the SIEM cannot destroy them.
- [ ] Test a restore regularly; an untested backup is a hope, not a plan.

## 7. Securing the platform

- [ ] Restrict and review access to the SIEM and its admin functions.
- [ ] Change default credentials; never leave built-in accounts on defaults.
- [ ] Expose management interfaces only to trusted networks, not the internet.
- [ ] Monitor the SIEM itself for configuration change, new processes and unusual access.

## 8. Review

Reviewed every 12 months.
