# A Day as an L3 Analyst / Hunter / Detection Engineer

L3 is where the SOC stops only reacting and starts getting ahead. You lead the hard incidents, hunt for what the rules missed, and turn every lesson into a new detection. Less queue, more depth.

!!! abstract "At a glance"
    - Audience: L3 analysts, threat hunters, detection engineers, senior L2s stepping up
    - Time to read: 30 minutes
    - Outcome: you can run a hunt, take a detection from idea to tested rule, triage a malware sample safely, and run a purple-team test

## The day (less fixed than L1 and L2)

L3 work is project work, not a queue. A typical day splits roughly:

| Block | Work |
|---|---|
| Morning | Lead or support any live serious incident; the SOC's hardest open case is yours |
| Mid-day | Detection engineering: build, test and tune rules from gaps, hunts and incidents |
| Afternoon | A planned hunt, or malware and artefact analysis, or a purple-team test |
| Ongoing | Mentor L1 and L2, review their hard cases, improve the team's method |

!!! tip "Protect the deep-work time"
    L3 value comes from uninterrupted depth: a hunt, a detection, an analysis. If you spend all day in the alert queue, the SOC loses its ability to get ahead of attackers. Guard a block of focus time every day.

## Running a hunt

A hunt looks for attackers no rule has caught. It is driven by a hypothesis, not by an alert.

```text
Hypothesis -> gather the data -> search for the pattern
  -> investigate hits -> conclude (found / not found / inconclusive)
  -> if useful signal, turn it into a detection -> record the hunt
```

1. **Form a hypothesis.** Specific and testable: "An attacker is using scheduled tasks for persistence on our servers", not "find evil".
2. **Pick the data.** Which log source would show it (process creation, 4698 scheduled task, EDR).
3. **Search for the pattern**, widely at first, then narrow.
4. **Investigate the hits.** Most will be benign; understand why, that is how you learn normal.
5. **Conclude** honestly: found something, found nothing, or could not tell (often a logging gap).
6. **Convert** any reliable signal into a detection ([Testing and tuning](../05-detection-engineering/testing-and-tuning.md)).
7. **Record the hunt**, even a negative one. "We looked and found nothing" is a real result and saves repeating it.

See [Threat hunting](../02-daily-operations/threat-hunting.md) for a hunt library and more queries.

### Example hunt: persistence through scheduled tasks

=== "Microsoft Sentinel KQL"

    ```kql
    DeviceProcessEvents
    | where Timestamp > ago(14d)
    | where FileName =~ "schtasks.exe" and ProcessCommandLine has "/create"
    | where ProcessCommandLine has_any ("\\Temp\\","\\AppData\\","powershell","-enc","http")
    | project Timestamp, DeviceName, AccountName, ProcessCommandLine
    ```

=== "Splunk SPL"

    ```spl
    index=sysmon EventCode=1 Image="*\\schtasks.exe" CommandLine="*/create*"
      (CommandLine="*\\Temp\\*" OR CommandLine="*\\AppData\\*" OR CommandLine="*powershell*" OR CommandLine="*-enc*")
    | table _time host user CommandLine
    ```

=== "Wazuh"

    ```text
    data.win.eventdata.image:*schtasks.exe and data.win.eventdata.commandLine:(*\/create* and (*Temp* or *AppData* or *powershell* or *-enc*))
    ```

## Detection engineering end to end

Turning a gap or hunt into a rule analysts trust. The full method is in [Detection engineering](../05-detection-engineering/index.md); the L3 flow:

- [ ] Write the logic to match the behaviour, not one indicator.
- [ ] Test it fires on the real thing (Atomic Red Team, sample logs) on a test host.
- [ ] Run it log-only against real traffic for two weeks; count false positives.
- [ ] Tune the logic to be precise; avoid broad exclusions.
- [ ] Set severity, write the alert text and the runbook step.
- [ ] Map it to ATT&CK; commit it to the detection repo with a review date.

## Malware and artefact triage (basics, know your limits)

When a suspicious file turns up, L3 does safe first-level triage, not full reverse engineering.

| Safe | Not without the right setup and authority |
|---|---|
| Hash lookup (do not upload confidential files) | Running the sample outside an isolated sandbox |
| Static look: strings, file type, signatures | Detonating on a networked machine |
| Detonate in an isolated sandbox you control | Analysis that could tip off the attacker |
| Extract IOCs (domains, IPs, mutexes) for hunting | Anything likely to reach court, without forensics process |

!!! danger "Never run a sample on a normal machine or a networked one"
    Malware analysis happens in an isolated, disposable sandbox with no path to production or the internet you care about. Running a sample "just to see" on your workstation is how an incident responder becomes patient zero. If you do not have a safe sandbox, do static analysis and hash lookups only.

Extract what helps the SOC: file hash, contacted domains and IPs, persistence it sets, and the behaviour to detect. Feed those into hunts and detections.

## Purple teaming

Purple teaming is running real attacker techniques (red) while the SOC watches (blue), to prove detections work and find gaps.

- [ ] Pick techniques that matter to your risk (from your ATT&CK coverage gaps).
- [ ] Run them on test systems with Atomic Red Team, MITRE Caldera, or Infection Monkey.
- [ ] For each: record the expected alert, the actual result (fired, logged only, not seen), and the fix.
- [ ] Turn every "not seen" into a detection or a logging fix.
- [ ] Repeat on a schedule; coverage decays.

This is the fastest honest test of whether your SOC can actually see attacks, not just whether it owns tools.

## Mentoring is part of the job

L3 lifts the whole team. Review L1 and L2's hard cases to teach, not to grade. Share hunts and detections so knowledge does not live in one head. A SOC where only one person can hunt or build detections is fragile.

## 6 to 12 month growth

- [ ] Own a detection coverage area and measurably improve it.
- [ ] Run regular hunts and build a hunt library.
- [ ] Lead a purple-team exercise end to end.
- [ ] Specialise: cloud detection, forensics, malware, or detection-as-code pipelines.
- [ ] Mentor an L2 toward L3.

## Related pages

- [Threat hunting](../02-daily-operations/threat-hunting.md)
- [Detection engineering](../05-detection-engineering/index.md)
- [Testing and tuning](../05-detection-engineering/testing-and-tuning.md)
- [Coverage mapping](../05-detection-engineering/coverage-mapping.md)
- [Evidence handling](../03-incident-response/evidence-handling.md)
