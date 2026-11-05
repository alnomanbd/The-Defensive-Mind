# Team and Roles

Who you need in a SOC, what each person does, and how people grow from junior to senior. Written so you can staff a three-person team or a thirty-person one from the same roles.

!!! abstract "At a glance"
    - Audience: SOC manager, HR, anyone hiring for a SOC
    - Time to read: 10 minutes
    - Outcome: clear role definitions, a growth path, and a realistic view of a small-team start

## The roles

A SOC is usually described in tiers. Tiers are about the work, not about worth. In a small team, one person covers several tiers.

| Role | What they do | Typical experience |
|---|---|---|
| L1 analyst (triage) | Watch the queue, validate and enrich alerts, close clear false positives, escalate the rest within SLA | 0 to 2 years |
| L2 analyst (investigation) | Scope and investigate escalated alerts, run containment, handle most incidents, propose tuning | 2 to 5 years |
| L3 analyst (hunter, responder) | Lead serious incidents, forensics, threat hunting, build and tune detections | 5 years and up |
| Detection engineer | Write, test and maintain detection rules; manage coverage against ATT&CK | Varies; often an L2 or L3 specialism |
| Threat intelligence analyst | Track threats relevant to the organisation, enrich alerts, run a threat feed and watchlist | Varies |
| SOC manager or lead | Run the rota, quality, metrics, hiring, and the relationship with the business | Senior |
| SOC or security engineer | Run the SIEM, EDR and pipelines; keep log sources flowing; build automation | Varies |

!!! note "Tiers are a model, not a wall"
    Strict L1 to L2 to L3 handoffs can slow things down and bore good people. Many modern SOCs blend tiers: analysts own an alert end to end with help from seniors, rather than passing a ticket up a chain. Use tiers to describe skill and responsibility, not to build a bureaucracy.

## What each person actually does in a day

| Role | A normal day |
|---|---|
| L1 | Acknowledge alerts within SLA, enrich (who, what, where), close noise with a reason, escalate real ones with notes |
| L2 | Take escalations, pull the full picture across logs, decide true or false positive, contain, write the case up |
| L3 | Lead any live incident, run a planned hunt, review and improve detections, mentor L1 and L2 |
| Detection engineer | Turn a gap or a hunt into a tested rule, retire noisy rules, track coverage |
| SOC manager | Check SLA and queue health, unblock the team, review case quality, handle stakeholders, plan |

## Starting small: who comes first

You cannot hire everyone at once. Hire in this order:

1. **The owner first.** One experienced person (an L3 or a hands-on manager) who can set up tools, write the first detections and runbooks, and handle an incident. Without this person, more juniors just means more confusion.
2. **One or two analysts** (L1 or L2) to run the daily queue once there is process for them to follow.
3. **An engineer** (or engineer time) to keep log sources and the SIEM healthy, if the owner cannot do it all.
4. **Specialists** (detection engineer, threat intel, more L3) as volume and maturity grow.

A credible first SOC is often three people: one senior owner, one or two analysts, and shared or borrowed engineering. Managed coverage fills the nights.

!!! warning "The anti-pattern"
    Hiring several juniors and no senior is the most common staffing mistake. Juniors need method, detections and someone to escalate to. Give them a senior and process, or they churn and the alerts pile up unworked.

## Growing people (and keeping them)

SOC work burns people out when it is endless alert-closing with no progress. Keep good people by giving them a path and real work.

| From | To | How |
|---|---|---|
| L1 | L2 | Shadow investigations, own small cases, learn one platform deeply |
| L2 | L3 or detection engineer | Lead an incident, build and own detections, run a hunt |
| Analyst | Specialist | Pick a lane: detection engineering, threat intel, forensics, cloud |

Retention basics that cost little:

- [ ] Rotate people off pure triage; give everyone some engineering, hunting or project time.
- [ ] Use automation to kill the dull, repetitive work, not to cut people.
- [ ] Give training time and let people certify.
- [ ] Review cases to learn, never to blame ([Post-incident review](../03-incident-response/post-incident-review.md)).
- [ ] Protect time off; a SOC that pages people on holiday loses them.

## Skills to hire for

Technical skills can be taught faster than these:

- Curiosity: the urge to ask "but why did that happen?"
- Calm under pressure: incidents are stressful; panic spreads.
- Clear writing: a case is only as good as its notes.
- Honesty: saying "I am not sure" and "I missed that" openly.

## Related pages

- [Operating model](operating-model.md)
- [Budget and staffing](budget-and-staffing.md)
- [SOC Training](../training/index.md)
- [Field guide](../field-guide/index.md)
