# Tabletop Exercise Template

Use this template to plan, run and report a discussion-based incident drill where people talk through a scenario instead of touching live systems.

!!! abstract "At a glance"
    - Audience: SOC lead / exercise facilitator / responders and managers
    - Time to complete: 2-4 hours to plan, 90-120 minutes to run
    - Outcome: a tested playbook, clear roles and a list of gaps with owners

!!! tip "How to use"
    - Pick **one** scenario and **three to five** objectives. Too many objectives and the drill loses focus.
    - Release information in injects (timed updates) so players must make decisions with incomplete facts.
    - Assign a note taker who records decisions, delays and questions nobody could answer.
    - Treat gaps found as success. Feed actions into the same tracker as post-incident reviews.

---

## Tabletop exercise: `<TTX-YYYY-NN>`, `<scenario name>`

### Planning

| Field | Value |
|---|---|
| Date, time, duration | `<YYYY-MM-DD HH:MM, 90 min>` |
| Facilitator | `<name>` |
| Note taker | `<name>` |
| Participants | `<roles: SOC L1/L2/L3, IT ops, legal, communications, management>` |
| Playbook(s) under test | `<name>` |
| Ground rules | No blame; assume tools work as they do today; "I don't know" is a valid answer |

### Objectives

| # | Objective | How we will know it was met |
|---|---|---|
| 1 | `<...>` | `<...>` |

### Scenario background

> `<Starting situation, two to four sentences.>`

### Injects

| # | Time | Inject (what players learn) | Questions for players | Expected response |
|---|---|---|---|---|
| 1 | `<T+0>` | `<...>` | `<...>` | `<...>` |
| 2 | `<T+15>` | `<...>` | `<...>` | `<...>` |

### Results

| Objective | Met? | Notes |
|---|---|---|
| `<1>` | `<Yes / Partly / No>` | `<...>` |

| Gap found | Action | Owner | Due date |
|---|---|---|---|
| `<...>` | `<...>` | `<...>` | `<...>` |

---

## Worked example

??? example "Filled-in exercise: TTX-2026-02, Ransomware on a file server"
    **Participants:** SOC L1, L2, L3; IT operations lead; backup administrator; legal counsel; communications manager; CISO.

    | # | Objective | Measure |
    |---|---|---|
    | 1 | Decide on network isolation within 30 minutes of confirmation | Decision time recorded |
    | 2 | Confirm who may approve shutting down a business system | Named role agreed |
    | 3 | Validate that backups can be restored and are not encrypted | Backup admin explains steps and evidence |
    | 4 | Draft the first internal message | Text agreed in the room |

    **Background:** Monday 07:30. The help desk receives five calls: shared drive files have a new extension and a ransom note appears in each folder.

    | # | Time | Inject | Questions | Expected response |
    |---|---|---|---|---|
    | 1 | T+0 | EDR alert: mass file rename on `fs-02.example.com` by service account `svc-sync` | Who leads? First three actions? | L2 declares Critical incident, isolates fs-02 via EDR, disables `svc-sync` |
    | 2 | T+15 | SIEM shows `svc-sync` logged on to 12 more servers overnight from `ws-0310` | Widen scope? | Isolate ws-0310, hunt for the same logons, consider blocking server-to-server SMB |
    | 3 | T+30 | Backup console shows last night's job failed | Recovery options? | Use previous good backup, check backups are offline or immutable |
    | 4 | T+45 | A journalist emails asking about "a cyber attack" | Who answers, what is said? | Communications uses holding statement, legal reviews notification duties |
    | 5 | T+60 | Attacker leak site lists ACME with a sample file | Pay or not? Who decides? | Escalate to executive crisis team per policy; engage law enforcement guidance |

    | Objective | Met? | Notes |
    |---|---|---|
    | 1 | Yes | Isolation decided at T+8 |
    | 2 | No | Nobody knew who can approve shutting down the ERP system |
    | 3 | Partly | Restore steps known; immutability of backups unverified |
    | 4 | Yes | Message drafted in 10 minutes |

    | Gap found | Action | Owner | Due |
    |---|---|---|---|
    | No authority to shut down business systems | Add decision rights table to crisis plan | CISO | 2026-05-30 |
    | Backup immutability unknown | Test restore and immutability, report evidence | Backup admin | 2026-05-15 |
    | Service account logs on interactively to servers | Restrict `svc-sync` logon rights; add detection | IT ops / detection engineering | 2026-05-20 |

## Checklist

- [ ] One scenario, three to five objectives
- [ ] Injects timed with expected responses
- [ ] Decision makers present, not only technical staff
- [ ] Gaps logged with owners and due dates
- [ ] Report shared within one week

## Related pages

- [Post-incident review template](post-incident-review-template.md)
- [Playbook template](../04-playbooks/playbook-template.md)
- [Templates overview](index.md)
