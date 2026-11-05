# SOC Build Roadmap

A practical order of work to go from nothing to a running SOC: the first 30, 60 and 90 days, then the rest of the first year. Each step produces something real, not a document that sits on a shelf.

!!! abstract "At a glance"
    - Audience: the person tasked with building the SOC, and their manager
    - Time to read: 10 minutes
    - Outcome: a phased plan with clear deliverables you can put dates against

!!! tip "Rule of the roadmap"
    Every phase must end with something that works, not something that is written. A detection that fires, a log source that flows, a runbook someone followed. Progress is measured in working capability, not slides.

## Before day one: three questions

Answer these with your sponsor first. They shape everything else.

| Question | Why it matters |
|---|---|
| What are we protecting, and from what? | Decides which logs and detections come first. A payment company and a hospital have different top risks |
| What hours must we cover? | Decides the operating model and headcount ([Operating model](operating-model.md)) |
| What can we spend, people and tools? | Decides in-house vs managed, open-source vs commercial ([Budget and staffing](budget-and-staffing.md)) |

## Days 1 to 30: foundation

Goal: see something, and be able to act on it.

- [ ] Name the owner and get time formally allocated (even if part time at first).
- [ ] Agree the operating model and hours with the sponsor.
- [ ] List the top 5 risks and the systems that matter most (the "crown jewels").
- [ ] Inventory what logs you already have and where they go.
- [ ] Stand up a SIEM (even a single-node open-source one) and an EDR on the most important endpoints.
- [ ] Onboard the first log sources: identity (Active Directory or the identity provider), endpoints (EDR), and the perimeter (firewall, VPN) ([Log source priorities](log-source-priorities.md)).
- [ ] Write a one-page incident response plan: who to call, how to declare, how to reach people out of hours.

Deliverable: alerts from your most important systems arrive in one place, and you know who acts on them.

## Days 31 to 60: detection and process

Goal: catch the attacks that matter most, consistently.

- [ ] Write the first 10 to 20 detections, chosen by risk, not by what is easy ([Use case prioritization](use-case-prioritization.md)).
- [ ] Map each detection to MITRE ATT&CK so you can see your coverage and gaps.
- [ ] Write the core runbooks: alert triage, severity and escalation, the top 3 playbooks for your most likely incidents.
- [ ] Set up the case or ticket system, even if it is a shared board to start.
- [ ] Start the daily rhythm: a health check and a triage round every working day ([Daily operations](../02-daily-operations/index.md)).
- [ ] Tune the first wave of noise so the queue stays workable.

Deliverable: a daily routine that a named person follows, with detections firing on real risk and runbooks to work them.

## Days 61 to 90: response and measurement

Goal: respond well, and prove it.

- [ ] Run a tabletop exercise on your most likely serious incident ([Tabletop exercises](../03-incident-response/tabletop-exercises.md)).
- [ ] Finish the incident response method: evidence handling, communication, post-incident review.
- [ ] Decide and publish your first metrics: time to acknowledge, time to respond, false positive rate, coverage ([Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)).
- [ ] Hold the first monthly review with the sponsor: what you caught, what you missed, what you need.
- [ ] Close the biggest coverage gaps found so far.
- [ ] Write the on-call or out-of-hours plan and test that paging works.

Deliverable: a SOC that detects, responds and reports, with numbers to show it is working.

## Months 4 to 12: maturity

Goal: get reliable, then get smart.

| Quarter | Focus |
|---|---|
| Months 4 to 6 | Widen log coverage (cloud, SaaS, email, web). Grow the detection library. Reduce false positives. Formalise shift handover and case quality review |
| Months 7 to 9 | Add automation for the repetitive work (enrichment, containment) with a SOAR or scripts. Start threat intelligence: a feed, a watchlist, context on alerts |
| Months 10 to 12 | Start regular threat hunting. Run a purple team exercise. Re-score maturity and set next year's targets ([Maturity model](maturity-model.md)) |

## Common mistakes in year one

| Mistake | Do instead |
|---|---|
| Buying the SIEM first, then wondering what to feed it | Decide log sources and detections first, then size the tool |
| Collecting everything "to be safe" | Collect what you will detect or investigate with. Noise costs money and attention |
| Hiring analysts before there is work or process | Build the minimum process first; a queue with no method burns people out |
| Chasing 24/7 from day one | Start with business hours plus a clear on-call plan; grow coverage with demand |
| Measuring alert volume as success | Measure outcomes: time to respond, real incidents caught, noise cut |
| Writing detections for easy things | Write detections for your real risks, even when they are harder |

## Related pages

- [Operating model](operating-model.md)
- [Log source priorities](log-source-priorities.md)
- [Use case prioritization](use-case-prioritization.md)
- [Maturity model](maturity-model.md)
- [Daily routine](../02-daily-operations/daily-routine.md)
