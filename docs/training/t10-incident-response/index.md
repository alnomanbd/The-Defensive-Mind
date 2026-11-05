# T10: Incident Response

What to do once an alert is a confirmed incident: classify, contain, eradicate, recover and learn, under pressure and with the right people. This module turns the incident response method into practised skill.

!!! abstract "At a glance"
    - Level: L2 to L3
    - Time: 6 to 8 hours with labs
    - Outcome: you can run an incident through its lifecycle and make sound containment decisions

## Learning objectives

- [ ] Run the incident response lifecycle: prepare, identify, contain, eradicate, recover, learn.
- [ ] Classify an incident and set its severity.
- [ ] Make containment decisions that stop the attack without destroying evidence.
- [ ] Communicate during an incident, with the right rhythm and the right people.
- [ ] Run and take part in a tabletop exercise.

## Lessons

1. **The lifecycle.** Each phase, what "done" looks like, and why evidence is collected throughout.
2. **Classification and severity.** What type of incident, how bad, and who that pulls in.
3. **Containment decisions.** Isolate vs power off, who approves business-affecting action, how to contain without losing evidence.
4. **Eradication and recovery.** Removing the cause, rebuilding from known-good, recovering in priority order, watching for recurrence.
5. **Communication.** The escalation matrix, update rhythm, out-of-band channels, legal clocks.
6. **Practice.** Tabletop exercises and why practising before the real thing matters.

## Lab

- [ ] Take one [walkthrough](../../field-guide/walkthroughs/index.md) and run it end to end: triage, scope, contain, recover, lessons.
- [ ] For a ransomware scenario, write the containment order and who approves each step.
- [ ] Draft a first-notice message to leadership (see the [templates](../../03-incident-response/escalation-and-communication.md)).
- [ ] Run a short tabletop with a colleague using a ready scenario.

## Self-check

1. Why collect evidence throughout, not just at the end?
2. When would you isolate a host rather than power it off?
3. Why does communication need a fixed rhythm during a P1?

??? note "Answers"
    1. Because evidence disappears (memory on reboot, logs on rotation) and the timeline is built as you go; collecting only at the end loses the story.
    2. Almost always: isolation preserves memory and allows remote response while cutting the network. Power off only if isolation is impossible and damage is active.
    3. So leadership is not surprised, teams do not duplicate work, and decisions are made on time; silence during a P1 breeds panic and bad calls.

## Links to the handbook and kit

- [IR lifecycle](../../03-incident-response/ir-lifecycle.md)
- [Escalation and communication](../../03-incident-response/escalation-and-communication.md)
- [Tabletop exercises](../../03-incident-response/tabletop-exercises.md)
- [Playbooks](../../04-playbooks/index.md)

## Next module

[T11 DFIR](../t11-dfir/index.md).
