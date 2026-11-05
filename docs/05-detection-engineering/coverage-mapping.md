# Coverage Mapping

How to see what your detections can and cannot catch, by mapping them to MITRE ATT&CK. Without a map, "we have a lot of rules" tells you nothing about your blind spots. With one, you can point at exactly what you cannot see and decide whether that matters.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC leads, SOC managers
    - Time to read: 10 minutes
    - Outcome: a method to map detections to ATT&CK, build a heatmap, and choose the next gap to close

## What MITRE ATT&CK gives you

ATT&CK is a public catalogue of the techniques attackers use, organised by tactic (the attacker's goal) and technique (how they do it). It gives the SOC a shared map: instead of a pile of rules, you get a picture of which attacker behaviours you detect and which you miss.

| Term | Meaning |
|---|---|
| Tactic | The attacker's goal at a step: initial access, persistence, exfiltration |
| Technique | How they achieve it: phishing, scheduled task, exfiltration to cloud storage |
| Sub-technique | A more specific method under a technique |
| Coverage | Which techniques you can detect, and how well |

## Map every detection to a technique

Tag each detection with the ATT&CK technique or techniques it catches. The Sigma rules in this handbook already carry their technique IDs in the `tags` field, for example `attack.t1059.001`.

- [ ] Give every detection one or more ATT&CK technique IDs.
- [ ] Keep the mapping with the rule, in version control, not in a separate spreadsheet that rots.
- [ ] Be honest about strength: a weak, noisy rule for a technique is partial coverage, not full.

## Build a heatmap

The [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) is a free tool that colours the technique matrix. Export your detections as a Navigator layer and you get a picture: green where you detect, blank where you do not.

A simple way to generate a layer from your rules:

- [ ] Collect the technique IDs from all your detections (from the Sigma `tags`, or your rule metadata).
- [ ] Score each: for example 1 for a weak or noisy rule, 2 for a tested reliable one.
- [ ] Load the layer into Navigator and colour by score.
- [ ] Look at the shape: which tactics are strong, which columns are empty.

!!! tip "Colour by confidence, not just presence"
    A heatmap that is all green because every technique has one weak rule is a comforting lie. Score by how reliably you actually detect each technique. A smaller map of techniques you truly catch is more honest, and more useful, than a full one you cannot trust.

## Read the map: find the gaps that matter

A gap is only a problem if it matters to you. Do not try to cover all of ATT&CK; cover what fits your risk.

| Ask | To decide |
|---|---|
| Is this technique used against our sector? | Threat intelligence tells you what is actually in play |
| Does it hit our crown jewels or identity? | Gaps near your most important systems come first |
| Do we have the log source to detect it at all? | A detection gap may really be a logging gap ([Log source priorities](../01-build-a-soc/log-source-priorities.md)) |
| Is there a cheap, high-value rule to fill it? | Fill easy, important gaps before hard, rare ones |

Prioritise gaps by likelihood and impact, the same way you prioritise use cases ([Use case prioritization](../01-build-a-soc/use-case-prioritization.md)).

## Coverage is not a score to maximise

!!! danger "Do not chase the number"
    "We cover 180 techniques" is a vanity metric if the rules are untested or noisy. Attackers do not care how many techniques you tag; they care which ones they can walk through unseen. Depth beats breadth. Ten techniques you reliably detect and respond to are worth more than a hundred you nominally tag.

Measure coverage as **techniques you reliably detect and have a response for**, not as rule count or raw technique count.

## Detection gaps are often logging gaps

Before writing a detection for a gap, check you even collect the data to detect it. You cannot detect PowerShell abuse without PowerShell logging, or cloud key misuse without cloud audit logs.

| Gap looks like | Might really be |
|---|---|
| No detection for a technique | No log source for it |
| A rule that never fires | A log source that stopped, or was never onboarded |
| Can only detect it after the fact | Logs arrive too slowly or are not parsed |

Fixing the log source often unlocks several detections at once. Map your coverage against your log sources, not just your rules.

## Use the map to drive work

The heatmap is not a poster; it is a backlog.

- [ ] Each quarter, pick the few gaps that matter most and build detections for them.
- [ ] Re-run the map after building, to show progress to leadership.
- [ ] Use the map in reviews: "we now detect X of the techniques our sector faces, up from Y".
- [ ] Combine it with testing: a green square you have never tested is a guess, not coverage.

## Related pages

- [Testing and tuning](testing-and-tuning.md)
- [Writing good detections](writing-good-detections.md)
- [Use case prioritization](../01-build-a-soc/use-case-prioritization.md)
- [Log source priorities](../01-build-a-soc/log-source-priorities.md)
- [Threat hunting](../02-daily-operations/threat-hunting.md)
