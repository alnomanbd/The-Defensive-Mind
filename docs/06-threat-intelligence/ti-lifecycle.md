# The Intelligence Lifecycle

The lifecycle is a loop: decide what you need, collect it, clean it, judge what it means, deliver it, ask if it helped. This page turns each phase into a concrete SOC procedure with templates, commands and metrics.

!!! abstract "At a glance"
    - Audience: SOC manager, L3 / TI analyst, L2
    - Time to read: 12 minutes
    - Outcome: you can run a requirements register, score sources, process feeds safely, report at three levels and prove value with numbers

## The loop as SOC tasks

| Phase | SOC task | Frequency | Owner | Artefact |
|---|---|---|---|---|
| Direction | Maintain the requirements register | Quarterly | SOC manager | `ti-requirements.xlsx` / wiki table |
| Collection | Run feeds, scans, leak checks; pull internal data | Daily | L1 / automation | Raw results folder or index |
| Processing | Normalise, dedupe, filter, tag, set expiry | Daily (automated) | L2 / automation | Clean IOC list |
| Analysis | Decide relevance and action | Daily / per finding | L2 / L3 | Ticket with assessment |
| Dissemination | Push to SIEM, WAF, tickets, reports | Continuous / monthly | L2 / SOC manager | Rules, blocks, report |
| Feedback | Measure hits, ask consumers, drop sources | Quarterly | SOC manager | Updated register |

## Direction: the requirements register

Copy this table. Keep 5-15 rows. Every source and every daily check must point to a row.

| ID | Question | Consumer | Level | Sources | Action when answered | Review |
|---|---|---|---|---|---|---|
| PIR-01 | Are credentials for our domains exposed or for sale? | SOC, identity team | Tactical | Breach services, infostealer lookups | Reset, revoke sessions, check logins | Quarterly |
| PIR-02 | What did we expose to the internet since yesterday? | SOC, infra | Tactical | Own scans, crt.sh, DNS | Ticket to owner | Quarterly |
| PIR-03 | Are we, a supplier or a customer named on ransomware leak sites? | SOC manager, legal | Operational | Leak site trackers | Incident / supplier risk process | Quarterly |
| PIR-04 | Which actively exploited CVEs hit software we run? | Vuln mgmt, IT | Operational | Known-exploited catalogue, vendor advisories | Emergency patch ticket | Quarterly |
| PIR-05 | Which phishing themes reach our staff? | SOC, awareness | Operational | Staff reports, mail gateway | Block + awareness note | Quarterly |
| PIR-06 | Are lookalike domains registered against our brand? | SOC, legal | Tactical | Cert transparency, registration feeds | Takedown request, block | Quarterly |
| PIR-07 | What are the top threats to our sector this year? | Management | Strategic | Sector reports, own incidents | Budget / roadmap input | Yearly |

## Collection: score every source

Score each source 1-3 on four criteria. Drop anything under 7 after 90 days.

| Criterion | 1 | 2 | 3 |
|---|---|---|---|
| Relevance | Rarely about our tech/sector | Sometimes | Often maps to a requirement |
| Timeliness | Days to weeks late | Within a day | Hours |
| Accuracy | Frequent false positives | Occasional | Rare |
| Actionability | Raw data, no context | Some context | Ready to block/detect |

Example free collection commands (check each provider's terms before automating):

```bash
# Known-exploited vulnerabilities catalogue (public JSON)
curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json \
  | jq -r '.vulnerabilities[] | select(.dateAdded >= "2026-10-20")
           | [.cveID, .vendorProject, .product, .dueDate] | @tsv'

# Botnet C2 IP blocklist (abuse.ch Feodo Tracker, plain text)
curl -s https://feodotracker.abuse.ch/downloads/ipblocklist.txt | grep -v '^#' > feodo-$(date +%F).txt

# Certificates issued for your domain in the last day (watch for lookalikes / unknown hosts)
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | jq -r '.[] | select(.entry_timestamp >= "2026-10-26") | .name_value' | sort -u
```

## Processing: the cleaning pipeline

Run these steps, in this order, before anything reaches a blocklist or SIEM.

1. **Normalise:** lowercase domains, strip `http://` and paths where you need the domain only, defang/refang consistently (`hxxp`, `[.]`).
2. **Deduplicate** across feeds; keep the earliest first-seen and the latest last-seen.
3. **Filter allow-list:** remove private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), your own public ranges, major public DNS resolvers, big CDN and cloud ranges, top-ranked popular domains.
4. **Tag:** source, first-seen, confidence, TLP, related requirement ID.
5. **Expire:** set `valid_until` (see [IOC Management](ioc-management.md)).

```bash
# Minimal filter example: drop private and own ranges from an IP list
grep -vE '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|203\.0\.113\.)' raw-ips.txt \
  | sort -u > clean-ips.txt
wc -l raw-ips.txt clean-ips.txt
```

!!! danger "Never skip the allow-list"
    One CDN address in a firewall blocklist can take down your own website, email or payment provider. Every automated block feed must pass an allow-list filter first.

## Analysis: the four-line assessment

Every TI ticket must contain these four lines. L1 can fill 1-2; L2 completes 3-4.

```text
WHAT:       New certificate for vpn-acme-login.example.net issued 2026-10-26 (crt.sh)
SO WHAT:    Lookalike of our VPN portal; likely credential phishing against staff
CONFIDENCE: Moderate - name matches brand, registered 2 days ago, no content yet
ACTION:     Block domain on proxy and mail gateway; watch DNS logs 30 days; legal for takedown
```

| Confidence | Use when |
|---|---|
| High | Confirmed by our own logs or two independent reliable sources |
| Moderate | One reliable source, consistent with what we see |
| Low | Single unverified source or indirect evidence |

## Dissemination: right format per audience

| Audience | Format | Channel | Frequency |
|---|---|---|---|
| L1/L2 analysts | Watchlists, detection rules, enrichment | SIEM, case tool | Continuous |
| System owners | Ticket with fix and deadline | Ticketing system | As found |
| SOC manager | Weekly digest of persistent findings | Email / chat | Weekly |
| Management | One-page summary | Report | Monthly |
| Board | Risk statement in business terms | Slide | Quarterly |
| All staff | Short scam warning | Email / intranet | When relevant |

Mark everything with the Traffic Light Protocol (TLP): RED (named people only), AMBER (inside the organisation), GREEN (community), CLEAR (public).

Monthly report outline (one page):

1. Headline: top three things that changed this month.
2. Exposures found and fixed (counts, median days to fix, oldest open item).
3. Credential exposures (new accounts affected, all reset Y/N).
4. Threats seen against us (phishing themes, blocked campaigns).
5. Decisions needed from management.

## Strategic, operational, tactical: what to produce

| Level | Example product | Who writes | Shelf life |
|---|---|---|---|
| Strategic | "Stolen remote-access logins are the main ransomware entry route in our sector; finish MFA on VPN this quarter." | SOC manager | Months |
| Operational | "Invoice-themed HTML attachments are hitting finance; here is the detection and an awareness note." | L3 | Weeks |
| Tactical | Sender domains, hashes, URLs pushed to mail gateway and SIEM | L2 | Days |

## Free vs paid: decision table

| Situation | Choose |
|---|---|
| Team under 3 analysts, no processes yet | Free sources only for 3 months; measure hits |
| Free sources miss infostealer logs you know exist | Paid credential/infostealer monitoring |
| You need monitoring of closed criminal forums | Paid (vendor carries legal and access risk) |
| Leadership asks for sector threat briefings | Sector ISAC membership before a commercial feed |
| You cannot integrate what you already have | Do not buy; fix processing first |

## Feedback: value metrics

| Metric | How to count | Target |
|---|---|---|
| TI-driven detections/blocks per month | Tickets tagged `source:ti` closed as true positive | Rising |
| TI alert true-positive rate | TP / all TI alerts | > 50% |
| Exposures found before abuse | Leaks + open services found by TI with no linked incident | Rising, then stable |
| Median days exposure -> fix | Ticket open -> close | < 7 days (critical < 2) |
| Feeds with zero useful hits in 90 days | From source scores | 0 (remove them) |
| Cost per useful finding | (Licences + analyst hours) / useful findings | Falling |

!!! warning "Common mistakes"
    - Collecting before writing requirements.
    - Reporting volumes ("2 million IOCs") instead of outcomes.
    - Same report for analysts and executives.
    - Never removing a feed.

## Checklist

- [ ] Requirements register with owners and review dates
- [ ] Every source scored and mapped to a requirement
- [ ] Allow-list filter in front of every automated block
- [ ] Every TI ticket has WHAT / SO WHAT / CONFIDENCE / ACTION
- [ ] Monthly one-page report delivered
- [ ] Value metrics reviewed quarterly

## Related pages

- [Threat Intelligence overview](index.md)
- [IOC Management](ioc-management.md)
- [Dark Web and Credential Monitoring](dark-web-and-credential-monitoring.md)
- [External Attack Surface Management](external-attack-surface-management.md)
- [Incident response lifecycle](../03-incident-response/ir-lifecycle.md)
- [Automation catalogue](../07-automation-soar/automation-catalog.md)
