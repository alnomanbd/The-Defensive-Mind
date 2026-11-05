# Use Case Prioritization

How to choose which detections to build first, and how to track what you cover. A "use case" is a thing you want to detect, for example "someone logs in to a server after many failed attempts". You cannot build hundreds at once, so build the ones that matter most for your real risks.

!!! abstract "At a glance"
    - Audience: detection engineer, SOC lead, SOC manager
    - Time to read: 10 minutes
    - Outcome: a method to pick the first detections by risk, and a way to measure coverage

!!! tip "Risk first, not easy first"
    The temptation is to build the detections that are quick to write. Resist it. Build detections for the attacks that would actually hurt you, even when they take more work. A SOC full of easy, low-value alerts is busy and blind at the same time.

## Pick use cases by risk, not by ease

Score each candidate on two things:

| Question | Scale |
|---|---|
| How likely is this against us? | Based on your sector, exposure and threat intelligence |
| How bad if it succeeds? | Based on what it reaches: crown jewels, regulated data, whole-domain impact |

Build the high-likelihood, high-impact ones first. A simple way to order them:

1. Attacks on your crown jewels and identity system.
2. The attacks your sector actually sees (ransomware, business email compromise, web attacks for most).
3. The attacks that match your exposure (lots of cloud means cloud key abuse; lots of internet apps means web attacks).
4. Everything else, later.

## Start from frameworks, do not start from scratch

You do not need to invent use cases. Proven starting points:

| Source | What it gives |
|---|---|
| MITRE ATT&CK | A map of attacker techniques; pick techniques relevant to you and detect them |
| Sigma rules | A large open library of detections in a portable format, convert to your SIEM |
| Your SIEM and EDR built-in rules | Turn on and tune the relevant ones before writing your own |
| Threat intelligence | What is being used against your sector right now |
| Your own incidents and near misses | The best source: detect what already got through |

## A first detection set (the starter pack)

If you are starting from nothing, these cover a lot of real risk. Roughly in order:

- [ ] Successful login after many failures (brute force that worked).
- [ ] Password spraying: one source, many accounts, few attempts each.
- [ ] Impossible travel or login from a new country on a privileged account.
- [ ] New or changed MFA method, especially on admins.
- [ ] New admin account or privilege grant.
- [ ] EDR malware detection that was allowed to run, not just blocked.
- [ ] Process stealing browser credentials (infostealer behaviour).
- [ ] Ransomware behaviour: shadow copy deletion, mass file changes.
- [ ] Command and control: beaconing, connections to newly registered domains.
- [ ] Data exfiltration: large or unusual outbound transfer, upload to personal cloud.
- [ ] Web attack with a success response, or web shell creation.
- [ ] Cloud: key used from a new place, logging turned off, new identity created.
- [ ] A log source going silent (your own blind-spot detector).

That is a dozen or so detections that catch a large share of real intrusions. Build these well before building a hundred niche ones.

## Track coverage with ATT&CK

Map every detection to the MITRE ATT&CK technique it catches. This turns "we have some rules" into a picture of what you can and cannot see.

| Benefit | How |
|---|---|
| See your gaps | Techniques with no detection are your blind spots |
| Avoid duplication | Spot where you have ten rules for one technique and none for another |
| Report coverage | "We detect X of the techniques our sector faces" is a clear metric |
| Prioritise | Fill the gaps that matter, not every gap |

Use the [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) to colour techniques by whether you detect them. Be honest: one weak rule for a technique is not full coverage.

!!! warning "Coverage is not a numbers game"
    "We cover 200 techniques" means little if the rules are noisy or never tested. Depth beats breadth: a tested, tuned detection that fires on real activity is worth more than ten rules nobody trusts. Measure coverage by techniques you reliably detect, not by rule count.

## Every use case needs more than a rule

A detection is not done when the rule is written. For each use case:

- [ ] A rule that fires on the real thing and is tested against a sample.
- [ ] A known and acceptable false positive rate.
- [ ] A severity and an owner.
- [ ] A runbook or playbook step telling the analyst what to do when it fires.
- [ ] A review date, because systems change and rules rot.

A rule with no runbook produces an alert nobody knows how to handle. Build the response with the detection, not after it.

## Related pages

- [Log source priorities](log-source-priorities.md)
- [Detection engineering](../05-detection-engineering/index.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
- [Maturity model](maturity-model.md)
