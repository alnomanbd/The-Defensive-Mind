# IOC Management

How to handle indicators of compromise (IOCs): the IPs, domains, hashes and other artefacts that mark an attack. The skill is not collecting indicators, anyone can download a million. The skill is deciding which to block, which to watch, and when to expire them, so your lists stay small, trusted and useful.

!!! abstract "At a glance"
    - Audience: SOC analyst L2/L3
    - Time to read: 10 minutes
    - Outcome: a method to store, score, apply and expire IOCs without poisoning your own alerts

## What an IOC is

An IOC (indicator of compromise) is an observable artefact linked to malicious activity.

| Type | Examples | Note |
|---|---|---|
| Network | IP address, domain, URL | IPs and domains change fast; they age quickly |
| File | SHA-256 hash, file name | Hashes are precise but attackers change files easily |
| Host | Registry key, mutex, service name, path | More durable; tied to a malware family's behaviour |
| Email | Sender address, subject, reply-to | Useful for a phishing campaign in progress |

!!! tip "Behaviour beats indicators"
    A single IP or hash is the weakest, most fleeting kind of detection; the attacker changes it in seconds. A detection for the **behaviour** (a process reading browser passwords, a login after failures) catches the next attack too. Use IOCs for fast blocking and enrichment, but invest most in behavioural detection ([Writing good detections](../05-detection-engineering/writing-good-detections.md)).

## Store IOCs with context, not as a bare list

An IOC with no context is a trap. The same IP can be a command-and-control server today and a shared cloud host tomorrow. Store fields that let you decide and expire.

| Field | Why it matters |
|---|---|
| Value and type | The indicator itself |
| Source | Where it came from, and how much you trust that source |
| Confidence | How sure you are it is malicious (high, medium, low) |
| First and last seen | When it was active; the basis for expiry |
| Context | What it is linked to (malware family, campaign, incident) |
| Action | Block, watch, or enrich-only |
| Expiry or review date | When to remove or recheck it |

A tool like MISP or OpenCTI stores all of this. A small team can start with a well-structured spreadsheet or a SIEM lookup table, as long as these fields are there.

## The key decision: block or watch?

This is the decision that keeps your SOC useful or breaks it. Blocking the wrong thing causes an outage; watching everything causes noise.

| Put it on the... | When | Effect |
|---|---|---|
| Blocklist | High confidence, low chance of false positive, and the harm of a wrong block is acceptable | Traffic to or from it is stopped automatically |
| Watchlist | Medium confidence, or a shared or dual-use indicator, or you want to see it before acting | It raises an alert; a human decides |
| Enrich-only | Low confidence or context-only | It adds context to alerts but neither blocks nor alerts on its own |

!!! danger "Never bulk-block a feed you have not vetted"
    Downloading a large threat feed and pushing it all to the firewall blocklist is how SOCs cause their own outages and block legitimate services. Feeds contain false positives, expired indicators, and shared infrastructure (a cloud IP that also serves your own apps). Load feeds as **watchlists** first, see what they hit, and promote only vetted indicators to blocking.

## Confidence and source scoring

Not all sources are equal. Score them so a low-trust feed cannot flood your blocklist.

- [ ] Rate each source for accuracy over time (does it produce false positives?).
- [ ] Give indicators from trusted, specific sources higher confidence than those from broad, automated feeds.
- [ ] Require higher confidence to block than to watch.
- [ ] Drop sources that repeatedly cause false positives; a noisy feed is worse than no feed.

## Expiry: the step everyone skips

IOCs rot. An IP that was a command-and-control server last month may be a normal cloud host now, reassigned to someone else. A blocklist that only grows will eventually block something it should not and bury real hits in dead entries.

| Indicator type | Typical expiry (tune to your sources) |
|---|---|
| IP address | Short, for example 30 to 90 days, unless re-confirmed |
| Domain | Medium, but recheck; domains get reassigned |
| URL | Short; URLs change constantly |
| File hash | Long or permanent; a hash is a specific file |
| Host artefact (registry, mutex) | Long; tied to malware behaviour |

- [ ] Set an expiry when you add an IOC, based on its type and source.
- [ ] Expire indicators automatically; review before removing high-value ones.
- [ ] Re-confirm an indicator to extend it, rather than keeping it forever by default.

## Applying IOCs in the SOC

| Use | How |
|---|---|
| Enrichment | Automatically check alert IOCs against your lists and add context ([Automation catalog](../07-automation-soar/automation-catalog.md)) |
| Watchlist alerting | Fire an alert when a watched indicator appears, for a human to triage |
| Blocking | Push vetted, high-confidence indicators to firewall, proxy, DNS filter or EDR |
| Retrospective hunt | When a new IOC arrives, search historical logs for past hits ([Threat hunting](../02-daily-operations/threat-hunting.md)) |

!!! tip "A new IOC is also a question about the past"
    When you learn an IP or hash is malicious, do not only block it going forward. Search your logs for the last 30 to 90 days: has it already been here? A new indicator often reveals an intrusion that started weeks ago.

## Sharing IOCs

Sharing indicators with trusted communities (an ISAC for your sector, a MISP community, partners) helps everyone see attacks sooner. Share carefully.

- [ ] Share only what you are allowed to, and strip anything sensitive or internal.
- [ ] Use a traffic light protocol (TLP) to mark how widely something can be shared.
- [ ] Give context, not just the bare indicator, so others can judge it.
- [ ] Take in shared IOCs as watchlists first, like any other feed.

## Keep your lists small and trusted

The goal is not the biggest IOC database; it is a small, current, trusted set that produces real hits and few false positives.

- [ ] Vet before blocking.
- [ ] Expire aggressively.
- [ ] Prefer behavioural detections over chasing indicators.
- [ ] Measure: how many real detections came from your IOCs, and how many false positives.

## Related pages

- [The Intelligence Lifecycle](ti-lifecycle.md)
- [Dark Web and Credential Monitoring](dark-web-and-credential-monitoring.md)
- [Writing good detections](../05-detection-engineering/writing-good-detections.md)
- [Threat hunting](../02-daily-operations/threat-hunting.md)
- [Automation catalog](../07-automation-soar/automation-catalog.md)
