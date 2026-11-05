# Tool Selection Guide

How to choose or replace a SOC tool without being sold to. A structured way to score options against your real needs, so you pick what fits your team and budget, not what demos best.

!!! abstract "At a glance"
    - Audience: SOC lead, SOC manager, engineers running a proof of concept
    - Time to read: 10 minutes
    - Outcome: a scoring method and a proof-of-concept plan that survive the vendor sales pitch

!!! tip "Start from your needs, not the market"
    The right order is: write down what you need, score options against that, then watch demos. Walk into a demo without your own requirements and you will be sold the vendor's strengths, which may not be your needs.

## Step 1: write your requirements first

Before looking at any product, list what you actually need, and split it into must-have and nice-to-have.

| Area | Example requirements |
|---|---|
| Fit | Works with your log sources, cloud and identity provider |
| Scale | Handles your data volume now and in two years |
| People | Your team can actually run it with the skills you have |
| Integration | Talks to your other tools through APIs |
| Response | Can take the actions you need (isolate, disable, block) |
| Cost | Total cost over three years, not just year one |
| Support | Vendor support, community, documentation |
| Exit | You can get your data and detections out if you leave |

A requirement the product cannot meet is a dealbreaker; a nice-to-have is a tie-breaker. Be honest about which is which.

## Step 2: score options

Rate each option against your requirements. A simple weighted table keeps it objective.

| Requirement | Weight | Option A | Option B | Option C |
|---|---|---|---|---|
| Fits our log sources | High | | | |
| We can run it | High | | | |
| Integrates with our stack | High | | | |
| Handles our volume | Medium | | | |
| Response actions | Medium | | | |
| Total 3-year cost | High | | | |
| Support and community | Medium | | | |
| Data and detection portability | Medium | | | |

Score each cell (for example 1 to 3), multiply by the weight, and total. The number does not decide for you, but it stops a slick demo outweighing a dealbreaker.

!!! warning "Watch for the traps"
    Three things sink tool decisions: **pricing by data volume** (a SIEM bill that explodes as you grow), **a tool your team cannot run** (powerful and idle beats powerful and misused), and **lock-in** (you cannot get your data or detections out). Score all three explicitly.

## Step 3: run a real proof of concept

Never buy on a demo. Run the tool on your own data, with your own team, for a set time.

- [ ] Define success criteria in advance: what must the tool do to pass?
- [ ] Use your real log sources and a realistic data volume.
- [ ] Have your actual analysts use it, not just the engineer who set it up.
- [ ] Run your top few detections and a real investigation through it.
- [ ] Test the integrations you depend on.
- [ ] Measure against the criteria, not against the sales story.

A tool that passes a proof of concept on your data, run by your people, is a safe buy. A tool that only shone in the vendor's demo is a risk.

## Open source vs commercial

| Factor | Open source | Commercial |
|---|---|---|
| Licence cost | None | Often significant, sometimes by data volume |
| Running cost | Your engineering time | Lower, the vendor runs more of it |
| Control | Full | Limited to what the vendor exposes |
| Support | Community, your own skills | Vendor support and SLAs |
| Best when | You have the skills and want control | You lack the people and want it to just run |

Neither is better in general. Open source moves cost from licences to engineering time; commercial moves it from hiring to a fee. Choose where you want the cost and the control to sit.

## Decide and record

- [ ] Pick the option that meets the must-haves, scores best, and passed the proof of concept.
- [ ] Record why you chose it, including what you traded off. The next person (and the next audit) will ask.
- [ ] Plan the rollout, the training, and how you would exit if it disappoints.
- [ ] Set a review date to check it is still the right choice.

## Related pages

- [Technology stack](../01-build-a-soc/technology-stack.md)
- [Open-source SOC lab](open-source-soc-lab.md)
- [Budget and staffing](../01-build-a-soc/budget-and-staffing.md)
- [Useful resources](useful-resources.md)
