# T14: SOC Management

Running the SOC as a capability: the metrics, the people, the reporting and the maturity. This module is for current and aspiring leads, and for analysts who want to understand how the SOC is run.

!!! abstract "At a glance"
    - Level: lead and manager
    - Time: 6 to 8 hours
    - Outcome: you can measure a SOC, report to leadership, and plan its growth

## Learning objectives

- [ ] Choose and use the metrics that matter, not vanity numbers.
- [ ] Staff and schedule coverage realistically.
- [ ] Report to management in terms of risk and outcomes.
- [ ] Score and improve SOC maturity.
- [ ] Protect people from burnout.

## Lessons

1. **Metrics.** Time to acknowledge and respond, false positive rate, coverage, SLA met, escaped incidents; measure outcomes, not activity.
2. **Staffing and shifts.** The headcount maths for coverage, why 24/7 needs 8 to 10 for one seat, and the operating-model choice.
3. **Reporting.** The monthly report: what you caught, what you missed, trends, and clear asks tied to risk.
4. **Maturity.** Scoring across the parts of a SOC and moving up a level by closing the lowest gap.
5. **People.** Rotating off triage, automation to kill dull work, blameless reviews, protecting time off.
6. **Making the case.** Tying every budget ask to a risk and a number.

## Lab

- [ ] Take a month of sample data and compute time-to-acknowledge and false positive rate.
- [ ] Write a one-page monthly management summary from it.
- [ ] Score a fictional SOC against the [maturity model](../../01-build-a-soc/maturity-model.md); pick the next step.
- [ ] Write one budget ask framed as risk reduction, not a tool name.

## Self-check

1. Why not measure the team on alerts closed?
2. How many people does one always-staffed 24/7 seat really need?
3. What is the right next target when improving maturity?

??? note "Answers"
    1. It rewards speed over correctness, including closing real alerts as benign to clear the queue. Measure outcomes: time to contain, incidents caught, noise cut.
    2. Roughly 8 to 10, once shifts, holidays, sickness, training and overlap are accounted for.
    3. Closing your lowest score, not raising your average; and never chasing advanced features while the basics are shaky.

## Links to the handbook and kit

- [SOC manager field guide](../../field-guide/soc-manager.md)
- [Metrics and KPIs](../../02-daily-operations/metrics-and-kpis.md)
- [Maturity model](../../01-build-a-soc/maturity-model.md), [Budget and staffing](../../01-build-a-soc/budget-and-staffing.md)

## Next module

[T16 Modern SOC Architecture](../t16-modern-soc/index.md), or [T15 Career and Interviews](../t15-career-interviews/index.md).
