# T01: SOC Foundations

The first module. What a SOC is, how the work flows, and the words and judgements every analyst uses from day one. Short theory, then you practise on real alerts.

!!! abstract "At a glance"
    - Level: L1
    - Time: 4 to 6 hours with labs
    - Outcome: you can take an alert, decide if it is real, set a severity, and write it up the way a SOC expects

## Learning objectives

- [ ] Explain what a SOC does and how the tiers (L1, L2, L3, manager) hand work to each other.
- [ ] Walk an alert through its full lifecycle, from detection to closure.
- [ ] Tell a true positive from a false positive, and know the in-between verdicts.
- [ ] Set a severity from impact and urgency, and know when to escalate.
- [ ] Write a case note and an escalation that the next person can act on.
- [ ] Name the daily rhythm and the reports a SOC produces.

## Lessons

1. **What a SOC is.** Not a room with screens: a capability of people, process and technology that detects, investigates, responds and improves.
2. **The tiers.** What L1, L2, L3 and the manager each own, and that tiers are about work, not worth.
3. **The alert lifecycle.** Detection, triage, investigation, response, closure, and why every step is recorded.
4. **Verdicts.** True positive, false positive, benign true positive, and undetermined, with examples of each.
5. **Severity.** Scoring impact and urgency, the P1 to P4 scale, and automatic overrides.
6. **Notes and escalations.** The one rule: if it is not in the ticket, it did not happen. How to write so the next analyst can act.
7. **The daily rhythm.** Health check, triage rounds, handover, and the reports a SOC produces daily, weekly and monthly.

## Lab

- [ ] Stand up a free SIEM (Wazuh single-node) and send it logs from one machine.
- [ ] Find the alert view and open three alerts.
- [ ] For each: write a one-line verdict (true or false positive) and why.
- [ ] Set a severity for each using impact and urgency.
- [ ] Write one as an escalation note another analyst could pick up.

## Self-check

1. What is the difference between a false positive and a benign true positive?
2. An alert shows blocked internet scanning from one IP. What severity, and why?
3. Why is "if it is not in the ticket, it did not happen" a rule and not just advice?

??? note "Answers"
    1. A false positive is not real activity at all; a benign true positive is real activity that is not malicious (your own scanner, a maintenance job).
    2. Low (P4): it is an attempt that was blocked, with no impact and no sign of success. Confirm the block worked and close.
    3. Because the SOC runs on handover and review. An undocumented check cannot be trusted, repeated, or learned from, and in an incident the timeline is the evidence.

## Links to the handbook and kit

- [Daily routine](../../02-daily-operations/daily-routine.md), [Alert triage](../../02-daily-operations/alert-triage.md), [Severity and SLA](../../02-daily-operations/severity-and-sla.md)
- [L1 analyst field guide](../../field-guide/l1-analyst.md)
- SOC Document Kit: the triage and severity SOPs on the [kit plan](../../soc-kit/index.md)

## Next module

[T02 SIEM Platforms](../t02-siem-platforms/index.md): the tools you will search every day.
