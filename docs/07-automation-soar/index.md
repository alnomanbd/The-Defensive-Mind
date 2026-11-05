# Automation and SOAR

How to make a SOC do more with the people it has, by automating the dull, repetitive parts of the work and letting analysts spend their time on judgement. SOAR stands for security orchestration, automation and response: tools and scripts that run the steps a human would otherwise do by hand.

!!! abstract "At a glance"
    - Audience: SOC manager, detection engineer, automation engineer, analysts
    - Time to read: 5 minutes
    - Outcome: you know what to automate, what not to, and where to start

## Pages in this section

| Page | Open it when you need to... | Main users |
|---|---|---|
| [SOAR principles](soar-principles.md) | Decide what to automate, how far, and how to keep it safe | SOC manager, automation engineer |
| [Automation catalog](automation-catalog.md) | Pick concrete workflows to build, from easy wins to full response | Automation engineer, detection engineer |
| [Alert fatigue and notifications](alert-fatigue-and-notifications.md) | Stop drowning analysts and send the right alert to the right place | SOC lead, manager |
| [Case deduplication](case-deduplication.md) | Group related alerts into one case instead of a hundred tickets | Detection engineer, L2 |

## What SOAR is, in plain words

A SOAR takes a playbook (the steps an analyst follows) and runs those steps automatically: look up an IP's reputation, check if a user is on the leaver list, pull the EDR process tree, and either present the result to an analyst or act on it. It is a robot that does the clicking, so the human does the thinking.

You do not need an expensive SOAR product to automate. A few scripts, a workflow tool, or an open-source automation platform can deliver most of the value. The skill is in choosing what to automate, not in which tool you buy.

## The golden rule

!!! tip "Automate enrichment freely. Automate action carefully."
    Gathering information (enrichment) is safe to automate: looking things up changes nothing. Taking action (disabling an account, isolating a host, blocking an IP) can break the business if it fires on a false positive. Automate enrichment everywhere; automate action only where a false positive is cheap to undo, or keep a human approval in the loop.

## Where automation pays off most

| Work | Automate? | Why |
|---|---|---|
| Enriching an alert (IP, domain, hash, user, host) | Yes, fully | Safe, repetitive, slow by hand |
| Grouping related alerts into one case | Yes | Cuts ticket noise massively ([Case deduplication](case-deduplication.md)) |
| Closing known-benign alerts | Yes, carefully | Saves huge time; needs tight conditions |
| Routing and notifying | Yes | Right alert, right person, right channel ([Alert fatigue](alert-fatigue-and-notifications.md)) |
| Containment (isolate host, disable account) | Partly | Automate with approval, or only where reversible |
| Judgement: is this a real incident? | No | This is the analyst's job; automation supports it |

## Start here

- [ ] Automate enrichment first. It is safe, it saves the most analyst time, and it teaches you the tools.
- [ ] Then automate alert grouping and routing to cut noise.
- [ ] Then automate response with a human approval step.
- [ ] Only fully automate an action when a false positive is cheap and you have measured the rule.

Do not buy a SOAR for a process you have not yet defined. Write the manual runbook first, run it by hand until it is stable, then automate it. Automating a bad process just produces mistakes faster.

## Related pages

- [SOAR principles](soar-principles.md)
- [Automation catalog](automation-catalog.md)
- [Technology stack](../01-build-a-soc/technology-stack.md)
- [Playbooks](../04-playbooks/index.md)
