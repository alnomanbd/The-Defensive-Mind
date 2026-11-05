# Useful Resources

Good external material to learn from and build on: frameworks, detection rule libraries, free training, and communities. Pointers, not copies. These are widely used references in the security community; check each for its own current terms before you rely on it.

!!! abstract "At a glance"
    - Audience: everyone building SOC skills or a SOC
    - Time to read: use it as a reference
    - Outcome: you know where to go for frameworks, rules, practice and community

!!! note "Verify before you depend on anything"
    Tools, projects and training move, change licence, or go stale. Treat every pointer here as a starting point, check its current state and terms, and prefer official sources. Nothing here is an endorsement or a guarantee.

## Frameworks and knowledge bases

| Resource | What it gives you |
|---|---|
| MITRE ATT&CK | The catalogue of attacker tactics and techniques; the backbone of coverage mapping |
| MITRE ATT&CK Navigator | A free tool to visualise your detection coverage as a heatmap |
| MITRE D3FEND | A companion that maps defensive techniques |
| NIST Cybersecurity Framework | A high-level framework for organising a security programme |
| CIS Controls | A prioritised list of practical security controls |
| The Pyramid of Pain | A model for how much it hurts an attacker to lose each kind of indicator |

## Detection rules and content

| Resource | What it gives you |
|---|---|
| Sigma | An open, portable detection-rule format and a large community rule repository |
| Sigma converters (sigma-cli, pySigma) | Turn a Sigma rule into your SIEM's query language |
| YARA | A standard for writing rules to identify files and malware |
| Atomic Red Team | Small, safe tests mapped to ATT&CK techniques, to prove detections work |
| MITRE Caldera | Adversary emulation for chained attacks |
| Detection engineering blogs and newsletters | Many teams publish their detections and methods openly |

## Free and low-cost training and practice

| Resource | What it gives you |
|---|---|
| Blue Team Labs Online, LetsDefend, CyberDefenders | Hands-on SOC and blue-team challenges |
| TryHackMe, Hack The Box | Guided and open practice, including defensive paths |
| Microsoft, AWS and Google security learning paths | Free cloud security training from the providers |
| Vendor documentation and free tiers | The best way to learn a specific SIEM or EDR |
| Open malware and PCAP sample sites | Practice artefacts (handle safely, in a sandbox) |

!!! warning "Practice with samples safely"
    Training sites and sample repositories sometimes include real malware and real attack traffic. Open samples only in an isolated lab with no path to anything you care about, never on your work machine.

## Communities and sharing

| Resource | What it gives you |
|---|---|
| Sector ISACs (information sharing and analysis centres) | Threat sharing for your industry |
| MISP communities | Shared indicators of compromise |
| Open security communities and forums | Peer help, war stories, current threats |
| Local security meetups and conferences | People to learn from and ask |

## Reading to build judgement

Skills are taught quickly; judgement takes longer. Broaden it with:

- [ ] Incident write-ups and post-incident reports that organisations publish. Real cases teach more than any course.
- [ ] Threat intelligence reports from reputable vendors and CERTs, for how real attacks unfold.
- [ ] The documentation of the tools you actually use, read properly once.
- [ ] This handbook's [playbooks](../04-playbooks/index.md) and [walkthroughs](../field-guide/walkthroughs/index.md), worked in your own lab.

## How to use all this

- [ ] Do not try to consume everything. Pick one framework (ATT&CK), one rule format (Sigma), and one practice platform, and go deep.
- [ ] Tie learning to your lab: read a technique, run it, detect it, write the rule.
- [ ] Share what you learn with your team; a SOC where knowledge lives in one head is fragile.
- [ ] Revisit this list as projects change; nothing here stays current forever.

## Related pages

- [Open-source SOC lab](open-source-soc-lab.md)
- [Tool selection guide](tool-selection-guide.md)
- [Detection engineering](../05-detection-engineering/index.md)
- [Coverage mapping](../05-detection-engineering/coverage-mapping.md)
- [SOC Training](../training/index.md)
