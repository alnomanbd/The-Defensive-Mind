# Tabletop Exercises

How to practise an incident in a meeting room before it happens for real: plan a scenario, run it in 90 minutes, find the gaps, and fix them. Also covers moving up to technical exercises (purple team, breach and attack simulation).

!!! abstract "At a glance"
    - Audience: SOC managers, CISO, incident leads, IT and business leaders
    - Time to read: 12 minutes
    - Outcome: you can plan and facilitate a tabletop, with three ready scenarios

## Types of exercise

| Type | What happens | Effort | Frequency |
|---|---|---|---|
| Tabletop (discussion) | People talk through what they would do as a scenario unfolds | Low | Quarterly |
| Walkthrough | The team steps through a playbook against a scenario, checking access and tools | Low to medium | When a playbook is new or changed |
| Functional drill | One part done for real: restore a backup, isolate a host, page the on-call | Medium | Twice a year |
| Purple team | Red team runs real techniques (Atomic Red Team, MITRE Caldera, Infection Monkey) while the SOC detects and responds | Medium to high | Quarterly to yearly |
| Full simulation | End to end with business, communications, legal | High | Yearly |

## Planning (2 to 3 weeks before)

1. **Objective:** what do we want to test? For example "Do we know who decides to take the online shop offline during ransomware?"
2. **Scenario:** realistic for your sector, based on recent threat intelligence.
3. **Participants:** SOC, IT operations, the system owner, CISO, communications, legal; executives for the business decisions.
4. **Injects:** 5 to 8 timed pieces of new information that force decisions.
5. **Facilitator and observers:** the facilitator runs it; observers note gaps; nobody is graded.

## Running it (90 minutes)

| Time | Step |
|---|---|
| 0 to 10 | Rules: no-fault, think out loud, "we would check X" is fine, say what you would actually do, not the ideal |
| 10 to 70 | Injects one by one; after each ask: who does what, who decides, who do we tell, what do we need that we do not have |
| 70 to 85 | Hot wash: what went well, what was unclear, what was missing |
| 85 to 90 | Actions with owners and dates |

## Three ready scenarios

### 1. Ransomware on a Friday night

| Time | Inject |
|---|---|
| 22:40 | EDR alerts: mass file renames on a file server, `.locked` extension |
| 22:55 | Service desk: users on night shift cannot open shared files |
| 23:20 | A ransom note found; the group claims to have copied 200 GB first |
| 00:10 | The backup server shows signs of access by the same admin account |
| 08:00 | A journalist emails asking about a leak-site post naming the company |

Decisions tested: isolate the network, who approves shutdown, backup integrity, legal and regulator notice, ransom policy, press statement.

### 2. CEO's mailbox forwarding to an outside address

| Inject |
|---|
| Finance received a payment change request "from the CEO" and paid 85,000 |
| Investigation finds an inbox rule forwarding to a free webmail address, created 12 days ago |
| Sign-in logs show logins from two countries; MFA push approved at 02:13 |
| The bank says recovery is possible only if reported within 24 hours |

Decisions tested: account containment for an executive, bank recall, who tells the CEO, scope of other mailboxes, police report.

### 3. Cloud keys leaked in a public repository

| Inject |
|---|
| A developer's public repository contains an access key with admin rights |
| Cloud billing alert: 40 large GPU instances started in an unused region |
| Audit logs show a new IAM user created by the leaked key |
| A storage bucket with customer exports was listed by the same key |

Decisions tested: key revocation without breaking production, cost containment, data exposure assessment, developer secret-handling process.

## Purple team follow-up

After a tabletop, test the detections for real:

```bash
# Atomic Red Team (PowerShell module), on a test host only
Invoke-AtomicTest T1486 -ShowDetailsBrief        # data encrypted for impact (simulated)
Invoke-AtomicTest T1114.003 -GetPrereqs          # email forwarding rule
Invoke-AtomicTest T1552.001 -TestNumbers 1       # credentials in files
```

| Tool | Best for |
|---|---|
| Atomic Red Team | Single techniques, quick detection checks |
| MITRE Caldera | Chained adversary emulation with agents |
| Infection Monkey | Lateral movement and network segmentation testing |

Record for each test: technique, expected alert, actual result (alerted, logged only, not seen), fix.

## Outputs

- [ ] Exercise report with gaps and actions
- [ ] Playbook and escalation matrix updates
- [ ] Detection gaps raised as detection requests
- [ ] Next exercise date and scenario

## Related pages

- [Tabletop exercise template](../09-templates/tabletop-exercise-template.md)
- [Post-incident review](post-incident-review.md)
- [IR lifecycle](ir-lifecycle.md)
- [SOC Training](../training/index.md)
