# T11: DFIR

Digital forensics and incident response: collecting and analysing evidence so you can answer what happened, how, and what was touched, and so the answer stands up later. This module teaches the free tools and the discipline.

!!! abstract "At a glance"
    - Level: L3
    - Time: 8 to 10 hours with labs
    - Outcome: you can collect and analyse host, memory and log evidence with a defensible process

## Learning objectives

- [ ] Follow the order of volatility and a defensible chain of custody.
- [ ] Collect triage and memory evidence from Windows and Linux.
- [ ] Build a timeline from artefacts.
- [ ] Do basic memory, network and cloud forensics.
- [ ] Know your limits and when to call a specialist.

## Lessons

1. **Principles.** Order of volatility, integrity (hashing), chain of custody, minimal change.
2. **Collection.** Triage with KAPE, UAC and Velociraptor; memory with WinPmem and AVML; disk imaging.
3. **Timelines.** Building a timeline with Plaso and Timesketch; fast triage with Hayabusa and Chainsaw on Windows logs.
4. **Memory forensics.** Volatility basics: processes, connections, injected code.
5. **Network and cloud forensics.** What the logs preserve, and exporting them before retention removes them.
6. **Chain of custody.** Recording every hand that touches evidence, for HR, insurers or court.

## Lab

- [ ] Collect a triage package from a Windows VM with KAPE or Velociraptor.
- [ ] Capture memory from a lab VM with WinPmem and hash it.
- [ ] Build a timeline from the collection with Plaso or Hayabusa.
- [ ] Fill in a chain-of-custody record for each item (ID, collector, time, hash, storage).
- [ ] Write a short factual finding: what happened, with evidence references.

## Self-check

1. Why collect memory before rebooting or imaging the disk?
2. What three things must a chain-of-custody record always have?
3. When should you stop and call an outside forensic firm?

??? note "Answers"
    1. Memory holds the most volatile evidence (running processes, network state, keys, injected code) and is lost on reboot; the order of volatility says collect it first.
    2. At least: what the item is and its unique ID, who handled it and when, and its hash; plus every transfer with from, to, time and reason.
    3. When the case is likely to reach court or a tribunal, involves serious insider or criminal activity, or exceeds your skills or tooling; preserve evidence and hand over cleanly.

## Links to the handbook and kit

- [Evidence handling](../../03-incident-response/evidence-handling.md)
- [IR lifecycle](../../03-incident-response/ir-lifecycle.md)
- [Insider threat playbook](../../04-playbooks/insider-threat.md)

## Next module

[T12 Malware Analysis Basics](../t12-malware-analysis/index.md).
