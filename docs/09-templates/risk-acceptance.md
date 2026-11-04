# Risk Acceptance Template

Use this form when a security gap found by the SOC cannot be fixed now and a business owner formally accepts the risk for a limited time.

!!! abstract "At a glance"
    - Audience: SOC lead (raises it) / risk owner and CISO (approve)
    - Time to complete: 20-40 minutes
    - Outcome: a signed, time-limited decision with compensating controls the SOC can monitor

!!! tip "How to use"
    - The **risk owner** must be the business person who benefits from the system, not the SOC.
    - Every acceptance has an expiry date (typically 3-12 months). No open-ended acceptances.
    - List the compensating controls the SOC will monitor, and alert on them.
    - Record the acceptance in the risk register and review it before expiry.

!!! warning "What cannot be accepted"
    Follow your policy, but typical exclusions are: breaking a law or regulation, exposing card or health data without controls, and internet-facing systems with known exploited vulnerabilities.

---

## Risk acceptance: `<RA-YYYY-NNNN>`

### Summary

| Field | Value |
|---|---|
| Title | `<short title>` |
| Raised by | `<name, role>` |
| Risk owner | `<name, business role>` |
| Date raised | `<YYYY-MM-DD>` |
| Expiry date | `<YYYY-MM-DD>` |
| Related findings | `<vulnerability ID, audit finding, incident ID>` |

### Description of the gap

| Field | Value |
|---|---|
| What is the weakness? | `<...>` |
| Affected assets | `<hosts, applications, users>` |
| Why it cannot be fixed now | `<cost, vendor dependency, business deadline>` |
| Planned permanent fix | `<what, who, by when>` |

### Risk rating

| Factor | Rating | Reason |
|---|---|---|
| Likelihood | `<Low / Medium / High>` | `<...>` |
| Impact | `<Low / Medium / High>` | `<...>` |
| Inherent risk (no controls) | `<...>` | |
| Residual risk (with compensating controls) | `<...>` | |

### Compensating controls

| Control | Owner | How the SOC monitors it | Evidence |
|---|---|---|---|
| `<...>` | `<...>` | `<detection rule / periodic check>` | `<...>` |

### Conditions that cancel this acceptance

- `<e.g. public exploit released, incident on the asset, scope change>`

### Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Risk owner | `<name>` | `<Accept / Reject>` | `<date>` |
| CISO | `<name>` | `<Accept / Reject>` | `<date>` |
| SOC lead (informed) | `<name>` | Acknowledged | `<date>` |

---

## Worked example

??? example "Filled-in acceptance: RA-2026-0009, Legacy payroll server without EDR"
    | Field | Value |
    |---|---|
    | Title | Legacy payroll server cannot run the EDR agent |
    | Raised by | SOC lead |
    | Risk owner | Head of Finance |
    | Date raised | 2026-02-10 |
    | Expiry date | 2026-08-31 |
    | Related findings | Coverage gap report Jan 2026, item 7 |

    **Weakness:** `payroll-01.example.com` runs an old operating system the EDR agent does not support. Malware or hands-on-keyboard activity on it would not be seen by EDR. **Why not fixed:** payroll vendor certifies only this OS until the new platform goes live. **Permanent fix:** migrate to new payroll platform by 2026-08-15 (Finance IT project PR-114).

    | Factor | Rating | Reason |
    |---|---|---|
    | Likelihood | Medium | Server not internet-facing, but reachable from 40 finance workstations |
    | Impact | High | Holds salary and bank data for all staff |
    | Inherent risk | High | |
    | Residual risk | Medium | After controls below |

    | Control | Owner | How the SOC monitors it |
    |---|---|---|
    | Firewall allows only 3 named jump hosts to reach the server | Network team | SIEM alert on any other source connecting (rule `net-0412`) |
    | Operating system logs sent to SIEM | Infrastructure | Log source health alert if silent for 30 minutes |
    | File integrity monitoring on payroll folders and system binaries | Infrastructure | High-severity alert on change outside the monthly payroll window |
    | Monthly vulnerability scan | Vulnerability management | Results in monthly SOC report |

    **Cancels if:** a remotely exploitable vulnerability is published for this OS, or any security incident touches the server.

    **Approved:** Head of Finance and CISO on 2026-02-14. Review reminder set for 2026-08-01.

## Checklist

- [ ] Risk owner is a business owner, not the SOC
- [ ] Expiry date set and in the risk register
- [ ] Each compensating control has an SOC monitoring method
- [ ] Cancellation conditions written
- [ ] Review reminder scheduled before expiry

## Related pages

- [Monthly SOC report](monthly-soc-report.md)
- [Change request template](change-request.md)
- [Templates overview](index.md)
