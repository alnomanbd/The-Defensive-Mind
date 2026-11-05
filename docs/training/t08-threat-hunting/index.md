# T08: Threat Hunting

Hunting is looking for the attacker no rule has caught, driven by a hypothesis rather than an alert. This module teaches how to form a hypothesis, hunt with free tools, and turn every useful hunt into a detection.

!!! abstract "At a glance"
    - Level: L3
    - Time: 8 to 10 hours with labs
    - Outcome: you can run a structured hunt and convert its findings into detections

## Learning objectives

- [ ] Form a specific, testable hunt hypothesis.
- [ ] Run intel-driven, analytics-driven and hypothesis-driven hunts.
- [ ] Hunt live with osquery and Velociraptor, and sweep files with YARA.
- [ ] Use the PEAK and TaHiTI hunting models.
- [ ] Turn a hunt into a detection and record it.

## Lessons

1. **What hunting is.** Proactive, hypothesis-led search, not alert triage; it assumes something got through.
2. **Types of hunt.** Intel-driven (from a report), analytics-driven (from anomalies), hypothesis-driven (from how attackers behave).
3. **Forming a hypothesis.** Specific and testable: "attackers are using scheduled tasks for persistence on our servers", not "find evil".
4. **Live hunting.** osquery across the fleet, Velociraptor hunts, YARA sweeps for files.
5. **Models.** PEAK (prepare, execute, act with knowledge) and TaHiTI (targeted hunting integrating threat intelligence) as repeatable structures.
6. **A hunt library.** Organising hunts by ATT&CK tactic so you cover the ground methodically.
7. **Closing the loop.** Every reliable hunt finding becomes a detection; every hunt is recorded, even a negative one.

## Lab

- [ ] Pick a hypothesis (for example, persistence through new scheduled tasks).
- [ ] Decide the data source and write the hunt query (see [Threat hunting](../../02-daily-operations/threat-hunting.md)).
- [ ] Run it in your lab; investigate the hits and explain why each is benign or not.
- [ ] Write the result up as a hunt record, including a negative result if you found nothing.
- [ ] Convert one reliable signal into a Sigma rule and test it.

### Hunt drill: scheduled-task persistence

=== "Microsoft Sentinel KQL"

    ```kql
    DeviceProcessEvents
    | where Timestamp > ago(14d) and FileName =~ "schtasks.exe" and ProcessCommandLine has "/create"
    | where ProcessCommandLine has_any ("\\Temp\\","\\AppData\\","powershell","-enc")
    | project Timestamp, DeviceName, AccountName, ProcessCommandLine
    ```

=== "Splunk SPL"

    ```spl
    index=sysmon EventCode=1 Image="*\\schtasks.exe" CommandLine="*/create*"
      (CommandLine="*\\Temp\\*" OR CommandLine="*powershell*" OR CommandLine="*-enc*")
    | table _time host user CommandLine
    ```

## Self-check

1. What makes a good hunt hypothesis?
2. Why record a hunt that found nothing?
3. What should happen to a hunt that found a reliable signal?

??? note "Answers"
    1. It is specific and testable: it names a behaviour, a data source, and what a hit would look like.
    2. A negative result is real information: it tells you (and the next hunter) that you looked and found nothing, saves repeated effort, and may reveal a logging gap.
    3. Convert it into a tested detection so the SOC catches it automatically next time, and record the hunt.

## Links to the handbook and kit

- [Threat hunting](../../02-daily-operations/threat-hunting.md)
- [Detection engineering](../../05-detection-engineering/index.md)
- [L3 analyst field guide](../../field-guide/l3-analyst.md)

## Next module

[T09 Detection Engineering](../t09-detection-engineering/index.md).
