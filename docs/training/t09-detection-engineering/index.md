# T09: Detection Engineering

Turning attacker behaviour into tested, owned, version-controlled detections that analysts trust. This module teaches detection as code: write, convert, test, tune and track.

!!! abstract "At a glance"
    - Level: L2 to L3
    - Time: 8 to 10 hours with labs
    - Outcome: you can take a detection from idea to a tested rule mapped to ATT&CK

## Learning objectives

- [ ] Write a Sigma rule and convert it to any SIEM.
- [ ] Write a basic YARA rule for files.
- [ ] Test a rule two ways: it fires on the attack, and it stays quiet on normal traffic.
- [ ] Tune a rule without creating a blind spot.
- [ ] Manage detections as code and map coverage to ATT&CK.

## Lessons

1. **Detection as code.** Rules in version control, reviewed, tested, versioned, like software.
2. **Sigma.** The portable rule format; writing a rule and converting it to SPL, KQL, Elastic, QRadar and Wazuh.
3. **YARA.** Writing a rule to identify a file or malware family from its contents.
4. **Testing.** True-positive testing with Atomic Red Team and Caldera; false-positive testing in log-only mode.
5. **Tuning.** Precise logic over broad exclusions; every exclusion documented with a review date.
6. **Coverage.** Mapping rules to ATT&CK and reading the heatmap honestly.

## Lab

- [ ] Write a Sigma rule for a behaviour (for example, a new local admin).
- [ ] Convert it to your SIEM with a Sigma converter and run it.
- [ ] Test it fires using Atomic Red Team on a test host.
- [ ] Run it log-only for a while; count false positives and tune.
- [ ] Commit it to a git repo with ATT&CK tags and a review date.

### A simple Sigma rule structure

```yaml
title: Local account added to Administrators
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4732
    TargetUserName: 'Administrators'
  condition: selection
tags:
  - attack.t1098
  - attack.t1136.001
level: medium
```

## Self-check

1. Why keep detections in version control?
2. What are the two tests every rule must pass before going live?
3. Why prefer better logic over a broad exclusion when tuning?

??? note "Answers"
    1. So changes are reviewed, tested, tracked and reversible, and so coverage is visible; a detection is powerful code and deserves the same discipline.
    2. It fires on the real attack (true positive), and it stays quiet on normal traffic (false positive), proven in log-only mode.
    3. A broad exclusion is a hole cut in the detection and an easy blind spot; precise logic reduces noise while still catching the attack.

## Links to the handbook and kit

- [Detection engineering](../../05-detection-engineering/index.md)
- [Testing and tuning](../../05-detection-engineering/testing-and-tuning.md)
- [Coverage mapping](../../05-detection-engineering/coverage-mapping.md)

## Next module

[T10 Incident Response](../t10-incident-response/index.md).
