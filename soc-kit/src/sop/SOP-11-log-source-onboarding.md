---
id: SOP-11
title: Log Source Onboarding
owner: SOC Engineer
audience: SOC engineers, detection engineers, platform and system owners
review: Every 12 months
summary: How to bring a new log source into the SIEM properly, so the data is complete, parsed, timed correctly, and actually used by a detection, not just collected.
---
## 1. Purpose

Collecting a log is not the same as using it. This procedure makes sure every new log source arrives complete, is parsed into usable fields, has correct timestamps, and feeds at least one detection, so the SOC gains real visibility rather than silent, unused data.

## 2. Scope

Any new log source added to the SIEM of [ORGANISATION]: identity, endpoints, network, cloud, email, applications and the SOC's own tools.

## 3. Before you start

- [ ] Confirm the source is on the priority list, or justify why it is being added now.
- [ ] Identify the source owner and agree the onboarding with them.
- [ ] Decide which events are needed; do not collect everything by default.
- [ ] Estimate the volume and check the cost and licence impact.

> NOTE: Collecting more is not safer; it is more expensive and noisier. Decide the few events that carry detection value for this source before you turn the tap on.

## 4. Procedure

### 4.1 Connect and collect

1. Configure the source to send the agreed events to the SIEM (agent, syslog, API, or connector).
2. Confirm data is arriving and roughly at the expected volume.
3. Record the source, its owner, the method and the expected volume in the log source inventory.

### 4.2 Parse and normalise

1. Confirm the events parse into fields you can search (user, source IP, action, host).
2. Normalise timestamps to [UTC]; confirm the time is correct, not skewed.
3. Map the key fields to your common schema so queries and detections are portable.

### 4.3 Validate

- [ ] Search for a known event and confirm it appears correctly.
- [ ] Check for dropped or truncated events.
- [ ] Confirm the volume is steady, not spiky or flat.

### 4.4 Detect and alert on silence

1. Create or enable at least one detection that uses this source.
2. Add the source to silent-source monitoring, so an alert fires if it stops sending data (SOP-12).
3. Record the detections that depend on this source.

## 5. Done when

- [ ] Data arrives, parses, and is correctly timed.
- [ ] The source is in the inventory with an owner.
- [ ] At least one detection uses it.
- [ ] Silent-source monitoring covers it.

## 6. Records

Update the log source inventory with the new source, its owner, method, volume, retention and the detections that use it.

## 7. Review

Reviewed every 12 months, and whenever onboarding methods change.
