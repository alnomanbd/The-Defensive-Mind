# Budget and Staffing

How to put real numbers against a SOC: people, tools and running costs, and how to make the case to leadership. The exact figures depend on your country and size, so this page gives the structure and the ratios, not prices you should copy blindly.

!!! abstract "At a glance"
    - Audience: SOC manager, CISO, finance
    - Time to read: 10 minutes
    - Outcome: a cost structure, the headcount maths for coverage, and how to justify the spend

!!! warning "Numbers here are illustrative"
    Salaries, licences and provider fees vary widely by country, sector and scale. Use the structure and ratios below, then fill in real quotes and local salary data. Do not take any figure here as a price.

## The three cost buckets

| Bucket | What is in it | Rough share |
|---|---|---|
| People | Salaries, on-call pay, training, recruitment | Usually the largest, often half to three quarters |
| Technology | SIEM, EDR, SOAR, TIP licences or hosting; storage | Varies most; data volume drives it |
| Running costs | Cloud or hardware to host tools, managed services, audits | Smaller but ongoing |

People are almost always the biggest cost. This is why automation (to make each person cover more) and managed services (to buy coverage you cannot staff) are such common choices.

## The headcount maths for coverage

This is the number leadership most often gets wrong. Covering one analyst seat around the clock does not take three or four people.

| Coverage | Analyst seats | People needed (roughly) |
|---|---|---|
| Business hours (8 hours, 5 days) | 1 | 1 to 2 (for cover during leave and sickness) |
| Extended (16 hours, 5 days) | 2 overlapping | 3 to 4 |
| 24/7, one seat always staffed | 1 continuous | 8 to 10 |
| 24/7, two seats always staffed | 2 continuous | 16 to 20 |

!!! note "Why 24/7 needs 8 to 10 for one seat"
    A year has 8,760 hours. One person works roughly 1,600 to 1,800 productive hours after holidays, sickness, training and breaks. Covering 8,760 hours with no gaps, plus overlap for handover and resilience, lands near 8 to 10 people for a single always-staffed seat. This single fact drives most operating-model decisions ([Operating model](operating-model.md)).

## A realistic small-SOC budget shape

For a first in-house SOC covering business hours plus on-call:

| Item | Notes |
|---|---|
| 1 senior owner (L3 or hands-on lead) | The anchor; sets up and runs everything |
| 1 to 2 analysts (L1 or L2) | Run the daily queue |
| Shared or part-time engineer | Keeps the pipeline and SIEM healthy |
| SIEM | Open source (hosting cost) or commercial (licence by data) |
| EDR | Licence per endpoint |
| Managed coverage for nights and weekends | An MDR provider, priced per endpoint or per seat |
| Training and certification budget | Small but vital for retention |
| Contingency | For incident response help you may need to buy in |

Open-source tools move cost from licences to engineering time. Managed services move cost from hiring to a monthly fee. Neither is free; choose where you want the cost to sit.

## Making the case to leadership

Leadership funds outcomes and risk reduction, not tools. Frame the ask that way.

| Weak case | Strong case |
|---|---|
| We need a SIEM and three analysts | We cannot currently detect ransomware before it spreads; here is what that costs us and what this team prevents |
| Buy this product, it is industry leading | For this spend we move from no night coverage to detecting and containing a serious incident within the hour |
| Our alert volume is up | We cut time-to-contain from days to hours; here is the trend |

Tie the budget to specific risks and to measurable improvement ([Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)). A number next to a prevented harm is far more persuasive than a tool name.

## Where to spend first when money is tight

In order of value for money:

1. **One capable person.** A senior who can build and run beats several juniors with no leader.
2. **EDR on important endpoints.** The most detection and response per dollar.
3. **A SIEM you can run**, fed by identity and endpoint logs.
4. **Managed coverage for nights**, if 24/7 matters, rather than hiring a night shift you cannot keep.
5. **Automation**, once the process exists, to make each person cover more.

Spend late on: a threat intelligence platform, a SOAR, and advanced tooling. These multiply a working SOC; they do not create one.

## Ongoing costs people forget

- [ ] Log storage grows; hot search data and long-term archive both cost money.
- [ ] Training and certification, every year, for every analyst.
- [ ] On-call pay and the cost of burnout and turnover if you skip it.
- [ ] Incident response retainer or budget for outside help in a crisis.
- [ ] Tool price rises, especially data-volume pricing as you grow.

## Related pages

- [Operating model](operating-model.md)
- [Team and roles](team-and-roles.md)
- [Technology stack](technology-stack.md)
- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
