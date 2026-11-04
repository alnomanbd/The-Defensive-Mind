# Log Source Onboarding Request Template

Use this form when a system needs to send its logs to the Security Information and Event Management (SIEM) platform. The system owner fills in the top part; SIEM engineering completes the rest.

!!! abstract "At a glance"
    - Audience: system owner (requester) / SIEM engineer / SOC lead
    - Time to complete: 20 minutes
    - Outcome: logs arrive parsed, on time and with known volume, and someone notices when they stop

!!! tip "How to use"
    - State **why** the logs are needed: which detections or investigations depend on them.
    - Give a realistic daily volume; it drives licence and storage cost.
    - Never close the request until a test event is visible and parsed in the SIEM.
    - Add a "log source silent" health alert for every new source.

---

## Log source onboarding: `<LSO-YYYY-NNNN>`

### Requester section

| Field | Value |
|---|---|
| System name and purpose | `<...>` |
| System owner | `<name, team>` |
| Hostnames / tenant | `<...>` |
| Environment | `<Production / Test>` |
| Asset criticality | `<Critical / High / Medium / Low>` |
| Reason | `<Detection use case / audit requirement / incident follow-up>` |
| Related record | `<PIR-..., DET-..., audit finding>` |

### Log details

| Field | Value |
|---|---|
| Log types | `<authentication, admin actions, system, application, network>` |
| Format | `<Syslog / JSON / Windows Event Log / CSV / API>` |
| Delivery method | `<Agent / Syslog over TLS / API pull / Cloud storage bucket>` |
| Time zone and clock source | `<UTC, NTP server>` |
| Estimated volume | `<events per second / GB per day>` |
| Sensitive data in logs? | `<passwords, personal data: masking needed?>` |

### SIEM engineering section

| Field | Value |
|---|---|
| Collector / agent | `<...>` |
| Parser / data model mapping | `<...>` |
| Index / data stream and retention | `<...>` |
| Network rules opened | `<source, destination, port, change ID>` |
| Test event confirmed (time, query) | `<...>` |
| Silent source alert configured | `<Yes: threshold>` |
| Detections enabled | `<rule IDs>` |
| Status | `<Requested / In progress / Live / Rejected>` |

---

## Worked example

??? example "Filled-in request: LSO-2026-0023, Web proxy logs"
    | Field | Value |
    |---|---|
    | System | Forward web proxy for all staff browsing |
    | Owner | Network team |
    | Hosts | `proxy-01.example.com`, `proxy-02.example.com` |
    | Criticality | High |
    | Reason | PIR-A3 for INC-2026-0042: could not trace phishing page visits beyond 7 days |
    | Log types | Access logs: user, source IP, URL, category, action, bytes |
    | Format / delivery | Syslog over TLS (TCP 6514) to SIEM collector |
    | Time | UTC, internal NTP |
    | Volume | About 350 events per second at peak, 18 GB per day |
    | Sensitive data | URLs may contain tokens in query strings, mask `token=` and `session=` values |

    | SIEM engineering | Value |
    |---|---|
    | Collector | `collector-02.example.com`, syslog input 6514 |
    | Parser | Proxy parser mapped to common web fields (`url.full`, `user.name`, `source.ip`, `event.action`) |
    | Retention | 90 days searchable, 12 months archive |
    | Network | proxy-01/02 -> collector-02 TCP 6514, CHG-2026-0302 |
    | Test | 2026-04-08 10:14 UTC, search `source=proxy user=testuser1` returned 42 parsed events |
    | Silent alert | Alert if no events for 15 minutes in business hours |
    | Detections | `web-0007` newly registered domains, `web-0012` uploads over 100 MB to personal storage |
    | Status | Live 2026-04-08 |

## Checklist

- [ ] Purpose and detections linked to the request
- [ ] Volume estimated and storage approved
- [ ] Sensitive fields masked before indexing
- [ ] Test event visible and parsed
- [ ] Silent-source health alert in place
- [ ] Log source register updated

## Related pages

- [Detection request](detection-request.md)
- [Change request template](change-request.md)
- [Open-source SOC lab](../10-labs-and-tools/open-source-soc-lab.md)
- [Templates overview](index.md)
