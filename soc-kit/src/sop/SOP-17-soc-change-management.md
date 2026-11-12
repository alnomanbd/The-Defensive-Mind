---
id: SOP-17
title: SOC Change Management
owner: SOC Manager
audience: SOC engineers, detection engineers, analysts
review: Every 12 months
summary: How changes to the SOC's own systems and detections are proposed, tested, approved and recorded, so a change does not quietly break detection or create a blind spot.
---
## 1. Purpose

A careless change to a detection, a pipeline or the SIEM can blind the SOC without anyone noticing. This procedure makes SOC changes deliberate: tested where possible, approved at the right level, recorded, and reversible.

> NOTE: The most dangerous SOC change is the one nobody recorded. When a detection goes silent or a source stops, the first question is "what changed?" A change log answers it in seconds; without one, you investigate blind.

## 2. Scope

Changes to the SOC's own systems for [ORGANISATION]: SIEM and platform configuration, detections and rules, log pipelines, automations, and integrations. This is about changing the SOC's machinery, not about containment actions during an incident (those follow GOV-04).

## 3. One change at a time

- [ ] Make one production change at a time where you can, so if something breaks you know the cause.
- [ ] Avoid bulk changes to production detections or pipelines; stagger them.

## 4. Procedure

### 4.1 Propose

1. Record the change: what, why, which systems, and the expected effect. Use the Change Request template.
2. Note the risk: could this reduce detection or create a blind spot?

### 4.2 Test

- [ ] Test the change in a sandbox or staged way where possible before production.
- [ ] For a detection change, re-test that it still fires on the real attack (SOP-14).

### 4.3 Approve

| Change | Approved by |
|---|---|
| A single detection or tuning change | Detection engineer or SOC lead |
| A pipeline, platform or integration change | SOC engineer and SOC manager |
| Anything that reduces coverage | SOC manager, recorded with the reason |
| An emergency change during an incident | Incident lead, recorded after the fact |

### 4.4 Apply and verify

1. Apply the change in a controlled window where it matters.
2. Confirm it had the intended effect and did not break collection or detection.
3. Keep a rollback ready; be able to undo it.

### 4.5 Record

Record every change in the change log: what, why, who, when, the result, and how to roll back. This is the single most useful record when something later goes wrong.

## 5. Emergency changes

During an incident, speed can require an immediate change (removing a malicious rule, blocking a source). Make it, then record it straight after with the reason and who authorised it.

## 6. Done when

- [ ] The change is applied and verified.
- [ ] Detection and collection are confirmed intact.
- [ ] The change is recorded with a rollback.

## 7. Review

Reviewed every 12 months.
