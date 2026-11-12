---
id: SOP-18
title: EDR and XDR Alert Handling
owner: SOC Lead
audience: L1 and L2 analysts
review: Every 12 months
summary: How to triage and act on an endpoint detection and response (EDR) or extended detection and response (XDR) alert, including the one question that decides everything: did it actually run?
---
## 1. Purpose

Most attacks touch an endpoint, so EDR and XDR alerts are a large part of the queue. This procedure makes triage consistent: confirm whether the threat executed, scope it, and respond, without panicking over every blocked detection or missing a real one.

## 2. Scope

All EDR and XDR alerts on covered endpoints for [ORGANISATION].

## 3. The first question: blocked or executed?

The action the tool took decides the severity.

| Action | Meaning | First move |
|---|---|---|
| Blocked or quarantined | Stopped before it ran | Lower priority; still check how it arrived |
| Detected or allowed | It may have run | Treat as executed until proven otherwise |

> NOTE: "Detected" is not "stopped". If the tool only detected, assume the threat executed and look for what it did (child processes, network connections, file writes) after the alert time.

## 4. Procedure

### 4.1 Triage (first 15 minutes)

- [ ] Read the detection: what, where, and the action taken.
- [ ] Confirm whether it executed (process tree, connections, file writes after the alert).
- [ ] Identify the host and user; admin, developer, finance or executive raises severity.
- [ ] Check the same hash or indicator across the fleet.
- [ ] Decide the verdict and severity (GOV-03).

### 4.2 Investigate

- [ ] Follow the process tree: parent, children, what they did.
- [ ] Note network connections and extract indicators (hashes, domains, IPs).
- [ ] Determine how it arrived (download, email, USB, lateral movement).
- [ ] Check for persistence (autoruns, scheduled tasks, services).

### 4.3 Respond

| Situation | Action | Reference |
|---|---|---|
| Confirmed malware that executed | Isolate the host | SOP-19 |
| Infostealer behaviour | Isolate and treat credentials as stolen | Malware playbook |
| Spreading or ransomware behaviour | Escalate to P1, open the ransomware playbook | Ransomware playbook |
| Blocked, single host, no execution | Clean up, add indicators, close with a note | - |

### 4.4 Close

Record the verdict, what executed, the indicators, the response, and any detection or tuning follow-up.

## 5. Common false positives

Admin tools flagged as hacktools, potentially unwanted programs, security tool updates, legitimate scripts. Confirm with context before closing, and tune repeat false positives (SOP-10).

## 6. Review

Reviewed every 12 months.
