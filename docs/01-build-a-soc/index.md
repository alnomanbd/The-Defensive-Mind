# Build a SOC

How to stand up a Security Operations Center (SOC) from nothing, or turn an informal "whoever notices" setup into a real capability. This section is the plan: the order to build in, who you need, what to buy, which logs to collect first, which detections to write first, and how to know you are getting better.

!!! abstract "At a glance"
    - Audience: anyone asked to start or rebuild a SOC: security lead, IT manager, new SOC manager, CISO
    - Time to read: 6 minutes
    - Outcome: you know the building blocks, the order to tackle them, and where to go deep

## Pages in this section

| Page | Open it when you need to... | Main users |
|---|---|---|
| [Roadmap](roadmap.md) | Plan the first 90 days and the first year in the right order | Security lead, SOC manager |
| [Operating model](operating-model.md) | Decide in-house, managed (MSSP), or hybrid, and the hours you cover | CISO, SOC manager |
| [Team and roles](team-and-roles.md) | Work out who you need, what each person does, and how to grow people | SOC manager, HR |
| [Technology stack](technology-stack.md) | Choose the tools (SIEM, EDR, SOAR, TIP) without overspending | SOC manager, security engineer |
| [Log source priorities](log-source-priorities.md) | Decide which logs to collect first for the most detection value | Security engineer, SOC lead |
| [Use case prioritization](use-case-prioritization.md) | Choose which detections to build first and track coverage | Detection engineer, SOC lead |
| [Maturity model](maturity-model.md) | Score where you are and plan the next step up | SOC manager, CISO |
| [Budget and staffing](budget-and-staffing.md) | Put real numbers to people, tools and running costs | SOC manager, CISO, finance |

## What a SOC actually is

A SOC is not a room with screens. It is a **capability**: people, process and technology working together to detect, investigate and respond to security threats, every day, and to get better over time. You can run a useful SOC with three people and open-source tools, or a weak one with twenty people and expensive products. The difference is process and focus, not spend.

A SOC does five things:

| Function | In plain words |
|---|---|
| Collect | Bring logs and telemetry from across the organisation into one place |
| Detect | Turn that data into alerts when something looks wrong |
| Triage and investigate | Decide which alerts are real and what they mean |
| Respond | Contain, eradicate and recover from real incidents |
| Improve | Tune out noise, add detections, learn from every incident |

## Build in this order

Building out of order is the most common and most expensive mistake. Buying a SIEM before you know your log sources, or hiring analysts before you have anything for them to do, wastes money and burns people out.

```text
1. Decide the operating model and hours        (operating-model)
2. Name an owner and a small team              (team-and-roles)
3. Pick the few log sources that matter most   (log-source-priorities)
4. Stand up a SIEM and EDR, collect those logs (technology-stack)
5. Write the first 10 to 20 detections         (use-case-prioritization)
6. Write the runbooks: triage, severity, IR    (daily operations and IR sections)
7. Run the daily rhythm, measure, improve       (daily operations, maturity-model)
8. Add automation and advanced work last        (SOAR, threat hunting, TI)
```

## The honest minimum

You have a working SOC, however small, when all of these are true:

- [ ] One person is accountable for security monitoring, named, with time allocated.
- [ ] Logs from identity, endpoints and the perimeter reach one searchable place.
- [ ] A written list of what you are trying to detect, and a detection for each.
- [ ] A triage method and a severity scale everyone uses ([Daily operations](../02-daily-operations/index.md)).
- [ ] An incident response plan people have actually read ([Incident response](../03-incident-response/index.md)).
- [ ] Someone looks at the alert queue every working day, and the queue is owned out of hours by a clear plan.

Everything else, more tools, more people, automation, hunting, is improvement on top of this minimum. Do not skip the minimum to get to the exciting parts.

## Related pages

- [Daily operations](../02-daily-operations/index.md)
- [Incident response](../03-incident-response/index.md)
- [Detection engineering](../05-detection-engineering/index.md)
- [SOC Training](../training/index.md)
