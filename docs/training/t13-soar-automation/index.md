# T13: SOAR and Automation

How to make a SOC do more with the people it has by automating the dull, repetitive work. This module teaches what to automate, what to keep human, and how to build safe workflows.

!!! abstract "At a glance"
    - Level: L2 to L3
    - Time: 6 to 8 hours with labs
    - Outcome: you can build enrichment and response workflows with human approval where it matters

## Learning objectives

- [ ] Decide what to automate and what to keep human.
- [ ] Build enrichment workflows (IP, domain, hash, user, host).
- [ ] Build case creation and routing.
- [ ] Add response actions with an approval step.
- [ ] Keep automation safe, logged and reversible.

## Lessons

1. **The golden rule.** Automate enrichment freely; automate action carefully. A wrong action at machine speed can be worse than the attack.
2. **What to automate.** Enrichment, grouping, routing, auto-closing tight benign patterns; keep judgement human.
3. **The patterns.** Automate and inform, automate with approval, fully automate (only reversible, low-risk, measured actions).
4. **Building workflows.** With a free tool (n8n, Shuffle): trigger on an alert, enrich, open a case, notify.
5. **Response with approval.** Propose an action, send an approval request, act on a click.
6. **Safety.** Log every action, prefer reversible ones, protect the automation's credentials, measure that it helps.

## Lab

- [ ] Set up a free automation tool (n8n or Shuffle).
- [ ] Build a workflow: on a test alert, look up an IP's reputation and attach the result.
- [ ] Extend it to open a case automatically for high severity.
- [ ] Add a response step (block an IP) behind a manual approval.
- [ ] Add logging so every action is recorded.

## Self-check

1. Why automate enrichment but not most actions?
2. What is the "automate with approval" pattern for?
3. Why must every automated action be logged and reversible?

??? note "Answers"
    1. Enrichment only reads data, so it is safe and saves the most time; actions change the world and can break the business on a false positive.
    2. Business-affecting response: the workflow gathers evidence and proposes the action, but a human approves before it runs.
    3. So you can prove what the automation did and undo it; automation holds powerful credentials and acts fast, so control and reversibility are essential.

## Links to the handbook and kit

- [Automation and SOAR](../../07-automation-soar/index.md)
- [SOAR principles](../../07-automation-soar/soar-principles.md)
- [Automation catalog](../../07-automation-soar/automation-catalog.md)

## Next module

[T14 SOC Management](../t14-soc-management/index.md).
