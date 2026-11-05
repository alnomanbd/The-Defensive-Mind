# Case 02: Brute Force, Then a Success

Hundreds of failed logins is usually noise. This one ends in a successful login. The whole case is about telling noise from a real breach, and spotting the one success that matters.

!!! abstract "At a glance"
    - Attack: password guessing against VPN, then a success
    - Starts from: a spike of failed logins
    - Playbook: [Brute force](../../04-playbooks/brute-force.md), [Account compromise](../../04-playbooks/account-compromise.md)

## The alert

```text
02:40 UTC. Rule: "High rate of authentication failures from one source".
Source: 91.240.118.22
Target: the VPN gateway.
640 failed logins in 20 minutes, across 55 user accounts.
```

**Stop. Noise or not? What decides it?** Write it down.

## L1 triage

| Check | Finding |
|---|---|
| One source or many? | One IP, 91.240.118.22, a hosting provider |
| One account or many? | 55 accounts, a few attempts each: this is password spraying, not single-account guessing |
| Are the usernames real? | Yes, mostly valid: the attacker has a staff list or a leak |
| Is the source ours (scanner, monitoring)? | No, not on the allow list; on a threat-intel block list |
| Any success? | This is the key question. One 4624-equivalent success for r.haddad at 02:58 |

The moment a success appears after the failures, this stops being noise.

### Spraying plus the success

=== "Splunk SPL"

    ```spl
    index=vpn earliest=-1d
    | stats count(eval(outcome="failure")) as fails count(eval(outcome="success")) as success
        values(eval(if(outcome="success",user,null))) as who by src_ip
    | where fails > 100 AND success > 0
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    Syslog
    | where TimeGenerated > ago(1d) and ProcessName has "vpn"
    | summarize fails = countif(SyslogMessage has "fail"), success = countif(SyslogMessage has "success") by SourceIP = extract("from ([0-9.]+)", 1, SyslogMessage)
    | where fails > 100 and success > 0
    ```

## Escalation to L2

```text
Escalated 03:05 UTC by L1.
Verdict: password spraying from 91.240.118.22 (640 fails, 55 users) with ONE success:
r.haddad on the VPN at 02:58. Treat as account compromise.
Asks: contain r.haddad, confirm what happened after the login, is MFA in place on VPN?
```

## L2 investigation

The success changes everything. What did the attacker do after getting in?

| Time (UTC) | Finding | Source |
|---|---|---|
| 02:40 to 02:57 | 640 failed logins, 55 users | VPN logs |
| 02:58 | Success for r.haddad from 91.240.118.22 | VPN logs |
| 02:58 | No MFA prompt recorded: r.haddad was exempt from VPN MFA (a legacy exception) | IdP policy |
| 03:01 | r.haddad's VPN session connects to an internal jump host | Firewall, internal logs |
| 03:03 | Network scan from the jump host to the server subnet | EDR, netflow |

The missing MFA is why the single correct password worked. From the VPN the attacker reached a jump host and began scanning. This is an active intrusion.

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Disable r.haddad's VPN access and reset the password, revoke sessions | Identity team | L2, confirmed compromise |
| Block 91.240.118.22 at the VPN and firewall (time-limited) | Network | L2 |
| Isolate the jump host the attacker reached | SOC and infra | SOC manager (production system) |
| Remove the VPN MFA exemption for r.haddad and audit all other exemptions | Identity team | SOC manager |

Three other accounts also had the MFA exemption; all were corrected the same night.

## Outcome

The attacker guessed one password that happened to belong to an account exempt from MFA, and used it to get a foothold. Containment stopped them during the scanning stage, before lateral movement succeeded. The root cause was not the weak password alone; it was the MFA exemption that let one correct guess straight in.

## Lessons learned

- [ ] No internet-facing login should allow single-factor access. Remove all MFA exemptions; they are a standing hole.
- [ ] Detection tuned: success-after-failures correlation, and any VPN login without an MFA event.
- [ ] Alert on remaining MFA exemptions as a standing risk, not a one-off fix.

## Quiz

1. At what exact point did this stop being noise?
2. Why did one correct password work when MFA was in place?
3. What would you check next to be sure the jump host was the attacker's only reach?

??? note "Answers"
    1. When a successful login appeared after the failures (r.haddad at 02:58). Failures alone are noise; a success is a breach.
    2. r.haddad had a legacy exemption from VPN MFA, so the single factor (password) was enough.
    3. Pivot from the jump host: its outbound connections, any successful logins it made to other servers, new processes or accounts, and whether the scan led to any further access.

## Related pages

- [Brute force playbook](../../04-playbooks/brute-force.md)
- [Account compromise playbook](../../04-playbooks/account-compromise.md)
- [Password and MFA policy](../../08-security-policies/password-and-mfa-policy.md)
