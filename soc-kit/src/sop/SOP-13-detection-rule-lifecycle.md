---
id: SOP-13
title: Detection Rule Lifecycle
owner: Detection Engineer
audience: Detection engineers, L2 and L3 analysts
review: Every 12 months
summary: How a detection goes from an idea to a tested, owned, version-controlled rule in production, and how it is reviewed and retired. Detections are code and are managed like code.
---
## 1. Purpose

This procedure manages detections as code, so every rule is tested, owned, documented and reversible. It stops the two failures: a rule that never fires because nobody tested it, and a rule that screams on normal traffic because nobody tuned it.

## 2. Scope

All detections the SOC of [ORGANISATION] owns, in the SIEM, EDR and other tools.

## 3. The lifecycle

```
Request -> Draft -> Test (fires and stays quiet) -> Review -> Deploy (log-only first)
  -> Promote to alerting -> Monitor and tune -> Review on schedule -> Retire
```

## 4. Procedure

### 4.1 Request

1. Capture the idea: the behaviour to detect, where it comes from (a gap, a hunt, an incident, intel), and the related playbook. Use the Detection Rule Request template.
2. Confirm the log source exists; a detection with no data is a logging request, not a detection.

### 4.2 Draft

- [ ] Write the logic to match the behaviour, not a single indicator.
- [ ] Prefer a portable format (Sigma) where possible, then convert.
- [ ] Set a draft severity and write the alert text an analyst will read.
- [ ] Map it to MITRE ATT&CK.

### 4.3 Test

- [ ] True positive: confirm it fires on the real behaviour (Atomic Red Team or sample logs, on a test host). See SOP-14.
- [ ] False positive: run it log-only against real traffic for [two weeks]; count and understand the hits.

### 4.4 Review and deploy

1. Have a second person review the logic, severity and alert text.
2. Deploy log-only first; confirm the false positive rate is acceptable.
3. Promote to alerting only when it passes both tests.
4. Write the runbook step that tells the analyst what to do when it fires.

### 4.5 Monitor, tune, review

- [ ] Watch it after go-live; tune the logic, not the scope, to cut noise (SOP-10).
- [ ] Review every rule on a schedule; rules rot as systems change.
- [ ] Track rules that never fire (broken or the attack never happened) and rules that fire constantly (tuning backlog).

### 4.6 Retire

Retire a rule that is superseded, permanently noisy with no value, or no longer relevant. Record why, so the coverage gap it leaves is a decision, not an accident.

## 5. Manage detections as code

- [ ] Keep rules in version control, with review before changes go live.
- [ ] Record each rule's owner, ATT&CK mapping, severity, and review date.
- [ ] Test changes before production.

## 6. Records

Every rule has a history: created, tested, deployed, tuned, reviewed, retired, with who and when.

## 7. Review

Reviewed every 12 months.
