# Acceptable Use and Endpoint Policy

A ready-to-adapt policy for what people may and may not do with company devices and systems, and how endpoints (laptops, desktops, phones) must be protected. Fill in the placeholders and get it approved.

!!! abstract "At a glance"
    - Audience: all staff (as the rule), IT, security, HR (as owners)
    - Time to read: 8 minutes
    - Outcome: a clear, fair acceptable-use standard the SOC can support

---

## Policy: Acceptable Use and Endpoint Security

**Purpose.** To set out how `[ORGANISATION]` devices, systems and data may be used, and how endpoints are kept secure, so the organisation and its people are protected.

**Scope.** All staff and contractors, all `[ORGANISATION]` devices and systems, and any personal device used for work (if allowed).

### Acceptable use

1. Company systems are for business use. **Reasonable personal use** is allowed where it does not break the law, harm security, or interfere with work.
2. **Do not** use company systems for anything illegal, for harassment, or to access or share material that is clearly inappropriate for work.
3. **Do not** try to bypass security controls (disabling the EDR agent, using unapproved VPNs or anonymisers, cracking or sharing passwords).
4. **Do not** install unapproved software, or connect unapproved devices (personal USB drives) to company endpoints, where this is restricted.
5. **Do not** move company data to personal accounts, personal cloud storage, or personal email.
6. Use only **approved cloud and SaaS services** for company data. If a new tool is needed, request it through `[process]`.

### Endpoint security

7. Company endpoints run the **approved security agent (EDR)**, which must not be disabled or removed.
8. Endpoints are **encrypted** (full-disk encryption) and **lock automatically** after `[10]` minutes.
9. Operating systems and software are kept **up to date**; security updates are not postponed indefinitely.
10. Users work from a **standard (non-administrator) account** for daily work. Administrator rights are granted only where needed and separately.
11. **Lost or stolen devices** are reported immediately through the [incident reporting](incident-reporting-policy.md) process so they can be locked or wiped.
12. **Personal devices used for work** (if allowed) must meet `[the minimum security requirements: screen lock, encryption, up to date, approved management]`.

### Monitoring and privacy

13. `[ORGANISATION]` monitors its systems and devices for security purposes. Monitoring is **proportionate**, focused on protecting the organisation, and carried out in line with `[local law and the privacy notice]`.
14. Security monitoring is not used to track personal productivity beyond what `[policy and law]` allow.

### Roles

- **IT** configures and maintains endpoint security.
- **The SOC** monitors for breaches of this policy and for threats.
- **HR** handles misuse under the disciplinary process.
- **Every user** follows this policy and reports problems.

### Exceptions, enforcement, owner

Exceptions in writing to `[role]`, time-limited. Breaches handled under `[HR process]`. **Owner:** `[role]`. **Approved by:** `[role]`. **Next review:** `[date]`.

---

## Guidance (not part of the policy)

!!! tip "Be clear and fair, or people route around you"
    A policy that bans all personal use, or that reads as surveillance, pushes people to use personal devices and accounts for work, which is worse for security. Allow reasonable personal use, be honest and proportionate about monitoring, and make the secure path the easy path.

!!! warning "Monitoring has legal limits"
    What you may monitor, and how you must tell people, varies by country and can involve works councils or data-protection law. Have `[legal]` review the monitoring section, and make sure a privacy notice tells staff what is monitored and why. Over-broad monitoring can be unlawful and destroys trust.

## What the SOC detects against this policy

- EDR agent disabled or missing on an endpoint (a key [self-monitoring](../05-detection-engineering/index.md) signal).
- Company data moving to personal cloud or email ([data exfiltration playbook](../04-playbooks/data-exfiltration.md)).
- Unapproved software or remote-access tools installed.
- Unapproved USB mass storage use.
- Out-of-date or unencrypted endpoints.

## Related pages

- [Password and MFA policy](password-and-mfa-policy.md)
- [Access control policy](access-control-policy.md)
- [Employee security guide](employee-security-guide.md)
- [Insider threat playbook](../04-playbooks/insider-threat.md)
