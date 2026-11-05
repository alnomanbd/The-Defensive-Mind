---
id: PB-03
title: Account Compromise
owner: SOC manager with Identity team
audience: SOC analyst L1/L2/L3, identity team, SOC manager
review: Every 12 months, and after every real incident that used this playbook
summary: Hands-on steps for suspicious sign-ins, impossible travel, Multi-Factor Authentication (MFA) fatigue and stolen session tokens.
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-03 |
| **Default severity** | High (see Severity and SLA) |
| **Escalate to Critical when** | Privileged account (identity / cloud / domain admin), finance or executive user, or attacker persistence found (new MFA device, OAuth app, admin role) |
| **MITRE ATT&CK** | T1078.004 Valid Accounts: Cloud Accounts, T1621 Multi-Factor Authentication Request Generation, T1539 Steal Web Session Cookie, T1550.004 Web Session Cookie, T1528 Steal Application Access Token, T1557 Adversary-in-the-Middle, T1098.005 Device Registration, T1556.006 Modify Authentication Process: MFA |
| **Typical alerts** | Impossible travel, sign-in from hosting / anonymiser IP, MFA push denials burst, IdP "risky sign-in", new MFA method, token replay from new IP |
| **Owner** | SOC manager with Identity team |
| **Last reviewed** | 2026-10-27 |

## 1. Summary

An attacker signs in as a real user with a stolen password, cookie or an approved MFA push. Decide fast whether it is the user; if not, kill password, sessions, tokens, devices and app consents together. Then scope what they did.

## 2. Triggers and detection

- **Impossible travel / new properties:** new country, hosting-provider ASN, unknown device, scripting user agent (`python-requests`, `axios`).
- **MFA fatigue:** many prompts in minutes, then one approval.
- **Token replay:** session used from an IP / device other than where it was issued, no fresh MFA (typical after Adversary-in-the-Middle (AitM) phishing or an infostealer).
- **Post-login changes:** new MFA method, device registration, inbox rule, OAuth consent, role assignment.
- **False positives:** corporate VPN / secure web gateway egress abroad, real travel, mobile carrier IP changes, new laptop. Check the corporate egress list and the asset ticket first.

## 3. Triage (first 15-30 minutes)

| Role | Responsibility |
|:---|:---|
| **L1** | Pull 7 days of sign-ins, compare with the user's baseline, check egress / travel lists, contact the user out of band, escalate |
| **L2/L3** | Decide compromise, revoke sessions, remove persistence, scope access (mail, files, SaaS, cloud), hunt same IP across tenant |
| **Manager** | Approve disabling executives / admins, inform CISO and data owners, start privacy / legal clock if personal data was accessed |

- [ ] Account type: user, admin, service account, shared mailbox?
- [ ] Source IP in corporate egress / known VPN / partner list? If yes, likely benign.
- [ ] Is the IP / country / device / user agent new for this user (7-30 days)?
- [ ] How was MFA satisfied: push approved, "previously satisfied" token claim, not required?
- [ ] MFA denials in the last hour ≥ 3 followed by an approval?
- [ ] Any changes after sign-in: MFA methods, inbox rules, OAuth apps, roles?
- [ ] Call / chat the user: "Did you sign in from Country X at 10:42 UTC?"

Decision:

- User confirms and nothing else is odd: close as benign.
- User denies, or cannot be reached and indicators are strong: contain now.
- Admin or finance account and still unsure: contain anyway.

> WARNING: Contain before you finish investigating. For privileged accounts, revoke sessions as soon as compromise is likely. Investigation continues from logs.


## 4. Investigation

| Question | Where to look |
|:---|:---|
| When did it start? | IdP sign-ins: first event from attacker IP / ASN / device; search back 30 days |
| How did they get in? | Phishing click (PB-01), infostealer (PB-08), leak (PB-05), spraying (PB-04) |
| Other accounts from the same IP? | IdP logs filtered by attacker IP across all users |
| What did they access? | Mailbox audit (MailItemsAccessed, Send), file / SaaS access logs |
| What persistence? | IdP audit: security info registered, device registered, consent granted, role added |
| Email sent as the user? | Mail trace for the attacker window: see BEC |
| Cloud console / API used? | Cloud audit logs: see PB-16 |

### Hunting queries

User sign-in baseline (KQL, Entra ID / Sentinel):

```kql
SigninLogs
| where TimeGenerated > ago(30d) and UserPrincipalName =~ "jdoe@example.com"
| project TimeGenerated, IPAddress, Country = tostring(LocationDetails.countryOrRegion),
          AppDisplayName, ResultType, AuthenticationRequirement, UserAgent,
          DeviceId = tostring(DeviceDetail.deviceId)
| order by TimeGenerated desc
```

MFA fatigue (KQL):

```kql
SigninLogs
| where TimeGenerated > ago(1d) and ResultType == "500121"
| summarize Denials = count(), IPs = make_set(IPAddress) by UserPrincipalName, bin(TimeGenerated, 1h)
| where Denials >= 5
```

MFA fatigue (Splunk SPL, Okta logs):

```spl
index=okta eventType IN ("system.push.send_factor_verify_push","user.mfa.okta_verify.deny_push")
| bin _time span=1h
| stats count(eval(eventType="system.push.send_factor_verify_push")) as pushes
        count(eval(eventType="user.mfa.okta_verify.deny_push")) as denies by _time actor.alternateId
| where pushes>=5 AND denies>=3
```

Persistence after sign-in (KQL):

```kql
AuditLogs
| where TimeGenerated > ago(7d)
| where OperationName in ("User registered security info","Register device",
                          "Consent to application","Add member to role")
| extend Target = tostring(TargetResources[0].userPrincipalName)
| project TimeGenerated, OperationName, Target, InitiatedBy
```

Same attacker IP across all users (Elastic ES|QL):

```sql
FROM logs-*
| WHERE source.ip == "198.51.100.23" AND event.category == "authentication"
| STATS events = COUNT(*), outcomes = VALUES(event.outcome) BY user.name
```

Wazuh (Discover / DQL): `data.srcip:"198.51.100.23" and rule.groups:"authentication_success"`.

### Worked example

```text
2026-10-27T08:02:11Z jdoe@example.com 10.0.8.15 (corp egress) Country=GB  App=Mail  MFA=push approved  UA=Edge/Windows
2026-10-27T10:40:57Z jdoe@example.com 198.51.100.23 ASN=hosting  Country=NL  Result=500121 (MFA denied) x7
2026-10-27T10:42:03Z jdoe@example.com 198.51.100.23 ASN=hosting  Country=NL  App=Mail  MFA=push approved  UA=python-requests
2026-10-27T10:44:19Z AuditLog: "User registered security info" target=jdoe@example.com  ip=198.51.100.23
2026-10-27T10:46:50Z OfficeActivity: New-InboxRule "." MoveToFolder=RSS Subject contains "invoice"
```

Reading: classic MFA fatigue, seven denials, one approval, scripting user agent from a hosting ASN, then a new MFA method and a hiding rule. Severity High (Critical if jdoe is in finance). Revoke, remove the new method and rule, then scope mailbox access from 10:42.

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Revoke all sessions and refresh tokens | L2 / Identity | Password reset alone does not kill tokens on many platforms |
| Reset password, or disable if user unreachable | Identity | Disable for admins; inform manager |
| Remove attacker MFA methods and devices | Identity | Compare with the user's known devices |
| Revoke suspicious OAuth consents / app passwords | Identity | Export first |
| Block attacker IP / ASN in conditional access | Identity | Hosting ASNs can be blocked broadly |
| Remove inbox rules and forwarding | Messaging | Export first |
| Remove roles / groups granted during incident | Identity / Cloud | Confirm with role owner |

### Example commands

Microsoft Entra ID (Graph PowerShell):

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","UserAuthenticationMethod.ReadWrite.All"
Revoke-MgUserSignInSession -UserId jdoe@example.com
Update-MgUser -UserId jdoe@example.com -AccountEnabled:$false
Get-MgUserAuthenticationMethod -UserId jdoe@example.com
Get-MgUserRegisteredDevice -UserId jdoe@example.com
Get-MgUserOauth2PermissionGrant -UserId jdoe@example.com
Get-InboxRule -Mailbox jdoe@example.com | Format-List Name,Enabled,From,SubjectContainsWords,MoveToFolder,ForwardTo,DeleteMessage
```

Okta and Keycloak (open source):

```bash
# Okta: clear sessions and OAuth tokens
curl -X DELETE -H "Authorization: SSWS $OKTA_TOKEN" \
  "https://acme.okta.example.com/api/v1/users/$USER_ID/sessions?oauthTokens=true"
# Keycloak: log the user out of all sessions in realm "acme"
kcadm.sh create users/$USER_ID/logout -r acme
```

## 6. Eradication and recovery

- [ ] Fix the root cause: clean the device, purge the phishing email, close the leak.
- [ ] Re-enable only after the user has a clean device and new credentials.
- [ ] Rotate secrets the user could see (shared passwords, API keys in mail / drive).
- [ ] Re-register with phishing-resistant MFA (FIDO2 / number matching).
- [ ] Watch 30 days: new-country sign-ins, MFA changes, rule creation.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| User and their manager | At containment, out of band | L2 / Identity |
| SOC manager / CISO | High immediately; Critical within 15 min | L2 to manager |
| Data owners | After scoping | Manager |
| Legal / privacy officer | Personal data accessed (notification clock) | Manager |
| Recipients of attacker email | If phishing was sent from the account | Manager + Communications |

See Escalation and Communication.

## 8. Evidence to keep

- IdP sign-in and audit exports for the attacker window plus 7 days before.
- Attacker IPs, ASNs, user agents, device IDs.
- Export of MFA methods, devices, consents and inbox rules **before** removal.
- Mailbox / file access audit extracts; notes of the user call (time, channel, answer).

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review: which control failed (MFA type, conditional access, device trust)? Dwell time? Did revocation reach every SaaS app? Detections to add: MFA method added after a risky sign-in, token use from a new ASN, inbox rule within 1 hour of a new-country sign-in.


## Related documents

- Phishing, Credential Leak / Dark Web, Brute Force
- Business Email Compromise, Cloud Account Compromise
- Alert Triage, Sigma rules
- Incident Report template
