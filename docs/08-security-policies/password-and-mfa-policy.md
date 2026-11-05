# Password and MFA Policy

A ready-to-adapt policy for how accounts are protected: passwords, multi-factor authentication (MFA) and secrets. Fill in the placeholders, get it approved, and publish it. The guidance notes after the policy explain the choices.

!!! abstract "At a glance"
    - Audience: IT, security, all staff (as a standard to follow)
    - Time to read: 8 minutes
    - Outcome: an approved standard the SOC can detect and enforce against

---

## Policy: Password and MFA

**Purpose.** To protect `[ORGANISATION]` accounts from unauthorised access by setting clear rules for passwords, MFA and secrets.

**Scope.** All `[ORGANISATION]` accounts: staff, contractors, service accounts and administrative accounts, on all systems.

### Statements

1. **MFA is required** for all remote access, all administrator accounts, all email and all cloud and SaaS applications that support it.
2. **MFA must be phishing-resistant** where possible: an authenticator app or a hardware security key. **SMS and voice codes must not be used** for administrator or remote access, because they can be intercepted or SIM-swapped.
3. **Passwords must be long, not complex.** A minimum of `[12]` characters for users and `[16]` for administrators. Length beats forced symbols.
4. **No forced periodic password changes** for user accounts. Change a password only when there is a sign it may be compromised. Frequent forced changes lead to weaker, predictable passwords.
5. **Passwords are checked against a banned list** of common and breached passwords, and must not contain the company name, the season, or the year.
6. **Each person has their own account.** No shared accounts or shared passwords. Where a shared system is unavoidable, access is logged and the exception is approved.
7. **A company password manager** is provided and must be used for work passwords. Passwords must not be reused between work and personal accounts.
8. **Secrets** (API keys, tokens, service-account credentials) must be stored in an approved secrets manager, never in code, config files, email or chat.
9. **Compromise is reported immediately** through the [incident reporting](incident-reporting-policy.md) process. A suspected password exposure is reset at once.

### Roles

- **IT** enforces these settings in the identity system and provides the password manager.
- **The SOC** detects weak, shared or compromised credentials and policy breaches.
- **Every user** follows this standard and reports suspected compromise.

### Exceptions

Requested in writing to `[security team]`, approved by `[named role]`, time-limited and recorded.

### Enforcement

Breaches are handled under `[the acceptable use policy and HR process]`.

**Owner:** `[role]`. **Approved by:** `[role]`. **Next review:** `[date]`.

---

## Why these choices (guidance, not part of the policy)

Modern guidance (such as NIST) has moved away from old habits. The reasons:

| Rule | Why |
|---|---|
| Length over complexity | Long passphrases are stronger and easier to remember than short ones full of symbols |
| No forced rotation | Frequent changes make people pick weak, patterned passwords (`Spring2026!`). Change on evidence of compromise instead |
| Phishing-resistant MFA | SMS codes can be intercepted or SIM-swapped; app and hardware-key MFA resist phishing far better |
| Banned-password list | Stops the passwords attackers try first, which complexity rules alone do not |
| Password manager | Enables unique, strong passwords per site without memorising them |

!!! warning "MFA is not all equal"
    SMS MFA is far better than no MFA, but attackers defeat it with SIM swaps and real-time phishing. For administrators and remote access, use an authenticator app or, best of all, a hardware key or passkey. Reserve SMS for low-risk accounts only.

## What the SOC detects against this policy

- Logins without MFA where MFA is required.
- New or changed MFA methods, especially on admins (a common attacker move).
- Shared-account use (same credential, many hosts or locations at once).
- Credentials appearing in breach dumps or infostealer logs ([credential leak playbook](../04-playbooks/credential-leak-dark-web.md)).
- Secrets committed to code repositories.

## Related pages

- [Access control policy](access-control-policy.md)
- [Employee security guide](employee-security-guide.md)
- [Brute force playbook](../04-playbooks/brute-force.md)
- [Account compromise playbook](../04-playbooks/account-compromise.md)
