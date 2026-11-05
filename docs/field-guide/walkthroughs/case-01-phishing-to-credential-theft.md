# Case 01: Phishing to Credential Theft

A user reports a suspicious email. By the end, we know whether they entered their password, whether the attacker used it, and what we did about it. Worked the way a real SOC does.

!!! abstract "At a glance"
    - Attack: phishing leading to account takeover
    - Starts from: a user-reported email
    - Playbooks: [Phishing](../../04-playbooks/phishing.md), [Account compromise](../../04-playbooks/account-compromise.md)

## The alert

```text
09:12 UTC. Reported through the "Report phishing" button.
Reporter: j.okoro (Finance).
Subject: "Action required: your mailbox is almost full - verify now"
From: "IT Service Desk" <support@m365-verify-login.com>
Body: a button, "Verify your account", linking to https://m365-verify-login.com/auth
```

**Stop. What would you check first?** Write it down before reading on.

## L1 triage (first 15 minutes)

| Check | Finding |
|---|---|
| Is the sender really us? | No. `m365-verify-login.com` is not a company domain; display name faked as "IT Service Desk" |
| Is the link a look-alike login page? | Yes. The URL leads to a fake Microsoft login |
| Is it a simulation? | Checked the awareness-training schedule: no simulation running |
| Did the reporter click or enter credentials? | Asked j.okoro directly: "I clicked and typed my password before it looked wrong" |
| Who else received it? | Message trace by subject and sender: 23 recipients |

The key fact: the reporter entered their password. This is no longer just phishing; it may be account takeover.

### Message trace: who else got it

=== "Microsoft Sentinel KQL"

    ```kql
    EmailEvents
    | where Timestamp > ago(2d)
    | where SenderMailFromDomain == "m365-verify-login.com" or Subject has "mailbox is almost full"
    | project Timestamp, RecipientEmailAddress, SenderFromAddress, Subject, DeliveryAction, UrlCount
    ```

=== "Splunk SPL"

    ```spl
    index=email (sender_domain="m365-verify-login.com" OR subject="*mailbox is almost full*") earliest=-2d
    | table _time recipient sender subject action
    ```

## Escalation to L2

```text
Escalated 09:26 UTC by L1 (a.ndiaye).
Verdict: malicious phishing, credentials likely stolen for j.okoro.
Evidence: look-alike domain m365-verify-login.com, fake M365 login, reporter confirms
password entry ~09:05. 23 recipients, 1 confirmed submitter.
Asks: treat j.okoro as account compromise; purge campaign; check other recipients.
```

## L2 investigation

The question now: did the attacker use the stolen password? Pivot to the user's sign-ins.

| Time (UTC) | Finding | Source |
|---|---|---|
| 09:05 | j.okoro enters password on fake page | Reporter, email timeline |
| 09:08 | Sign-in success for j.okoro from 185.220.101.50 (a hosting provider, new country) | IdP sign-in logs |
| 09:10 | New inbox rule created: move mail with "invoice" or "payment" to RSS Feeds | M365 audit `New-InboxRule` |
| 09:11 | Mailbox searched for "wire" and "bank" | M365 audit `SearchQueryInitiated` |
| 09:12 | j.okoro reports the email | Report button |

The attacker was in within three minutes, hid incoming mail, and searched for payment threads. This is a live account takeover heading toward business email compromise.

### Did the attacker get in

=== "Microsoft Sentinel KQL"

    ```kql
    SigninLogs
    | where TimeGenerated > ago(1d) and UserPrincipalName startswith "j.okoro"
    | project TimeGenerated, IPAddress, Location, ResultType, AppDisplayName, UserAgent
    | order by TimeGenerated asc
    ```

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Reset password, revoke all sessions and tokens for j.okoro | Identity team | L2, standard for confirmed takeover |
| Remove the malicious inbox rule (after exporting it as evidence) | Email admin | L2 |
| Purge the phishing email from all 23 mailboxes | Email admin | L2 |
| Block the domain m365-verify-login.com at mail gateway and proxy | SOC | L2 |
| Check the other 22 recipients for clicks or sign-ins from the same IP | L2 | - |

Two other recipients had clicked but not entered credentials; they were reset as a precaution. No other sign-ins from the attacker IP.

## Outcome

Caught within minutes because the user reported it. The attacker had a live session but was cut off before any payment fraud. Session revocation, not just the password reset, is what actually ejected them, because the stolen session cookie would otherwise have kept working.

## Lessons learned

- [ ] MFA was in place but the attacker proxied it in real time (an adversary-in-the-middle page). Move finance to phishing-resistant MFA (hardware keys or passkeys).
- [ ] Detection added: new inbox rule with financial keywords, and sign-in from a hosting-provider IP right after.
- [ ] The report button worked and was fast; reinforce it in awareness training.

## Quiz

1. Why was a password reset alone not enough?
2. What single log event proved the attacker was inside, not just that the user clicked?
3. Why does the new inbox rule matter so much?

??? note "Answers"
    1. The attacker had a live session (cookie) that survives a password change; sessions and tokens had to be revoked to eject them.
    2. The sign-in success for j.okoro from the attacker IP at 09:08.
    3. It hides the attacker's tracks (moving replies out of sight) and shows intent: they were setting up to intercept payment and invoice threads, the start of business email compromise.

## Related pages

- [Phishing playbook](../../04-playbooks/phishing.md)
- [Account compromise playbook](../../04-playbooks/account-compromise.md)
- [Business email compromise playbook](../../04-playbooks/business-email-compromise.md)
