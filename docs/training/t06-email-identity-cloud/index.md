# T06: Email, Identity and Cloud Security

The three places most modern attacks actually happen: the inbox, the identity provider, and the cloud control plane. This module teaches how to read their logs and investigate the attacks that target them.

!!! abstract "At a glance"
    - Level: L2
    - Time: 6 to 8 hours with labs
    - Outcome: you can investigate phishing, account takeover and cloud key abuse from the logs

## Learning objectives

- [ ] Read email headers and mail flow to investigate phishing and business email compromise.
- [ ] Read identity sign-in and audit logs (Entra ID, Okta, Google).
- [ ] Read cloud audit logs (AWS CloudTrail, Azure, Google Cloud).
- [ ] Spot the signals of account takeover and cloud key abuse.
- [ ] Understand why identity is the perimeter in the cloud.

## Lessons

1. **Email.** Mail flow, headers (From, Reply-To, Received, SPF, DKIM, DMARC), message trace, inbox rules and forwarding.
2. **Phishing and BEC in the logs.** Look-alike domains, new inbox rules with financial keywords, external forwarding, mailbox access from odd places.
3. **Identity.** Sign-in logs (result, risk, IP, device), audit logs (MFA changes, app consent), what impossible travel looks like.
4. **Account takeover signals.** Login from a new country then a mailbox rule; new MFA method on an admin; token reuse.
5. **Cloud audit logs.** CloudTrail and the equivalents: management events, who did what, in which region.
6. **Cloud key abuse.** Key use from a new place, new identities created, logging turned off, resource hijacking; identity as the perimeter.

## Lab

- [ ] Take a phishing email sample and read its headers: is the sender real, does DMARC pass, where does the link go?
- [ ] In a free cloud account, generate audit log events (create a user, create a key) and find them in the log.
- [ ] Write the query for "everything this access key did" (see the [cloud playbook](../../04-playbooks/cloud-account-compromise.md)).
- [ ] List the sign-in fields that would show an account takeover.

## Self-check

1. Which email header helps you spot a display-name impersonation?
2. What sign-in pattern suggests account takeover?
3. Why is "identity is the perimeter" true in the cloud?

??? note "Answers"
    1. Compare From and Reply-To, and check the real sending domain and SPF, DKIM and DMARC results; a faked display name over an external address is a classic trick.
    2. A successful sign-in from a new country, device or hosting-provider IP, especially followed by a mailbox rule, MFA change, or sensitive access.
    3. Cloud attacks use valid credentials and the same API calls as your engineers, with no malware. Controlling identity (keys, sessions, MFA) is what keeps attackers out.

## Links to the handbook and kit

- [Phishing playbook](../../04-playbooks/phishing.md), [Business email compromise](../../04-playbooks/business-email-compromise.md)
- [Account compromise](../../04-playbooks/account-compromise.md), [Cloud account compromise](../../04-playbooks/cloud-account-compromise.md)

## Next module

[T07 Threat Intelligence](../t07-threat-intelligence/index.md).
