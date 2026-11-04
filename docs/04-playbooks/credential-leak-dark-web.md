# Playbook: Credential Leak / Dark Web Exposure

What to do when company credentials turn up in infostealer logs, on dark-web markets, in paste sites or in breach dumps. The goal is to act before the credentials are used.

!!! abstract "At a glance"
    - Audience: SOC analyst, threat intelligence analyst, identity team
    - Time to read: 12 minutes
    - Outcome: verify a leak, find the people and devices behind it, reset and revoke, clean the source device, and watch for use

| Field | Value |
|:---|:---|
| **ID** | PB-03 |
| **Default severity** | Medium (see [Severity and SLA](../02-daily-operations/severity-and-sla.md)) |
| **Escalate to Critical when** | The leak contains valid privileged credentials, live session cookies for corporate SSO, VPN / remote access credentials, or there is evidence the credentials were already used |
| **MITRE ATT&CK** | T1589.001 Gather Victim Identity Information: Credentials, T1597.002 Search Closed Sources: Purchase Technical Data, T1555.003 Credentials from Web Browsers, T1539 Steal Web Session Cookie, T1552.001 Unsecured Credentials: Credentials In Files, T1078 Valid Accounts |
| **Typical alerts** | Dark-web / credential monitoring feed hit, breach notification service, threat intel report, researcher or law-enforcement notification, internal secret scanning alert |
| **Owner** | Threat intelligence lead with SOC lead |
| **Last reviewed** | 2026-10-27 |

## 1. Summary

Stolen credentials are sold in bulk. The most dangerous source today is **infostealer logs**: archives taken from an infected computer that contain saved browser passwords, cookies, autofill data and system details. Older **breach dumps** (a third-party site was hacked) and **combo lists** (recycled email:password pairs) are less fresh but still used for credential stuffing. Success for the defender: every exposed credential is invalid before an attacker tries it, the infected device is found and cleaned, and nobody's private data is spread further during the response.

## 2. Triggers and detection

| Source type | What it usually contains | Typical risk |
|:---|:---|:---|
| Infostealer log | URL + username + password, session cookies, machine name, IP, OS, installed software | High, fresh, often includes cookies that bypass MFA |
| Breach dump of a third-party site | Corporate email + password used on that site (often hashed) | Medium, only a problem if the password is reused |
| Combo list / paste | Email:password pairs, mixed ages, many duplicates | Low to Medium, mostly old, verify freshness |
| Access broker listing | "VPN / RDP / admin access to a company in sector X, revenue Y" | High to Critical, implies working access |
| Code repository or public paste | API keys, tokens, `.env` files | High, see [Cloud Account Compromise](cloud-account-compromise.md) |

**True positive pattern:** infostealer record with a corporate SSO URL (`https://sso.example.com`), a current employee's username, a capture date in the last 30 days, and a machine name that matches the asset inventory.

**Common false positives:** former employees whose accounts are already disabled; personal email addresses that only mention the company domain; very old breaches already handled; test or generic accounts; records for a similarly named but different organisation.

## 3. Triage (first 15-30 minutes)

- [ ] Record the source, the date it was posted, and the capture date inside the record (they differ).
- [ ] Classify the source type using the table above.
- [ ] Extract only what you need: usernames, affected URLs, machine names, IPs, capture date. Do not copy full personal data into tickets or chat.
- [ ] Is the username a current, enabled account? Check the directory. Disabled -> note and lower priority.
- [ ] Which service does the credential belong to: corporate SSO, VPN, email, a SaaS app, a personal site?
- [ ] Is the password still current? Compare the leak date with the last password change date. **Do not** test the password by logging in.
- [ ] For infostealer logs: is the machine name / hardware ID a corporate asset or a personal device?
- [ ] Any sign-ins with this account from unknown IPs since the capture date?

Decision: current account + recent leak -> true positive, continue, password changed after the leak and no cookies -> reset anyway as hygiene, Low, former employee / unrelated -> close with reason, access-broker listing -> escalate to SOC lead immediately.

!!! danger "Handle leaked data carefully"
    Do not buy data from criminal markets, do not register on criminal forums with corporate identities, and do not download raw dumps onto corporate laptops. Work through your monitoring provider or an approved, isolated research environment. See [Dark Web and Credential Monitoring](../06-threat-intelligence/dark-web-and-credential-monitoring.md).

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Which people are affected? | Directory lookup for every username / email in the record |
| Which device was infected? | Machine name, hardware ID, IP from the stealer log matched against asset inventory, EDR and DHCP logs |
| Is the infected device still infected? | EDR telemetry on that host: unknown processes, persistence, outbound connections to rare domains |
| Was it a personal device? | No match in inventory; the record lists personal accounts alongside corporate ones: common with remote work |
| Which services were exposed? | URLs in the record: SSO, VPN, email, code repository, cloud console, internal admin panels |
| Were the credentials or cookies used? | IdP and VPN logs since the capture date: new IPs, new devices, token reuse without MFA |
| Are there other corporate secrets in the record? | API keys, cloud tokens, password manager exports, files grabbed from the desktop |
| Is this one victim or a pattern? | Count records over the last 90 days; look for common lures (cracked software, fake updates) |

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Reset the password for every exposed corporate account | Identity team | Force change at next sign-in; low risk |
| Revoke all sessions and refresh tokens | Identity team | Essential when cookies were stolen, a password reset alone leaves sessions alive |
| Review and reset MFA methods if the attacker could have registered one | Identity team | Compare with known devices |
| Rotate any API keys, tokens or service passwords found | Owning engineering team | Coordinate to avoid outages; rotate, then revoke the old key |
| Isolate the infected corporate device | SOC / Desktop | Run [Malware / Infostealer](malware-infostealer.md) |
| Ask the user to stop using a personal infected device for work | IT / Manager | Provide clean-up guidance; do not demand access to personal devices |
| Block access from the user's account from unmanaged devices until cleared | Identity team | Conditional access; temporary |
| Request takedown of public pastes or repositories | Threat intel / Legal | Takedown does not undo exposure, still rotate |

## 6. Eradication and recovery

- [ ] Corporate device: re-image (preferred for infostealers) or clean with EDR and verify.
- [ ] Personal device: user re-installs or runs a trusted clean-up, changes personal passwords too (they were stolen as well).
- [ ] User re-enrols MFA on a clean device; prefer phishing-resistant methods.
- [ ] Add the user's accounts to a high-watch list for 30 days: sign-ins from new ASNs, MFA changes, mailbox rules.
- [ ] Keep monitoring the source for new records about the same users or devices.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Affected user | At reset time, by phone or chat; explain calmly what was found and why | Analyst / IT |
| User's manager | If the device is corporate or work is disrupted | SOC lead |
| Owners of rotated secrets | Before rotation | Analyst |
| CISO | Access-broker listings, privileged accounts, or evidence of use | SOC lead |
| Privacy officer / Legal | If customer or employee personal data appears in the record | SOC lead |

Be kind: most infostealer victims downloaded something they believed was legitimate. See [Escalation and Communication](../03-incident-response/escalation-and-communication.md).

## 8. Evidence to keep

- Monitoring alert, source reference (no raw dump files on general storage), capture and posting dates.
- A minimised extract: usernames, URLs, machine names, IPs, redacted passwords (keep only first and last characters if needed for comparison).
- Directory status and last password change for each account.
- IdP / VPN log extract since the capture date.
- EDR triage of the infected device.

Follow [Evidence Handling](../03-incident-response/evidence-handling.md); restrict access to the case because it contains personal data.

## 9. Lessons learned

For the [Post-Incident Review](../03-incident-response/post-incident-review.md):

- How did the device get infected? Cracked software, malicious ad, fake browser update?
- Were corporate passwords saved in the browser? Should browser password saving be disabled by policy?
- Could personal devices reach corporate SSO without device checks?
- How long between capture date and our detection? Is our monitoring coverage enough?

Controls to consider: device-bound sessions / token binding, conditional access requiring managed devices, enterprise password manager, user guidance in the [Employee Security Guide](../08-security-policies/employee-security-guide.md).

## Related pages

- [Dark Web and Credential Monitoring](../06-threat-intelligence/dark-web-and-credential-monitoring.md)
- [Malware / Infostealer](malware-infostealer.md), [Account Compromise](account-compromise.md), [Brute Force](brute-force.md)
- [Cloud Account Compromise](cloud-account-compromise.md)
- [Incident Report template](../09-templates/incident-report.md)
