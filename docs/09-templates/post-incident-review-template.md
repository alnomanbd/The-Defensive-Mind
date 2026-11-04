# Post-Incident Review Template

A template for the structured review held after an incident is closed. The goal is learning and improvement, not blame.

!!! abstract "At a glance"
    - Audience: SOC lead / incident handlers / process and system owners
    - Time to read: 5 minutes (60-90 minute meeting plus write-up)
    - Outcome: a short list of owned, dated improvements that make the next incident smaller

!!! tip "How to use"
    - Hold the review within 5-10 working days of closure, while memories are fresh.
    - Invite everyone who touched the incident, including non-security teams.
    - Use a neutral facilitator who did not lead the response.
    - Read the [incident report](incident-report.md) before the meeting so time is spent on analysis, not retelling.
    - State the blameless rule at the start: we examine systems and decisions, not people.

!!! note "When is a review required?"
    Common triggers: every Critical or High incident, any incident with regulatory or customer impact, any incident where a playbook did not work, and a sample of Medium incidents each quarter.

---

## Post-incident review: `<PIR-YYYY-NNNN>` for `<INC-YYYY-NNNN>`

### Meeting details

| Field | Value |
|---|---|
| Date and time | `<YYYY-MM-DD HH:MM UTC>` |
| Facilitator | `<name>` |
| Note taker | `<name>` |
| Attendees | `<names and roles>` |
| Incident severity | `<Critical / High / Medium / Low>` |
| Classification | `<TLP:AMBER>` |

### Incident in one paragraph

> `<Short factual summary: what happened, impact, duration.>`

### Key metrics

| Metric | Target | Actual | Met? |
|---|---|---|---|
| Time to detect (first malicious activity to alert) | `<e.g. 1 hour>` | `<...>` | `<Yes / No>` |
| Time to acknowledge (alert to analyst pickup) | `<15 minutes>` | `<...>` | `<...>` |
| Time to contain (alert to containment) | `<4 hours>` | `<...>` | `<...>` |
| Time to recover (containment to normal service) | `<...>` | `<...>` | `<...>` |
| Escalation done within policy? | Yes | `<...>` | `<...>` |

### What went well

| # | Observation | Keep doing by |
|---|---|---|
| 1 | `<EDR isolation took under 2 minutes>` | `<Keep isolation in playbook step 1>` |
| 2 | `<...>` | `<...>` |

### What did not go well

| # | Observation | Impact | Category |
|---|---|---|---|
| 1 | `<Proxy logs were not in the SIEM>` | `<Two hours lost tracing download>` | `<Visibility>` |
| 2 | `<On-call contact list out of date>` | `<Escalation delayed 40 minutes>` | `<Process>` |

Categories: People / Process / Technology / Visibility / Communication / Third party.

### Root cause analysis

Use "five whys" or a similar method. Stop when you reach something the organisation can change.

| Why? | Answer |
|---|---|
| Why did the incident happen? | `<...>` |
| Why was that possible? | `<...>` |
| Why was that not prevented? | `<...>` |
| Why was it not detected sooner? | `<...>` |
| Why did that gap exist? | `<...>` |

**Root cause statement:** `<one sentence>`

### Detection and response assessment

| Question | Answer |
|---|---|
| Which control detected it first? | `<...>` |
| Which controls should have detected it earlier but did not? | `<...>` |
| Did the playbook fit the incident? What was missing? | `<...>` |
| Were the right people informed at the right time? | `<...>` |
| Was any evidence lost or unavailable? | `<...>` |
| Would we detect the same attack today? | `<Yes / No / Partially: explain>` |

### Improvement actions

| ID | Action | Type | Owner | Due date | Ticket | Status |
|---|---|---|---|---|---|---|
| `<PIR-A1>` | `<Onboard proxy logs to SIEM>` | Visibility | `<team>` | `<date>` | `<LSO-...>` | Open |
| `<PIR-A2>` | `<Add detection for observed technique>` | Detection | `<team>` | `<date>` | `<DET-...>` | Open |
| `<PIR-A3>` | `<Update playbook step for escalation>` | Process | `<team>` | `<date>` | `<...>` | Open |

!!! warning "Avoid the action graveyard"
    Limit the list to the five to seven actions that matter most. Track each one in a real ticketing system and report progress in the [monthly SOC report](monthly-soc-report.md) until it is closed.

### Documents to update

- [ ] Playbook: `<name>`
- [ ] Detection rules: `<rule IDs>`
- [ ] Contact list / escalation matrix
- [ ] Asset inventory or log source register
- [ ] Training material

### Approval

| Role | Name | Date |
|---|---|---|
| SOC lead | `<name>` | `<date>` |
| Process owner | `<name>` | `<date>` |

---

## Worked example

??? example "Filled-in review: PIR-2026-0007 for INC-2026-0042 (mailbox takeover)"
    | Metric | Target | Actual | Met? |
    |---|---|---|---|
    | Time to detect | 1 h | 31 min | Yes |
    | Time to acknowledge | 15 min | 3 min | Yes |
    | Time to contain | 4 h | 46 min | Yes |
    | Escalation within policy | Yes | No, L2 paged 25 min after triage | No |

    **Went well:** the inbox-rule detection fired fast; the mail purge of the same phishing email took 20 minutes.

    **Did not go well:**

    | # | Observation | Impact | Category |
    |---|---|---|---|
    | 1 | MFA exception from 2024 never reviewed | Attack succeeded | Process |
    | 2 | L1 spent 25 min checking if the rule was user-created | Slower escalation | Process |
    | 3 | Proxy logs only kept 7 days | Could not check earlier visits | Visibility |

    | Why? | Answer |
    |---|---|
    | Why did the attacker get in? | Password phished and no MFA on the account |
    | Why no MFA? | Temporary exception granted in 2024 |
    | Why still active? | Exceptions have no expiry date |
    | Why no expiry? | Exception process has no review step |

    **Root cause statement:** MFA exceptions have no owner or expiry, so temporary gaps become permanent.

    | ID | Action | Owner | Due | Status |
    |---|---|---|---|---|
    | PIR-A1 | Add 30-day expiry and owner to every MFA exception | Identity team | 2026-04-15 | Open |
    | PIR-A2 | Playbook: any inbox forwarding to an external domain is escalated to L2 at once | SOC lead | 2026-03-31 | Done |
    | PIR-A3 | Extend proxy log retention to 90 days | SIEM engineering | 2026-04-30 | Open |

## Checklist

- [ ] Blameless rule stated at the start of the meeting
- [ ] Metrics compared against targets
- [ ] Root cause reaches a changeable system or process
- [ ] Each action has an owner, date and ticket
- [ ] Report shared with attendees within five working days

## Related pages

- [Incident report template](incident-report.md)
- [Tabletop exercise template](tabletop-exercise-template.md)
- [Detection request](detection-request.md)
- [Playbook template](../04-playbooks/playbook-template.md)
