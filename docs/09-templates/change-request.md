# Change Request Template

Use this form before changing SOC tooling in production: SIEM rules, parsers, automation workflows, agents, integrations or blocking actions.

!!! abstract "At a glance"
    - Audience: SOC engineer / detection engineer (requester) / change approver / SOC lead
    - Time to complete: 15-30 minutes
    - Outcome: a change that is planned, tested, reversible and visible to the shift on duty

!!! tip "How to use"
    - Every change needs a tested rollback plan. If you cannot roll back, say so and raise the risk.
    - Tell the shift on duty before and after the change; they will see the side effects first.
    - Use a standard (pre-approved) change type for routine, low-risk work such as tuning one rule.
    - Attach the before and after configuration, or a link to the version-control commit.

---

## Change request: `<CHG-YYYY-NNNN>`

### Overview

| Field | Value |
|---|---|
| Title | `<...>` |
| Requested by | `<name, team>` |
| Change type | `<Standard / Normal / Emergency>` |
| Systems affected | `<SIEM / EDR / SOAR / collectors / firewall>` |
| Planned window | `<YYYY-MM-DD HH:MM-HH:MM UTC>` |
| Related records | `<DET-..., LSO-..., INC-...>` |

### Description and reason

> `<What will change and why. Link to the ticket that triggered it.>`

### Risk and impact

| Question | Answer |
|---|---|
| What could go wrong? | `<...>` |
| Detection blind spot during change? | `<Yes: how long / No>` |
| Expected alert noise | `<...>` |
| Risk level | `<Low / Medium / High>` |

### Implementation steps

| # | Step | Who | Check |
|---|---|---|---|
| 1 | `<...>` | `<...>` | `<...>` |

### Test and verification

- Pre-production test: `<where, result>`
- Post-change check: `<query or action and expected result>`

### Rollback plan

| # | Step | Time needed |
|---|---|---|
| 1 | `<...>` | `<...>` |

### Approval and closure

| Role | Name | Decision | Date |
|---|---|---|---|
| Approver | `<name>` | `<Approved / Rejected>` | `<date>` |
| Shift on duty informed | `<name>` | Acknowledged | `<date>` |
| Result | `<Successful / Rolled back / Partial>` | | `<date>` |

---

## Worked example

??? example "Filled-in change: CHG-2026-0291, Deploy email takeover detection"
    | Field | Value |
    |---|---|
    | Title | Deploy rule `det-email-0031` (risky sign-in then inbox rule) |
    | Requested by | Detection engineer |
    | Change type | Normal |
    | Systems | SIEM rule set, SOAR enrichment workflow |
    | Window | 2026-04-02 10:00-10:30 UTC |
    | Related | DET-2026-0144, PIR-2026-0007 |

    **Description:** add a correlation rule that alerts when a user signs in from a new country and creates a forwarding inbox rule within 60 minutes. Add an automation step that attaches the user's last 10 sign-ins to the alert.

    | Question | Answer |
    |---|---|
    | What could go wrong? | Query too heavy and slows other searches; unexpected alert volume |
    | Blind spot? | No, new rule, nothing removed |
    | Expected noise | 0-2 alerts per week |
    | Risk level | Low |

    | # | Step | Check |
    |---|---|---|
    | 1 | Merge rule from Git branch `det-email-0031` into main | Pipeline syntax check passes |
    | 2 | Deploy rule in enabled state, severity High | Rule visible in SIEM rule list |
    | 3 | Enable enrichment step in SOAR workflow | Workflow test run succeeds |
    | 4 | Run test with lab account `lab-user-07` | Alert fires within 10 minutes with sign-in history attached |

    **Rollback:** disable rule `det-email-0031` and revert commit (5 minutes); disable enrichment step (2 minutes).

    **Result:** approved by SOC lead 2026-04-01; night shift informed; deployed and verified 2026-04-02 10:22 UTC; test alert ALR-87990 closed as expected. Successful.

## Checklist

- [ ] Rollback plan written and realistic
- [ ] Blind spot during the change identified
- [ ] Shift on duty informed before and after
- [ ] Post-change verification done and recorded
- [ ] Configuration stored in version control

## Related pages

- [Detection request](detection-request.md)
- [Log source onboarding request](log-source-onboarding-request.md)
- [Shift handover template](shift-handover-template.md)
- [Templates overview](index.md)
