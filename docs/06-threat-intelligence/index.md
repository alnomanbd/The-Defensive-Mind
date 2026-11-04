# Threat Intelligence

Threat Intelligence (TI) is information about threats that is checked, put in context and tied to an action: block, detect, patch or warn. This section gives a SOC (Security Operations Center) the daily procedures, free-source commands and alert rules to run TI with a small team.

!!! abstract "At a glance"
    - Audience: SOC analyst L1/L2/L3, SOC manager
    - Time to read: 5 minutes
    - Outcome: you know which TI jobs to run daily, weekly and monthly, which page holds each procedure, and what to set up first

## Pages in this section

| Page | Procedures inside | Owner |
|---|---|---|
| [The Intelligence Lifecycle](ti-lifecycle.md) | Requirements register, source scoring, weekly triage, monthly report, value metrics | SOC manager / L3 |
| [Dark Web and Credential Monitoring](dark-web-and-credential-monitoring.md) | Daily leak check with curl against free sources, masking rules, response workflow | L1 runs, L2 triages |
| [External Attack Surface Management](external-attack-surface-management.md) | Asset discovery, daily nmap diff, risky service list, cert expiry, CVE matching | L2 runs, L3 maintains |
| [IOC Management](ioc-management.md) | IOC fields, confidence and expiry, blocklist vs watchlist decision, MISP sharing | L2 / L3 |

## The SOC TI routine

| When | Task | Who | Time | Output |
|---|---|---|---|---|
| Daily 08:00 | Review overnight credential-exposure results | L1 | 15 min | Ticket per new exposure |
| Daily 08:15 | Review EASM change report (new ports, new hosts, certs < 14 days) | L1 -> L2 | 15 min | Ticket per real change |
| Daily | Enrich alert IOCs (IP, domain, hash) before escalating | L1 | Per alert | Enrichment note in ticket |
| Daily | Check new ransomware leak site posts for company, suppliers, customers | L1 | 5 min | Escalation if match |
| Weekly (Mon) | Known-exploited vulnerability catalogue vs asset inventory | L2 | 30 min | Patch tickets |
| Weekly | Expire old IOCs, review watchlist hits, promote/demote | L2 | 30 min | Updated lists |
| Weekly | Phishing reports from staff -> extract IOCs -> block/watch | L2 | 30 min | IOC entries |
| Monthly | TI summary for management (one page) | SOC manager | 2 h | Report |
| Quarterly | Review requirements and drop useless feeds | SOC manager + L3 | 2 h | Updated register |

## Setup order for a new team

Do these in order. Each step works without the next.

1. **Create the internet-facing asset list** (domains, subdomains, public IPs, cloud endpoints) with an owner per row. See [EASM](external-attack-surface-management.md).
2. **Turn on credential exposure checks** for every company email domain. See [Dark Web and Credential Monitoring](dark-web-and-credential-monitoring.md).
3. **Schedule a daily external scan** of your own ranges with diff-based alerts.
4. **Load two or three free feeds into the SIEM as watchlists**, not blocklists. See [IOC Management](ioc-management.md).
5. **Write the requirements register** (template in [lifecycle page](ti-lifecycle.md)) and kill any feed that serves no requirement.
6. **Automate** the daily checks and send results to the ticket queue. See [Automation catalogue](../07-automation-soar/automation-catalog.md).

!!! tip "Start with your own exposure"
    Leaked passwords, open admin ports and forgotten subdomains cause more real incidents in small and mid-size organisations than any named threat group. Cover them before buying attacker-tracking feeds.

## Quick enrichment cheat sheet for L1

Run these before escalating an unknown indicator. Never submit internal hostnames, customer data or private files to public services.

```bash
# What is exposed on a public IP (free, no key)
curl -s https://internetdb.shodan.io/203.0.113.10

# Certificates ever issued for a domain (free, no key)
curl -s "https://crt.sh/?q=example.com&output=json" | jq -r '.[].name_value' | sort -u

# WHOIS / registration age of a suspicious domain
whois suspicious-example.com | grep -iE 'creation|registrar'

# DNS records
dig +short A suspicious-example.com
dig +short MX suspicious-example.com
```

| Result | Meaning | Action |
|---|---|---|
| Domain registered < 30 days ago, used in email to staff | Likely phishing infrastructure | Escalate to L2, block sender domain |
| IP is a major cloud or CDN provider | Shared infrastructure; blocking IP hurts real users | Block URL/domain, not IP |
| IP on a known botnet C2 list and seen in outbound traffic | Probable infection | Escalate immediately, isolate host per playbook |
| No hits anywhere | Unknown, not clean | Add to watchlist 14 days, continue triage |

## Who does what

| Activity | L1 | L2 | L3 | SOC manager | IT / asset owner |
|---|---|---|---|---|---|
| Run daily checks | R | A | - | I | - |
| Triage credential leaks | R | A | C | I | C |
| Fix exposed services | I | C | C | I | R/A |
| Maintain IOC lists | - | R | A | I | - |
| Requirements and feed review | - | C | R | A | C |
| Monthly report | - | C | C | R/A | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

!!! warning "Common mistakes"
    - Loading every free feed straight into the firewall blocklist and breaking business traffic.
    - Running scans without written authorisation for the ranges.
    - Storing leaked passwords in tickets or chat.
    - Alerting on every persistent finding every day until analysts ignore the channel. Alert on change; report persistent items in a weekly digest.

## Checklist

- [ ] Internet-facing asset list exists, each row has an owner
- [ ] Daily credential exposure check scheduled
- [ ] Daily external scan with change alerts scheduled
- [ ] Feeds loaded as watchlists with expiry
- [ ] Requirements register approved
- [ ] Monthly TI report on the calendar

## Related pages

- [Credential leak / dark web playbook](../04-playbooks/credential-leak-dark-web.md)
- [Infostealer malware playbook](../04-playbooks/malware-infostealer.md)
- [Phishing playbook](../04-playbooks/phishing.md)
- [Automation catalogue](../07-automation-soar/automation-catalog.md)
- [Technology stack](../01-build-a-soc/technology-stack.md)
