---
id: SOP-26
title: Privileged Access Monitoring
owner: SOC Lead
audience: L2 and L3 analysts, identity team
review: Every 12 months
summary: How to watch the most powerful accounts, admins, domain and cloud administrators, service accounts, so misuse or compromise of the keys to everything is caught fast.
---
## 1. Purpose

Privileged accounts are the keys to everything. Their compromise or misuse is among the most damaging things that can happen. This procedure sets what the SOC watches on privileged accounts and how it responds, so abuse is caught early.

> NOTE: Attackers aim for privileged accounts because one of them can undo every other control. Watch them most closely, and treat any anomaly on an admin, domain or cloud administrator account as high priority until explained.

## 2. Scope

Privileged accounts for [ORGANISATION]: domain and local administrators, cloud root and administrator identities, privileged service accounts, and break-glass accounts.

## 3. What to monitor

| Signal | Why it matters |
|---|---|
| Privileged logon from a new host, location or at an odd time | Possible compromise or misuse |
| New admin account or privilege grant | A classic attacker persistence step |
| Admin account used for everyday activity | Breaks tiering; a sign of misuse or compromise |
| Break-glass account used | Should be rare and always investigated |
| Privileged action outside a change ticket | Unapproved or malicious change |
| Service account behaving like an interactive user | Possible credential theft |
| Changes to privileged groups (for example Domain Admins) | High-impact; confirm every one |

## 4. Procedure

### 4.1 Review privileged activity

- [ ] Review alerts on privileged accounts promptly; they are high priority.
- [ ] For each, confirm it matches an approved change, a known admin task, or the account's normal pattern.
- [ ] Check the source (host, location, device) and whether strong MFA was used.

### 4.2 Decide

| Finding | Action |
|---|---|
| Matches an approved change or normal task | Note and close |
| Unapproved but by a legitimate admin | Raise with the admin and their manager; log it |
| No benign explanation | Treat as possible compromise: contain the account (SOP-25) and escalate |
| Break-glass used without an incident | Investigate immediately |

### 4.3 Standing hygiene the SOC watches

- [ ] Admins use separate admin accounts, not their everyday account.
- [ ] Privileged accounts have strong, phishing-resistant MFA.
- [ ] Break-glass accounts are protected, monitored, and alert when used.
- [ ] Privileged access is reviewed regularly (GOV, access control policy).

## 5. Service and break-glass accounts

- [ ] Each privileged service account has a documented owner and expected behaviour; alert on deviation.
- [ ] Break-glass accounts trigger an alert on every use and are reviewed every time.

## 6. Records

Record privileged-activity reviews of note, any misuse found, and the response.

## 7. Review

Reviewed every 12 months.
