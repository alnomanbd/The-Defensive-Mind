# Playbook: Brute Force and Password Spraying

How to handle repeated authentication failures against SSH, RDP, VPN, web logins and SSO, and, most importantly, what to do when a success follows the failures.

!!! abstract "At a glance"
    - Audience: SOC analyst (L1/L2)
    - Time to read: 10 minutes
    - Outcome: separate background noise from a targeted attack, spot the one successful login that matters, and block the source without locking out the business

| Field | Value |
|:---|:---|
| **ID** | PB-04 |
| **Default severity** | Low for blocked noise, Medium for targeted attempts (see [Severity and SLA](../02-daily-operations/severity-and-sla.md)) |
| **Escalate to Critical when** | A successful login follows the failures on a privileged account, a server, or the VPN; or many accounts are locked out and business is affected |
| **MITRE ATT&CK** | T1110.001 Password Guessing, T1110.003 Password Spraying, T1110.004 Credential Stuffing, T1078 Valid Accounts, T1133 External Remote Services, T1021.001 Remote Desktop Protocol, T1021.004 SSH |
| **Typical alerts** | Many failed logins from one IP, one password tried across many users, account lockout storm, success after failures, login from a known-bad IP |
| **Owner** | SOC lead |
| **Last reviewed** | 2026-10-27 |

## 1. Summary

Every internet-facing login receives guessing traffic all day. Most of it is noise and should be handled by automation. The cases that matter are (a) **password spraying**, a few common passwords tried slowly against many accounts to avoid lockout, (b) **credential stuffing**, leaked email:password pairs tried against your services, and (c) **any successful login that follows failures**. Success for the defender: noise stays automated, targeted attacks are blocked early, and every success-after-failure is checked within minutes.

## 2. Triggers and detection

| Pattern | Signal | Log source |
|:---|:---|:---|
| Classic brute force | One source, one account, many failures in minutes | SSH `auth.log`, Windows Security event 4625, web app login logs |
| Password spraying | One or few sources, **many accounts**, 1-3 failures each, often same time window | IdP sign-in logs, Windows 4625/4771, VPN logs |
| Distributed spraying | Many IPs (residential proxies), many accounts, low rate | IdP logs aggregated by failure reason and user agent |
| Credential stuffing | Many accounts, failure reason mostly "user not found" or "bad password", some successes | Web app / customer login logs, Web Application Firewall (WAF) |
| Success after failure | Failures then success for the same account from the same source | All of the above; Windows 4624 after 4625 |

**Common false positives:** a user with an old password saved on a phone (repeating failures from one mobile IP), a service account with an expired password, a vulnerability scanner you own, a misconfigured monitoring probe, a load balancer health check hitting a login page.

## 3. Triage (first 15-30 minutes)

- [ ] Which service: SSH, RDP, VPN, SSO, webmail, a customer-facing app?
- [ ] Is the source internal or external? Internal source attacking many accounts = a compromised host, escalate.
- [ ] Is the source one of ours (scanner, monitoring, jump host)? Yes -> tune and close.
- [ ] How many accounts targeted, how many failures each? (Spraying vs. guessing.)
- [ ] Do the targeted usernames exist? Valid names suggest the attacker did reconnaissance or has a leak.
- [ ] **Was there any successful login** from the same source IP, ASN or user agent? This is the key question.
- [ ] Is the source already on a threat intel block list? Is it a TOR exit or hosting provider?
- [ ] Is the service supposed to be exposed to the internet at all?

Decision: failures only, external, automated noise -> Low, confirm auto-block worked, close, targeted spraying with valid usernames -> Medium, block and monitor, any success after failures -> High, treat as [Account Compromise](account-compromise.md), internal source -> High, investigate the host.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Which accounts were targeted? | Auth logs grouped by `target_user` for the source IP(s) |
| Did any attempt succeed? | Linux: `Accepted password` / `Accepted publickey` in `auth.log`; Windows: 4624 logon type 3/10 after 4625; IdP: result = success |
| What did the attacker do after a success? | Linux: shell history, `sudo` logs, new users, cron, `authorized_keys` changes; Windows: process creation (4688 / Sysmon 1), new services (7045); IdP: app access |
| Is the attack distributed? | Group failures by user agent, password-failure reason and time bucket rather than by IP |
| Where did the usernames come from? | Compare with [credential leak](credential-leak-dark-web.md) records; public staff lists; email address format |
| Is MFA in place for the targeted service? | IdP policy; legacy protocols (IMAP, POP, SMTP AUTH, basic auth) often bypass MFA |
| Are other services hit from the same sources? | Search all auth sources for the same IP / ASN over 7 days |

Query ideas:

```sql
-- password spraying: one source, many distinct users, few attempts each
SELECT src_ip, COUNT(DISTINCT target_user) AS users, COUNT(*) AS attempts
FROM auth_events
WHERE outcome = 'failure' AND timestamp > now() - interval '1 hour'
GROUP BY src_ip
HAVING COUNT(DISTINCT target_user) >= 10 AND COUNT(*) / COUNT(DISTINCT target_user) <= 3;

-- success after failures for the same account and source
SELECT f.target_user, f.src_ip, MIN(s.timestamp) AS success_time
FROM auth_events f JOIN auth_events s
  ON f.target_user = s.target_user AND f.src_ip = s.src_ip
WHERE f.outcome = 'failure' AND s.outcome = 'success'
  AND s.timestamp BETWEEN f.timestamp AND f.timestamp + interval '30 minutes'
GROUP BY f.target_user, f.src_ip;
```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Block source IPs / ranges at firewall, WAF or IdP | SOC / Network | Use time-limited blocks; avoid blocking shared carrier-grade NAT ranges used by staff |
| Turn on or tighten rate limiting / smart lockout | Identity / App team | Hard lockout lets an attacker lock out everyone, prefer smart lockout |
| Disable legacy authentication protocols | Identity team | Check first which apps still depend on them |
| For a successful login: reset password, revoke sessions, review activity | Identity team / SOC | Run [Account Compromise](account-compromise.md) |
| For a compromised server: isolate the host | SOC / Infrastructure | Coordinate with the service owner; may cause downtime |
| Restrict SSH / RDP exposure (VPN, bastion, allow list) | Infrastructure | The real fix, direct internet RDP should not exist |
| Enable automatic blocking (e.g. fail2ban, CrowdSec, SIEM active response) | Infrastructure / SOC | Test thresholds to avoid blocking your own monitoring |

## 6. Eradication and recovery

- [ ] Remove any attacker persistence found on a server (new users, SSH keys, cron jobs, services).
- [ ] Rebuild compromised servers from a known-good image when root / admin was obtained.
- [ ] Enforce MFA on every externally reachable login; move SSH to key-only authentication.
- [ ] Check password policy against a banned-password list (season + year, company name).
- [ ] Monitor the targeted accounts and services for 14 days for successes from new sources.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Service owner | When blocking or rate limiting changes their service | Analyst |
| Affected users | If their account was locked or reset | IT helpdesk |
| SOC lead | Any success after failures, or an internal source | Analyst |
| CISO | Compromise of a server, VPN or privileged account | SOC lead |

Most noise needs no communication. See [Escalation and Communication](../03-incident-response/escalation-and-communication.md).

## 8. Evidence to keep

- Auth log extracts for the attack window: sources, targeted users, counts, any successes.
- List of blocked IPs with block time and expiry.
- For a compromised host: volatile data and disk image before rebuild.
- Screenshots or exports of IdP risk detections.

Follow [Evidence Handling](../03-incident-response/evidence-handling.md).

## 9. Lessons learned

For the [Post-Incident Review](../03-incident-response/post-incident-review.md):

- Why was the service reachable from the internet with password-only login?
- Did automatic blocking work, and how fast?
- Did the attacker use leaked credentials? Should credential monitoring cover more domains?
- Are there accounts with weak or never-changed passwords (service accounts)?

Detections to add or tune: spraying (many users per source), success-after-failure correlation, failures on disabled or non-existent accounts, auth from internal hosts to many servers.

## Related pages

- [Account Compromise](account-compromise.md), [Credential Leak / Dark Web](credential-leak-dark-web.md), [Web Application Attack](web-application-attack.md)
- [Alert Triage](../02-daily-operations/alert-triage.md)
- [Sigma rules](../05-detection-engineering/index.md#sigma-rule-library)
- [Incident Report template](../09-templates/incident-report.md)
