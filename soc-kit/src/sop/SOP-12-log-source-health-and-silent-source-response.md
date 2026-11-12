---
id: SOP-12
title: Log Source Health and Silent Source Response
owner: SOC Engineer
audience: SOC analysts, SOC engineers
review: Every 12 months
summary: How to notice when an important log source goes quiet and what to do about it. A silent source is an invisible blind spot, and attackers stop logging on purpose.
---
## 1. Purpose

A log source that stops sending data is the most dangerous kind of gap, because everyone assumes it is working. This procedure makes sure the SOC detects silence quickly and responds, rather than discovering weeks later that it was blind.

> WARNING: One of the first things a capable attacker does is disable or clear logging. A silent critical source is not just an operational glitch; treat it as a possible security event until proven otherwise.

## 2. Scope

All important log sources feeding the SIEM, especially identity, endpoints, perimeter and cloud.

## 3. Detecting silence

- [ ] Each important source has an expected minimum rate of events.
- [ ] A detection fires when a source sends nothing (or far below normal) for longer than its threshold.
- [ ] The threshold suits the source: minutes for a busy source, hours for a quiet one.

## 4. Procedure when a source goes silent

### 4.1 Triage

1. Confirm the source is really silent, not just low activity (a weekend, a holiday).
2. Check how long it has been silent and when it last sent data.
3. Check whether a change (maintenance, a deployment) explains it; look at the change log (SOP-17).

### 4.2 Decide

| Finding | Action |
|---|---|
| Known maintenance or planned change | Note it, set a time to re-check, close |
| A broken connector, agent or pipeline | Raise an operations ticket to fix; restore collection |
| No benign explanation, on a critical source | Treat as a possible security event: could an attacker have disabled it? Escalate |

> NOTE: Ask "could this silence be the attacker?" before assuming it is a glitch, especially for endpoint, identity and cloud logging. A disabled EDR agent or a stopped cloud trail can be the first sign of an intrusion.

### 4.3 Restore and confirm

1. Fix the cause (restart the agent, repair the pipeline, re-enable logging).
2. Confirm data is flowing again and complete.
3. Check for a gap: did you lose events, and does that gap need investigating?

## 5. Done when

- [ ] The source is sending data again, or the silence is explained and accepted.
- [ ] Any security concern has been escalated and worked.
- [ ] Any data gap has been assessed.

## 6. Records

Record each silent-source event: the source, how long, the cause, the action, and whether it was a security concern. Repeated silence on the same source is a reliability problem to fix at the root.

## 7. Review

Reviewed every 12 months.
