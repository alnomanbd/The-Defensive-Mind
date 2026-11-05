# Case 05: Suspicious Mailbox Forwarding (BEC)

Finance asks why a supplier payment went to a new bank account. The trail leads to a hidden mailbox rule and a compromised account. This case is about business email compromise: find the rule, start the money recall, and work out loud without tipping off the attacker.

!!! abstract "At a glance"
    - Attack: business email compromise through a compromised mailbox
    - Starts from: a finance query about a payment
    - Playbook: [Business email compromise](../../04-playbooks/business-email-compromise.md)

## The alert

```text
10:50 UTC. Not an automated alert: a finance manager emails the SOC.
"We paid an invoice to a supplier, but they say they never changed their bank details
and never got the money. The email asking us to change the account came from our usual
contact, l.moreau. Amount: 48,000."
```

**Stop. What is the first thing you do, before any investigation?** Write it down.

## L1 triage

| Check | Finding |
|---|---|
| Has money moved? | Yes, 48,000 paid to a new account this morning. Start the recall now |
| Whose account sent the request? | Internal: l.moreau (Accounts Payable). Either compromised or impersonated |
| Is it our real mailbox or a look-alike? | The email came from the real l.moreau mailbox, not a look-alike |
| Any inbox rule or forwarding on that mailbox? | Yes: a rule moving mail containing "invoice" or "bank" to a rarely used folder |

The first action is not investigation; it is telling finance to call the bank and start the recall. Minutes matter for recovering funds.

## Escalation to L2

```text
Escalated 11:02 UTC by L1. Finance already calling the bank for recall.
Verdict: likely BEC. l.moreau's real mailbox sent a bank-change request and has a hidden
inbox rule. Treat the mailbox as compromised.
Asks: confirm compromise, find the rule and any forwarding, scope what the attacker read,
warn the supplier through a known phone number.
```

## L2 investigation

Work the mailbox like an account takeover, and keep the investigation off the channels the attacker might be reading.

| Time (UTC) | Finding | Source |
|---|---|---|
| 3 days ago | l.moreau signed in from a new country right after a phishing email | Sign-in logs |
| 3 days ago | Inbox rule created: move "invoice", "bank", "payment" to Archive, mark read | M365 audit `New-InboxRule` |
| Over 3 days | Attacker read the supplier invoice thread | MailItemsAccessed |
| This morning | Reply sent inside the real thread with new bank details | Sent items, message trace |
| This morning | The supplier's genuine replies were auto-filed away, so staff never saw the mismatch | The inbox rule |

The attacker had been in for three days, learned the live invoice conversation, and replied inside it with new bank details, while the rule hid the supplier's real messages.

### Find the rule and forwarding

```powershell
Connect-ExchangeOnline
Get-InboxRule -Mailbox l.moreau@example.com | Select Name, Enabled, SubjectContainsWords, MoveToFolder, ForwardTo, DeleteMessage
Get-Mailbox l.moreau@example.com | Select ForwardingSmtpAddress, ForwardingAddress
Get-MessageTrace -SenderAddress l.moreau@example.com -StartDate (Get-Date).AddDays(-5) -EndDate (Get-Date)
```

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Finance calls the bank to recall or freeze the payment, files a fraud report | Finance | Immediate, done first |
| Reset l.moreau's password, revoke sessions, review MFA methods | Identity team | L2, confirmed compromise |
| Export then remove the malicious inbox rule | Email admin | L2 |
| Purge the attacker's emails; block their infrastructure | Email admin, SOC | L2 |
| Warn the supplier by a known phone number (not a number from email) | Finance or account manager | L2 |
| Check other finance mailboxes for the same attacker IP and rules | L2 | - |

The investigation was coordinated by phone and a separate chat, not l.moreau's mailbox, in case the attacker was still watching.

## Outcome

The payment recall, started in the first minutes, recovered most of the funds because the bank was told within hours. The compromise had lasted three days, hidden by the inbox rule. The attacker was ejected and no other mailbox was affected.

## Lessons learned

- [ ] A bank-detail change must be confirmed by phone to a known number, never from the email. Make this a hard finance rule.
- [ ] Detection added: inbox rules with financial keywords or that move mail to hidden folders, and sign-in from a new country followed by rule creation.
- [ ] Move finance to phishing-resistant MFA; the attacker got in through a phished code.
- [ ] Set DMARC to reject and enable impersonation protection for finance and key suppliers.

## Quiz

1. Why is the first action a phone call to the bank, not an investigation?
2. How did the attacker make the fraud so convincing?
3. Why coordinate the response off the compromised mailbox?

??? note "Answers"
    1. Payment recovery drops sharply after the first day. Starting the bank recall immediately is the only way to get the money back; the investigation can run in parallel.
    2. They used the real mailbox, replied inside the genuine invoice thread, and used an inbox rule to hide the supplier's real replies so nobody saw the mismatch.
    3. The attacker may still have access and be reading the mailbox. Discussing the response there would tip them off; use out-of-band channels.

## Related pages

- [Business email compromise playbook](../../04-playbooks/business-email-compromise.md)
- [Account compromise playbook](../../04-playbooks/account-compromise.md)
- [Escalation and communication](../../03-incident-response/escalation-and-communication.md)
