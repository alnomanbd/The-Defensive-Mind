# Testing and Tuning

How to prove a detection works before it goes live, and how to keep it useful afterwards. A rule that never fires is useless; a rule that fires constantly on normal traffic is worse than useless, because it buries the real alerts. Testing proves it catches the attack; tuning keeps it quiet on everything else.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC analysts L2/L3
    - Time to read: 12 minutes
    - Outcome: a method to test a new rule two ways, and a tuning loop that cuts noise without creating blind spots

## Every rule is tested two ways

A detection must pass both tests before it pages anyone.

| Test | Question | How |
|---|---|---|
| True positive | Does it fire on the real attack? | Reproduce the behaviour safely and confirm the alert |
| False positive | Does it stay quiet on normal activity? | Run it in log-only mode against real traffic for a period |

A rule that passes one but not the other is not ready. Catching the attack while screaming on normal traffic is as bad as silence.

## Test 1: does it fire? (true positive)

Reproduce the behaviour the rule is meant to catch, in a safe place, and confirm the alert appears.

| Method | Use for | Notes |
|---|---|---|
| Atomic Red Team | Single ATT&CK techniques | Small, safe tests mapped to technique IDs; run on a test host only |
| MITRE Caldera | Chained adversary emulation | For multi-step attacks and testing a sequence of detections |
| Sample logs through the pipeline | Any rule, no live action | Feed a known-bad log line through test tooling (for example `wazuh-logtest`, Splunk `| makeresults`, a Sigma unit test) |
| Your own lab | Behaviours you can safely run | Spin up the condition (a new admin, an encoded command) on a test box |

!!! warning "Test on a test host, never in production"
    Atomic tests and emulation run real techniques. Run them only on isolated test systems you own, with permission, never on production or on someone else's machine. Know how to clean up after each test.

Example: testing a "PowerShell encoded command" rule with Atomic Red Team on a test host:

```powershell
Invoke-AtomicTest T1059.001 -TestNumbers 1 -ShowDetailsBrief
Invoke-AtomicTest T1059.001 -TestNumbers 1
# then confirm the alert fired, and clean up:
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
```

Record for each test: the technique, the expected alert, and the actual result (fired, logged only, or not seen).

## Test 2: does it stay quiet? (false positive)

Before a rule pages anyone, run it in **log-only mode** against real traffic and count how often it would have fired on normal activity.

- [ ] Deploy the rule so it logs but does not alert or notify.
- [ ] Let it run against real traffic for at least `[two weeks]`, covering a normal business cycle (including month-end, patching, backups).
- [ ] Count the hits and look at what caused them.
- [ ] If almost all hits are normal activity, tune before going live.
- [ ] Only promote the rule to alerting when the false positive rate is acceptable.

A rule that would have fired 400 times in two weeks, all benign, is not ready to wake anyone.

## Tuning: cut noise without going blind

Tuning is reducing false positives while keeping the detection. The danger is tuning so hard that you blind yourself. Every tuning change is a small risk decision, so record it.

### Ways to tune, best to worst

| Method | What it does | Risk |
|---|---|---|
| Make the logic more precise | Add conditions that match the attack better (parent process, command pattern, outcome) | Low, this is real improvement |
| Exclude a specific known-good source | Allowlist your own scanner, a named service account, a backup job | Low, if specific and documented |
| Raise a threshold | Fire on 10 failures, not 3 | Medium, you may miss slow attacks |
| Broad exclusion | Exclude a whole subnet, user group or event type | High, easy to create a blind spot |
| Lower severity | Keep the signal but stop it paging | Low, good for noisy-but-useful rules |

Prefer better logic over exclusions. An exclusion is a hole you cut in the detection; make it as small and specific as possible.

!!! danger "Tuning can become a blind spot"
    "We tuned that out" is how attackers hide in plain sight. If you exclude the finance team's subnet to stop noise, you have also stopped detecting an attack from the finance team's subnet. Tune the logic to be precise, not the scope to be blind. Every exclusion needs a reason, an owner and a review date.

### The tuning loop

```text
Review noisiest rules weekly -> pick the worst
  -> understand the false positives (what is really causing them)
  -> tune the logic, or add a specific, documented exclusion
  -> re-test it still catches the attack
  -> record the change in version control
  -> repeat
```

- [ ] Review your top 10 noisiest rules every week.
- [ ] Fix the logic where you can; exclude narrowly where you must.
- [ ] After any exclusion, re-run the true-positive test to prove the rule still catches the attack.
- [ ] Record every change (what, why, who, when) in the rule's version history.

## Document every tuning change

A tuning change is a change to what you can see. Treat it like a code change ([Detection lifecycle](detection-lifecycle.md)).

| Record | Why |
|---|---|
| What changed and why | So the next person understands the blind spot you accepted |
| Who approved it | Tuning that reduces coverage needs an owner |
| What false positive it addressed | So you can tell if it comes back |
| A review date | So temporary exclusions do not become permanent |

## Watch for rule rot

Rules decay. Systems change, a noisy source appears, or an attacker learns to avoid the pattern. A rule that was perfect a year ago may now be silent or screaming.

- [ ] Review every rule on a schedule (for example yearly), not just when it misbehaves.
- [ ] Track rules that have never fired: either the attack never happened, or the rule is broken. Find out which.
- [ ] Track rules that fire constantly: a tuning backlog.
- [ ] Re-test important rules after major changes to systems or logging.

## Related pages

- [Detection lifecycle](detection-lifecycle.md)
- [Writing good detections](writing-good-detections.md)
- [Coverage mapping](coverage-mapping.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
- [Tabletop exercises](../03-incident-response/tabletop-exercises.md)
