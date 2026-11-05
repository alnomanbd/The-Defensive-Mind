# SOAR Principles

How to automate SOC work without creating new risks. Automation that fires the wrong action on a false positive can do more damage than the attack. These principles keep automation useful and safe.

!!! abstract "At a glance"
    - Audience: SOC manager, automation engineer, detection engineer
    - Time to read: 10 minutes
    - Outcome: a set of rules for what to automate, how far, and how to keep it under control

## Principle 1: automate the process, not the judgement

Automation is brilliant at the repetitive, rule-based parts of SOC work: looking things up, copying data, routing, grouping. It is poor at judgement: deciding whether something is a real attack in a situation nobody foresaw. Automate the hands, keep the head human.

| Automate | Keep human |
|---|---|
| Enrichment, lookups, correlation, routing, grouping, closing clearly benign alerts | Deciding "is this a real incident", approving business-affecting action, anything novel |

## Principle 2: enrichment is safe, action is not

Reading information changes nothing, so automate it freely. Taking action changes the world, so treat it with care.

| Action | Risk if it fires wrongly | How to automate it safely |
|---|---|---|
| Look up IP, domain, hash, user | None | Fully automate |
| Block an IP at the firewall | Could block a partner or your own range | Time-limit it; exclude known-good ranges |
| Disable a user account | Could lock out a real user, including an executive | Require approval, or limit to clearly malicious cases |
| Isolate a host | Could take a production server offline | Approval for servers; auto for laptops is often fine |
| Delete or quarantine a file | Could remove something needed | Quarantine (reversible), not delete |

!!! warning "The false positive multiplier"
    A manual analyst catches a false positive before acting. Automation does not; it acts at machine speed on every match, including the wrong ones. Before you automate an action, ask: what happens if this fires 100 times on a false positive at 3am? If the answer is "an outage", keep a human in the loop.

## Principle 3: keep a human in the loop where it matters

Full automation is not the goal; the right amount is. Three patterns, from safest to boldest:

| Pattern | What it means | Use for |
|---|---|---|
| Automate and inform | The robot gathers and presents; the human decides and acts | Most investigation and enrichment |
| Automate with approval | The robot proposes an action; a human clicks approve | Business-affecting response |
| Fully automate | The robot acts, then logs what it did | Only reversible, low-risk, well-measured actions |

Move an action from one pattern to a bolder one only after it has run safely for a while and you trust the conditions.

## Principle 4: build on a stable manual process

Automate a runbook only after humans have run it enough to know it is right. Automating an unstable process just makes mistakes faster and harder to see.

- [ ] Write the manual runbook.
- [ ] Run it by hand until the steps and conditions are stable.
- [ ] Automate the safe, repetitive parts first (enrichment).
- [ ] Add action steps last, with approval.

## Principle 5: every automation is logged and reversible

You must be able to answer "what did the automation do, and can we undo it?"

- [ ] Log every automated action: what, when, why, on what, by which workflow.
- [ ] Prefer reversible actions (quarantine, time-limited block) over permanent ones (delete, permanent block).
- [ ] Have a documented way to undo each automated action and to turn the automation off fast.
- [ ] Alert when an automation fails or behaves oddly; a broken workflow is a blind spot.

## Principle 6: automation is code, treat it as code

Workflows and scripts are code with real power. Manage them like code.

- [ ] Keep them in version control, with review before changes go live.
- [ ] Test changes somewhere safe before production.
- [ ] Protect the credentials automations use; they often have strong permissions.
- [ ] Review and retire automations that are no longer needed or trusted.

!!! danger "Automation holds powerful credentials"
    A SOAR that can disable accounts and isolate hosts holds some of the most powerful access in the organisation. If an attacker reaches it, they can turn your defences into a weapon. Protect automation credentials, segment the automation platform, and monitor it like a crown jewel.

## Principle 7: measure whether it helps

Automation should save time and reduce mistakes. Prove it.

| Measure | Shows |
|---|---|
| Analyst time saved per alert | Whether enrichment automation is worth it |
| Time to contain, before and after | Whether response automation helps |
| False actions taken by automation | Whether an action automation is safe |
| Alerts auto-closed and later found real | Whether auto-close conditions are too loose |

If an automation does not measurably help, or it causes wrong actions, turn it off and fix it. Automation for its own sake is just more code to maintain.

## Related pages

- [Automation catalog](automation-catalog.md)
- [Alert fatigue and notifications](alert-fatigue-and-notifications.md)
- [Playbooks](../04-playbooks/index.md)
- [SOC Training](../training/index.md)
