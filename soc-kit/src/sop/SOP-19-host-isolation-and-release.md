---
id: SOP-19
title: Host Isolation and Release
owner: SOC Lead
audience: L1, L2 and L3 analysts
review: Every 12 months
summary: How to isolate a host to stop an attack spreading, what isolation does and does not do, who approves it, and how to safely release the host afterwards.
---
## 1. Purpose

Isolating a host cuts an attacker off while keeping the machine available for investigation. This procedure sets when to isolate, who approves it, and how to release safely, so isolation stops the threat without causing an unnecessary outage.

## 2. What isolation does

| Isolation does | Isolation does not |
|---|---|
| Cut the host's network so it cannot spread or reach command and control | Power the host off |
| Keep memory and running processes for analysis | Remove the malware |
| Usually allow the EDR and responders to still reach it | Fix the root cause |

> NOTE: Isolation keeps the machine powered on, which preserves memory (processes, keys, network state) for analysis. Power off only if isolation is impossible and damage is actively happening.

## 3. When to isolate

- [ ] Confirmed malware that executed on the host.
- [ ] Signs of hands-on attacker activity or lateral movement.
- [ ] Ransomware or wiper behaviour (isolate immediately).
- [ ] An infostealer that ran (to stop ongoing exfiltration).

## 4. Approvals

| Host | Approval |
|---|---|
| Laptop or workstation | Pre-authorised for the SOC on confirmed malware (GOV-04) |
| Server | SOC manager or system owner, because of the outage risk |
| A critical production system | System owner and incident lead; weigh outage against spread |

## 5. Procedure

### 5.1 Isolate

1. Confirm the reason and the approval needed (above).
2. Isolate the host through the EDR.
3. Record the time, the host, who approved it, and why, in the case.
4. Tell the user and the system owner that the host is isolated and why.

### 5.2 Investigate while isolated

Collect what you need (process tree, memory if required, indicators) before any rebuild. The host is contained but still available to you.

### 5.3 Release

Release only when the threat is removed and the host is safe. Before releasing:

- [ ] The malware and any persistence are removed, or the host is being rebuilt.
- [ ] You understand how it got in and that path is closed.
- [ ] The system owner agrees the host is ready.

1. Release the host from isolation through the EDR.
2. Confirm it behaves normally and the EDR is healthy.
3. Monitor it closely for [a period] for any return of the activity.
4. Record the release time and who approved it.

> WARNING: Do not release a host just to restore service before the threat is removed. A host released with the attacker still on it re-infects the network. If service is urgent and the host is not clean, rebuild from a known-good image rather than releasing the compromised one.

## 6. Records

Record every isolation and release: host, time, reason, approver, what was found, and the outcome.

## 7. Review

Reviewed every 12 months.
