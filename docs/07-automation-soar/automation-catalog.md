# Automation Catalog

Concrete automations to build, from easy and safe to advanced, with what each one does and how risky it is. Use this as a menu: pick the ones that fit your tools and risk appetite, and build the safe, high-value ones first.

!!! abstract "At a glance"
    - Audience: automation engineer, detection engineer, SOC lead
    - Time to read: 12 minutes
    - Outcome: a ranked list of workflows to build, with inputs, actions and risk

!!! tip "Read the order as a build plan"
    The catalog runs from safest and highest value (enrichment) to boldest (automated response). Build top-down. Each tier earns the trust to attempt the next.

## Tier 1: enrichment (safe, build first)

These only gather information. They change nothing, so they carry no risk and save the most analyst time.

| Workflow | What it does | Inputs | Output |
|---|---|---|---|
| IP enrichment | Reputation, geolocation, owner (ASN), is it a TOR or hosting node, is it on your block list | Source IP | A summary added to the alert |
| Domain and URL enrichment | Age, registrar, reputation, is it newly registered | Domain or URL | Verdict and context |
| File hash enrichment | Reputation lookup by hash (not uploading the file), known malware family | SHA-256 | Known-bad or unknown, with family |
| User context | Is this a real, enabled account; is the user on the leaver list; their department and manager; recent risky sign-ins | Username | A profile block on the alert |
| Host context | Owner, role (server or laptop), criticality, patch state, recent alerts | Hostname | A profile block on the alert |
| Asset and crown-jewel tagging | Mark alerts that touch important systems | Asset from the alert | A priority flag |

!!! note "Do not upload confidential files to public services"
    Enrich a file by its hash, not by uploading the file itself. Uploading a document to a public scanning service can leak confidential data. Hash lookups reveal nothing about the content.

## Tier 2: triage support (safe, build second)

These help the analyst decide faster but still leave the decision to a human.

| Workflow | What it does | Risk |
|---|---|---|
| Alert grouping and deduplication | Combine related alerts into one case ([Case deduplication](case-deduplication.md)) | None; it only groups |
| Auto-close known benign | Close alerts that exactly match a tight, approved benign pattern (your own scanner, a health check) | Low, if conditions are tight; measure what you close |
| Routing and assignment | Send the alert to the right queue or person by type and severity | None |
| Smart notification | Notify the right channel by severity, de-duplicated, not one message per event ([Alert fatigue](alert-fatigue-and-notifications.md)) | None |
| Open a case automatically | Create a case with enrichment already attached when an alert passes a threshold | Low |

## Tier 3: response with approval (build third)

These take action, but a human approves first. The automation does the slow part; the human makes the call.

| Workflow | Proposed action | Why approval |
|---|---|---|
| Suggested host isolation | Isolate a host through the EDR | A server could be production |
| Suggested account disable | Disable or force password reset | Could affect a real or senior user |
| Suggested IP block | Block a source at firewall or WAF, time-limited | Could hit a shared or partner range |
| Phishing response | Pull a reported email from all mailboxes, block the sender | Could remove a legitimate mail |
| Revoke sessions | Revoke tokens and sessions for a user | High value against token theft; confirm the user first |

The pattern: the workflow gathers evidence, decides a recommendation, and sends an approval request to an analyst (in chat or the case tool) with one click to proceed.

## Tier 4: full automation (build last, narrow scope)

Only for actions that are reversible, low-risk, and backed by a measured, trusted detection.

| Workflow | Action taken automatically | Safe because |
|---|---|---|
| Auto-isolate a laptop on high-confidence ransomware behaviour | EDR isolation of a workstation (not a server) | Reversible, and the cost of a wrong isolation of one laptop is small against ransomware spreading |
| Auto-block a confirmed-malicious IP from threat intel | Time-limited firewall block | Reversible, from a trusted feed, with good-range exclusions |
| Auto-quarantine a known-malware file | Quarantine (not delete) on a high-confidence match | Reversible |
| Auto-expire old blocks | Remove time-limited blocks when they lapse | Housekeeping, no risk |

!!! warning "Full automation is a small, carefully chosen set"
    Most SOCs fully automate only a handful of narrow, reversible actions. If you find yourself fully automating a business-affecting action on a detection you have not measured, stop and add an approval step. Speed is not worth an outage.

## A sensible build order

- [ ] Weeks 1 to 2: IP, domain, hash, user and host enrichment. Attach to every alert.
- [ ] Weeks 3 to 4: alert grouping, routing, smart notifications.
- [ ] Month 2: auto-close tight benign patterns; auto-open cases with enrichment.
- [ ] Month 3: response-with-approval for the top few actions (isolate, disable, block, phishing pull).
- [ ] Later: a small set of fully automated, reversible actions, each measured first.

## Related pages

- [SOAR principles](soar-principles.md)
- [Case deduplication](case-deduplication.md)
- [Alert fatigue and notifications](alert-fatigue-and-notifications.md)
- [Playbooks](../04-playbooks/index.md)
