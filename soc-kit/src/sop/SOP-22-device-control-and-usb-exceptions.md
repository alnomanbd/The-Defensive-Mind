---
id: SOP-22
title: Device Control and USB Exceptions
owner: SOC Lead
audience: L1 and L2 analysts, endpoint team
review: Every 12 months
summary: How to handle removable-media (USB) alerts and exception requests, so data cannot walk out on a stick and malware cannot walk in, while legitimate business needs are met.
---
## 1. Purpose

Removable media is a two-way risk: data can be copied out, and malware can be brought in. This procedure handles device-control alerts and the exception requests that inevitably follow a block, so the control protects the organisation without blocking real work in a way that pushes people to work around it.

## 2. Scope

Removable storage (USB drives, external disks, memory cards) device-control events and exception requests for [ORGANISATION] endpoints.

## 3. The baseline

- [ ] Removable storage is [blocked / read-only / allowed with logging] by default, per the endpoint policy.
- [ ] All removable-media use is logged (device, serial, host, user, files where possible).
- [ ] Exceptions are time-limited and approved, never standing by default.

## 4. Handling a device-control alert

### 4.1 Triage

- [ ] What happened: a blocked device, a large copy to a device, a new device on a sensitive host?
- [ ] Who and where: the user, the host, and whether either is sensitive (finance, admin, source code).
- [ ] How much data, and what kind?
- [ ] Is there an approved exception for this?

### 4.2 Decide

| Finding | Action |
|---|---|
| Blocked device, no data moved | Note it; close, or raise with the user if repeated |
| Large copy to a personal device, no exception | Investigate as possible data exfiltration; see the playbook |
| New device on a sensitive host | Confirm it is expected; investigate if not |
| A known, approved exception | Confirm it matches the approval; close |

> NOTE: A sudden copy of many files to a USB device, especially by someone changing role or leaving, is a classic insider signal. Check the leaver list and follow the insider process (GOV-10) before treating it as routine.

## 5. Handling an exception request

When someone needs removable media for a genuine business reason:

- [ ] The request is in writing, with the business reason.
- [ ] It names the user, the device or device type, the purpose, and a time limit.
- [ ] It is approved by [role], weighing the data risk.
- [ ] The exception is recorded, time-limited, and reviewed when it expires.
- [ ] Prefer a safer alternative first (approved file transfer, encrypted company device) before granting raw USB access.

> WARNING: A permanent, unreviewed USB exception is a standing hole for data to leave and malware to enter. Keep exceptions specific and time-limited, and remove them when the need passes. An undocumented exception is just the control being bypassed.

## 6. Records

Record device-control events of note and all exceptions: who, what device, purpose, approver, expiry.

## 7. Review

Reviewed every 12 months.
