# A Day as a SOC Manager / Lead

The manager makes the SOC reliable: the queue is worked, SLAs are met, people are not burning out, incidents are handled, and leadership sees the value. Less hands-on analysis, more making the machine run and protecting the people in it.

!!! abstract "At a glance"
    - Audience: SOC managers, team leads, aspiring leads
    - Time to read: 25 minutes
    - Outcome: a daily, weekly and monthly routine, the core metrics, how to run a major-incident bridge, and message templates

## The routine

### Daily

| Time | What you do | Why |
|---|---|---|
| Start | Check the queue health and any SLA breaches overnight | Catch a drowning queue before it hides a real alert |
| Start | Read the overnight handover and any open incidents | Know what is live before the day starts |
| Morning | Unblock the team: approvals, access, stuck cases | Analysts should not wait on you to act |
| Through day | Be reachable for escalations and major-incident decisions | You approve business-affecting containment |
| End | Confirm handover and out-of-hours cover is clear | Nobody should be unsure who holds the pager tonight |

### Weekly

- [ ] Review the noisiest rules and the tuning backlog ([Alert tuning](../02-daily-operations/alert-tuning.md)).
- [ ] Sample closed cases for quality; coach, do not blame.
- [ ] Check SLA trends and queue volume; staff or tune accordingly.
- [ ] One-to-one or team check-in; watch for burnout.
- [ ] Review open incidents and their actions.

### Monthly

- [ ] Produce the management report: what you caught, what you missed, trends, needs ([Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)).
- [ ] Review detection coverage and the gap backlog ([Coverage mapping](../05-detection-engineering/coverage-mapping.md)).
- [ ] Check post-incident review actions are actually closing.
- [ ] Review threat intel relevance; drop useless feeds.
- [ ] Look ahead: training, hiring, tooling, upcoming risks.

## The metrics that matter

Measure outcomes, not activity. "We closed 5,000 alerts" says nothing about whether you are safe.

| Metric | What it means | Watch for |
|---|---|---|
| Time to acknowledge (MTTA) | How fast an alert is picked up | Rising = queue overwhelmed or understaffed |
| Time to respond or contain (MTTR) | How fast a real incident is stopped | The number leadership cares about most |
| False positive rate | Share of alerts that were noise | High = tuning backlog, analysts drowning |
| Coverage | Techniques you reliably detect | Gaps near crown jewels are the priority |
| SLA met | Share of alerts and incidents handled in time | Falling = a resourcing or process problem |
| Escaped incidents | Real incidents found late or by someone else | The honest measure of what you missed |

!!! warning "Do not reward volume"
    If you measure the team on alerts closed, you get alerts closed fast, including real ones closed as benign to clear the queue. Measure outcomes: time to contain, real incidents caught, noise reduced. What you measure is what you get.

## Running a major incident

When a P1 hits, the manager coordinates; the analysts investigate. Your job is to run the response, not to grab a keyboard.

- [ ] Declare the incident, set severity, name an incident lead (may be you or an L3).
- [ ] Open the bridge or channel; get the right people on it (SOC, IT, the system owner, and the CISO for P1).
- [ ] Keep the timeline and decisions logged; assign someone to scribe.
- [ ] Approve or escalate business-affecting containment (isolation, shutdown).
- [ ] Run the communication rhythm: regular updates to leadership with facts, not speculation ([Escalation and communication](../03-incident-response/escalation-and-communication.md)).
- [ ] Protect the team: rotate people on long incidents, bring food, manage fatigue.
- [ ] After: make sure a blameless review happens and its actions get owned ([Post-incident review](../03-incident-response/post-incident-review.md)).

## Protecting your people

Burnout is the SOC's biggest hidden risk. A tired, demoralised analyst misses the alert that matters.

- [ ] Keep the queue humanly workable; a flood is a process failure, not an effort failure.
- [ ] Rotate people off pure triage; give everyone some hunting, engineering or project work.
- [ ] Use automation to kill dull work, not to cut headcount.
- [ ] Protect time off; do not page people on holiday except for genuine P1.
- [ ] Run reviews to learn, never to blame. One blame session and people stop reporting their own mistakes.
- [ ] Give training time and a growth path ([Team and roles](../01-build-a-soc/team-and-roles.md)).

## Message templates

### Status update to leadership (open High or Critical)

```text
Subject: [Pn] <short title> - update <time UTC>
Status: <contained / investigating / recovering>
What happened: <one or two factual sentences>
Impact: <systems, users, data: confirmed / suspected / unknown>
Actions taken: <containment so far>
Next steps: <what, by when>
Needed from you: <decision or support, or "nothing right now">
Next update: <time>
```

### Monthly summary opening

```text
In <month>, the SOC handled <N> alerts, of which <M> were real incidents.
We contained incidents in a median of <X>. False positives fell to <Y percent> after tuning.
Highlights: <1 to 3 things caught or improved>.
Risks and needs: <1 to 3 clear asks tied to risk>.
```

## Making the case for resources

Leadership funds risk reduction, not tools or headcount for their own sake. Tie every ask to a risk and a number ([Budget and staffing](../01-build-a-soc/budget-and-staffing.md)).

| Weak | Strong |
|---|---|
| We need more analysts | Our time-to-contain is rising because the queue exceeds capacity; here is the trend and what one more analyst changes |
| Buy this tool | For this spend we go from no night coverage to containing a serious incident within the hour |

## Related pages

- [Metrics and KPIs](../02-daily-operations/metrics-and-kpis.md)
- [Operating model](../01-build-a-soc/operating-model.md)
- [Team and roles](../01-build-a-soc/team-and-roles.md)
- [Escalation and communication](../03-incident-response/escalation-and-communication.md)
- [Post-incident review](../03-incident-response/post-incident-review.md)
