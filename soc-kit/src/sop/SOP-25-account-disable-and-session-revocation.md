---
id: SOP-25
title: Account Disable and Session Revocation
owner: SOC Lead
audience: L2 analysts, identity team
review: Every 12 months
summary: How to cut off a compromised account properly. A password reset alone is not enough; stolen sessions and tokens must be revoked, or the attacker stays in.
---
## 1. Purpose

When an account is compromised, the SOC must eject the attacker completely. The common mistake is resetting the password and stopping there, while a stolen session cookie or token keeps the attacker signed in. This procedure makes sure the account is truly cut off.

> WARNING: A password reset does not end existing sessions. Modern attacks steal session cookies and tokens, which bypass the password and MFA. You must revoke sessions and tokens as well, or the attacker remains logged in after the reset.

## 2. Scope

Containing a compromised or suspected-compromised account for [ORGANISATION]: user, admin or service accounts.

## 3. Choose the response

| Situation | Response |
|---|---|
| Confirmed compromise | Reset password, revoke all sessions and tokens, review MFA; consider disabling first if the user is unreachable |
| Strong suspicion, user unreachable | Disable the account to stop activity, then investigate |
| Executive, admin or privileged account | Same, with the approval in GOV-04 and the SOC manager informed |
| Service account | Rotate its credentials and keys; coordinate with the owner to avoid breaking a system |

## 4. Procedure

### 4.1 Contain

1. Reset the password (or disable the account if the user cannot be reached and the risk is high).
2. Revoke all active sessions and refresh tokens, so stolen sessions stop working.
3. Review MFA methods; remove any the attacker added, and re-enrol the user cleanly.
4. For a service account, rotate its secret or key with the owner.

### 4.2 Check for attacker persistence

- [ ] New or changed MFA methods.
- [ ] Inbox rules or mail forwarding (SOP-23, BEC playbook).
- [ ] OAuth app consents the attacker granted.
- [ ] New app passwords or API tokens.

Remove each one found; a reset without removing these leaves a way back in.

### 4.3 Restore access to the real user

1. Confirm the real user's identity through a trusted channel (not the compromised account).
2. Help them set a new password and re-enrol MFA.
3. Tell them what happened and what to watch for.

## 5. Approvals and care

- [ ] Follow GOV-04 for disabling executive, admin or privileged accounts.
- [ ] Avoid locking the business out: have a break-glass admin ready before disabling admin accounts.
- [ ] Do not contact the suspected-compromised account about the investigation from that account.

## 6. Records

Record the account, the actions (reset, revoke, MFA, persistence removed), the times, and who approved any disable.

## 7. Review

Reviewed every 12 months.
