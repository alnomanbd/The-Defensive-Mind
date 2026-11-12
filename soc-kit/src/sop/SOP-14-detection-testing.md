---
id: SOP-14
title: Detection Testing with Atomic Red Team, MITRE Caldera and Infection Monkey
owner: Detection Engineer
audience: Detection engineers, L3 analysts
review: Every 12 months
summary: How to safely prove that a detection fires on the real attack, using controlled attack-simulation tools on test systems only.
---
## 1. Purpose

A detection you have not tested is a guess. This procedure runs real attacker techniques safely, so you know a rule actually fires, and so a green square on your coverage map means something.

> WARNING: These tools run real techniques. Run them only on isolated test systems you own, with authorisation, never on production or anyone else's machine. Know how to clean up after each test.

## 2. Scope

Testing detections and coverage for the SOC of [ORGANISATION], on test systems in an isolated lab.

## 3. The tools

| Tool | Use for | Scope |
|---|---|---|
| Atomic Red Team | Single ATT&CK techniques, quick detection checks | A single test host |
| MITRE Caldera | Chained adversary emulation with agents | An isolated test network |
| Infection Monkey | Lateral movement and segmentation testing | An isolated lab only |

## 4. Before testing

- [ ] Authorisation to run the test is recorded.
- [ ] The target is an isolated test system, with a snapshot to roll back.
- [ ] You know the expected alert and where it should appear.
- [ ] You know the cleanup steps.

## 5. Procedure

### 5.1 Single technique (Atomic Red Team)

1. Pick the technique that matches the detection (by ATT&CK ID).
2. Review what the test does before running it.
3. Run it on the test host.
4. Confirm whether the detection fired, logged only, or was not seen.
5. Clean up the test.

```
Invoke-AtomicTest T1059.001 -TestNumbers 1 -ShowDetailsBrief
Invoke-AtomicTest T1059.001 -TestNumbers 1
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
```

### 5.2 Chained emulation (Caldera) and lateral movement (Infection Monkey)

Use these for multi-step attacks and segmentation testing in an isolated network, when a single technique is not enough. Record the expected detections for each step.

## 6. Record the result

For each test, record:

| Field | Example |
|---|---|
| Technique | T1059.001 PowerShell |
| Expected alert | "PowerShell encoded command" |
| Actual result | Fired / logged only / not seen |
| Fix | Detection added or tuned, or logging gap raised |

## 7. Close the loop

- [ ] "Not seen" becomes a detection to build or a logging gap to fix.
- [ ] "Logged only" becomes an alerting rule if the behaviour warrants it.
- [ ] Update the ATT&CK coverage map with what you proved.
- [ ] Run tests on a schedule; coverage decays.

## 8. Review

Reviewed every 12 months.
