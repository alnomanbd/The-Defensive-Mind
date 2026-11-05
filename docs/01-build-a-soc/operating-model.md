# Operating Model

How to decide the shape of your SOC: run it yourself, buy it as a service, or mix the two; and which hours you really need to cover. Get this wrong and you either overspend on staff you cannot keep busy, or you have no one watching when the attack comes.

!!! abstract "At a glance"
    - Audience: CISO, SOC manager, IT leadership
    - Time to read: 10 minutes
    - Outcome: a clear choice of model and coverage hours, with the trade-offs named

## The three models

| Model | What it means | Best when |
|---|---|---|
| In-house | You hire, train and run the whole SOC | You have the budget and scale, strict data rules, or need deep knowledge of your own systems |
| Managed (MSSP or MDR) | A provider monitors and alerts (MSSP) or monitors and responds (MDR) for you | You are small, need 24/7 fast, or lack the people to hire |
| Hybrid | You keep triage, response and knowledge in-house; a provider fills nights, weekends or specialist work | Most organisations past the smallest size: you keep control and context, buy coverage and depth |

!!! note "MSSP vs MDR"
    An **MSSP** (managed security service provider) watches your tools and sends you alerts; you still investigate and respond. An **MDR** (managed detection and response) provider also investigates and takes agreed response actions, such as isolating a host. MDR costs more but gives you far more than alerts.

### How to choose

Ask these, in order:

- [ ] Do we have strict rules on who can see our data (law, contract, sector)? If yes, in-house or a provider cleared for that data.
- [ ] Do we need 24/7 within weeks, not months? If yes, start with managed or hybrid; you cannot hire a night shift that fast.
- [ ] Can we recruit and keep security analysts in our location and budget? If no, lean on managed for the hard-to-staff hours.
- [ ] How unusual are our systems? Very unusual systems are hard for an outside provider to understand; keep more in-house.
- [ ] What is the real budget over three years, not just year one? Managed is faster to start; in-house can be cheaper at scale but slower to build.

The most common sensible answer for a mid-sized organisation is **hybrid**: a small in-house team in business hours who know the systems, plus an MDR provider for nights, weekends and overflow.

## Coverage hours

"24/7" is the instinct, but it is expensive and often unnecessary on day one. Match coverage to risk and to how fast you could actually respond.

| Model | What it covers | Roughly needs |
|---|---|---|
| Business hours | Monitoring during the working day only | 1 to 3 people, plus an on-call plan for after hours |
| Business hours plus on-call | Working day monitored; nights and weekends paged for high-severity alerts | Small team plus a paid on-call rota |
| Extended (for example 07:00 to 23:00) | Two overlapping shifts cover most of the day | 4 to 6 people |
| 24/7 follow-the-shift | Someone always watching | 8 to 12 people for one seat, or a managed provider for nights |

!!! warning "24/7 is a people problem, not a tool problem"
    One analyst seat covered around the clock needs roughly 8 to 10 people once you account for shifts, holidays, sickness and training. Night shifts are hard to staff and hard to keep. This is the single biggest reason organisations buy managed coverage for nights.

### A realistic path

1. Start with business hours plus a tested on-call plan for P1 and P2 incidents.
2. Add an MDR provider for nights and weekends when risk or compliance demands it.
3. Move more in-house only when volume justifies full shifts and you can recruit for them.

## What to keep in-house even when you buy managed

Never outsource these, whatever model you pick:

- [ ] Ownership and accountability. A provider supports you; they are not responsible for your risk.
- [ ] Knowledge of your own systems, crown jewels and business context.
- [ ] The decision to declare an incident and the authority to approve containment that affects the business.
- [ ] Relationships with IT, legal, HR and leadership.
- [ ] Reading and challenging the provider's alerts and monthly reports.

A managed service with no engaged owner on your side drifts into a stream of alerts nobody acts on. The provider is an extension of your team, not a replacement for having one.

## Managing a provider well

| Do | Why |
|---|---|
| Agree response times (SLAs) in writing, per severity | So "we are looking into it" has a deadline |
| Give them context: asset lists, crown jewels, maintenance windows | Cuts false positives and missed detections |
| Review their alerts and misses monthly | Keeps quality up and shows you are paying attention |
| Run a test or purple team against them yearly | Proves they actually detect, not just promise to |
| Keep your own copy of logs and detections | So you are not locked in and can leave if needed |

## Related pages

- [Team and roles](team-and-roles.md)
- [Budget and staffing](budget-and-staffing.md)
- [Roadmap](roadmap.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
