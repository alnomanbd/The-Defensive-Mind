# T07: Threat Intelligence

Threat intelligence is information about threats that is checked, put in context and tied to an action. This module teaches the models, the lifecycle, and how to run intelligence with a small team so it actually changes what you detect and block.

!!! abstract "At a glance"
    - Level: L2 to L3
    - Time: 6 to 8 hours with labs
    - Outcome: you can run the intelligence lifecycle and apply intel to detection and response

## Learning objectives

- [ ] Run the intelligence lifecycle from requirements to feedback.
- [ ] Use the core models: Cyber Kill Chain, Diamond Model, MITRE ATT&CK, Pyramid of Pain.
- [ ] Score sources and indicators by confidence.
- [ ] Use STIX and TAXII, MISP and OpenCTI to store and share intel.
- [ ] Write a short, useful intelligence report.

## Lessons

1. **What intelligence is, and is not.** Context and action, not a feed of raw indicators.
2. **The lifecycle.** Requirements, collection, processing, analysis, dissemination, feedback.
3. **Models.** The Cyber Kill Chain (stages of an attack), the Diamond Model (adversary, capability, infrastructure, victim), ATT&CK (techniques), the Pyramid of Pain (which indicators hurt the attacker most to lose).
4. **Requirements first.** Deciding what you actually need to know before collecting anything.
5. **Sources and confidence.** Scoring feeds and indicators so a weak source cannot flood your lists.
6. **Standards and tools.** STIX and TAXII for sharing, MISP and OpenCTI for storing and enriching.
7. **Writing intel.** Short, relevant, action-oriented reports a busy reader will use.

## Lab

- [ ] Write three intelligence requirements for a fictional company (what must the SOC know?).
- [ ] Stand up MISP (or use a demo instance); load a free feed as a watchlist.
- [ ] Take one indicator and add context: source, confidence, expiry, action.
- [ ] Map a recent public attack to the Cyber Kill Chain and ATT&CK.
- [ ] Write a half-page intel note with a clear recommended action.

## Self-check

1. Why do requirements come before collection?
2. What does the Pyramid of Pain tell you about which indicators to invest in?
3. What makes an intel report useful rather than just interesting?

??? note "Answers"
    1. Without requirements you collect everything and drown; requirements focus collection on what will actually change a decision.
    2. Indicators at the top (tools, tactics, techniques) hurt the attacker far more to change than hashes and IPs at the bottom; detecting behaviour beats chasing fleeting indicators.
    3. It is relevant to a real decision, in context, with a clear recommended action and confidence, and short enough to be read.

## Links to the handbook and kit

- [The Intelligence Lifecycle](../../06-threat-intelligence/ti-lifecycle.md)
- [IOC management](../../06-threat-intelligence/ioc-management.md)
- [Dark Web and Credential Monitoring](../../06-threat-intelligence/dark-web-and-credential-monitoring.md)

## Next module

[T08 Threat Hunting](../t08-threat-hunting/index.md).
