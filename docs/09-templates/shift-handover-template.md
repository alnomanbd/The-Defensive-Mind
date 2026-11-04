# Shift Handover Template

A template for passing open work from one SOC shift to the next so that nothing is dropped between people.

!!! abstract "At a glance"
    - Audience: SOC analyst / shift lead
    - Time to read: 3 minutes (10-15 minutes to complete per shift)
    - Outcome: the incoming shift knows exactly what is open, what is urgent and what to watch

!!! tip "How to use"
    - Fill the template during the last 30 minutes of the shift, not after it ends.
    - Do a short live handover (call or in person) and walk through the "Needs action" items.
    - The incoming analyst confirms receipt by signing at the bottom.
    - Link to tickets instead of copying their content; the ticket stays the source of truth.
    - Store handovers in one place so anyone can read the last 7 days.

---

## Shift handover: `<YYYY-MM-DD>` `<Day / Night / Shift name>`

### Shift details

| Field | Value |
|---|---|
| Shift window | `<HH:MM-HH:MM UTC>` |
| Outgoing analyst(s) | `<names>` |
| Incoming analyst(s) | `<names>` |
| Shift lead / on-call escalation | `<name, contact method>` |
| Overall status | `<Green: normal / Amber, elevated / Red, active major incident>` |

### Needs action from incoming shift

| Priority | Ticket | Summary | Next step | Deadline (UTC) |
|---|---|---|---|---|
| `<P1>` | `<INC-...>` | `<Possible account takeover, user jdoe>` | `<Confirm with user's manager, then reset>` | `<HH:MM>` |
| `<P2>` | `<ALR-...>` | `<...>` | `<...>` | `<...>` |

### Open incidents

| Incident ID | Severity | Status | Lead | Last update |
|---|---|---|---|---|
| `<INC-...>` | `<High>` | `<Containment>` | `<name>` | `<what changed this shift>` |

### Alert queue status

| Queue | Open at start | New this shift | Closed this shift | Open at end | Oldest open (age) |
|---|---|---|---|---|---|
| `<SIEM>` | `<n>` | `<n>` | `<n>` | `<n>` | `<hh:mm>` |
| `<EDR>` | `<n>` | `<n>` | `<n>` | `<n>` | `<hh:mm>` |
| `<Email reports>` | `<n>` | `<n>` | `<n>` | `<n>` | `<hh:mm>` |

### Watch list

Things that are not incidents yet but need attention.

| Item | Why it matters | What to watch for |
|---|---|---|
| `<Host srv-app-03.example.com>` | `<Unusual outbound traffic earlier>` | `<Any connection to 203.0.113.0/24>` |
| `<Noisy rule "<rule name>">` | `<Flooding queue>` | `<Tuning ticket <DET-...> in progress>` |

### Tooling and log source health

| Component | Status | Notes |
|---|---|---|
| SIEM ingestion | `<OK / Degraded / Down>` | `<e.g. firewall logs delayed 20 min>` |
| Endpoint Detection and Response (EDR) console | `<OK>` | `<...>` |
| Case management | `<OK>` | `<...>` |
| Automation / SOAR (Security Orchestration, Automation and Response) | `<OK>` | `<...>` |
| Known missing log sources | `<...>` | `<ticket>` |

### Changes and maintenance

| Time (UTC) | Change | Expected effect on alerts | Change ID |
|---|---|---|---|
| `<HH:MM>` | `<Firewall upgrade at site B>` | `<Link-down alerts expected>` | `<CHG-...>` |

### Escalations and communications this shift

| Time (UTC) | To whom | Topic | Response |
|---|---|---|---|
| `<HH:MM>` | `<IT on-call>` | `<Request to block domain>` | `<Done at HH:MM>` |

### Notes

> `<Anything else: threat intel bulletin received, VIP travel, planned phishing test, staff absence.>`

### Handover confirmation

| Role | Name | Time (UTC) |
|---|---|---|
| Outgoing analyst | `<name>` | `<HH:MM>` |
| Incoming analyst | `<name>` | `<HH:MM>` |

---

## Worked example

??? example "Filled-in handover: 2026-05-09 Night shift (22:00-06:00 UTC)"
    **Overall status:** Amber, one open High incident.

    | Priority | Ticket | Summary | Next step | Deadline (UTC) |
    |---|---|---|---|---|
    | P1 | INC-2026-0051 | ws-0217 isolated after EDR flagged credential dumping tool | Collect memory image with DFIR tool, then hand to L3 | 08:00 |
    | P2 | ALR-88412 | 40 failed VPN logins for svc-backup from 203.0.113.77 | Ask IT if account is still used; if not, disable | 09:00 |
    | P3 | ALR-88430 | User reported suspicious email (no click) | Purge email from all mailboxes, add sender to block list | 12:00 |

    | Queue | Open at start | New | Closed | Open at end | Oldest |
    |---|---|---|---|---|---|
    | SIEM | 14 | 63 | 70 | 7 | 2 h 10 min |
    | EDR | 2 | 5 | 6 | 1 | 0 h 40 min |

    **Watch list:** srv-db-02.example.com showed 3 GB outbound at 02:10, matched a backup job (CHG-2026-0310), but confirm with the database team. Rule "PowerShell encoded command" fired 22 times on the patch server; tuning ticket DET-2026-0144 open.

    **Tool health:** SIEM ingestion OK; firewall logs 15 minutes behind since 04:00, SIEM team notified (ticket OPS-5512). EDR OK. Case management OK.

    **Changes:** 07:00 UTC, core switch firmware upgrade at site B (CHG-2026-0318); expect device-down alerts for 20 minutes.

    **Confirmed:** outgoing A. Analyst 05:55; incoming B. Analyst 06:05 after live walk-through.

## Good handover habits

| Do | Avoid |
|---|---|
| Write the next concrete step for each item | "Look into this" without context |
| State deadlines in UTC | Local time without a zone |
| Mention planned changes that create noise | Letting the next shift chase expected alerts |
| Hand over half-finished containment live | Leaving containment steps only in a note |

## Checklist

- [ ] Every "Needs action" item has a next step and deadline
- [ ] Open incidents list matches the case management tool
- [ ] Tool health checked, not assumed
- [ ] Live walk-through done
- [ ] Incoming analyst confirmed receipt

## Related pages

- [Incident report template](incident-report.md)
- [Change request template](change-request.md)
- [Monthly SOC report](monthly-soc-report.md)
- [Templates overview](index.md)
