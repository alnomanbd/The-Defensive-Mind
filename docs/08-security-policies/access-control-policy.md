# Access Control Policy

A ready-to-adapt policy for who gets access to what, and how access is granted, changed and removed. Weak access control is behind a large share of breaches: too much access, access that was never removed, and admin rights everywhere. Fill in the placeholders and get it approved.

!!! abstract "At a glance"
    - Audience: IT, security, managers, HR (for joiners and leavers)
    - Time to read: 8 minutes
    - Outcome: an approved standard the SOC can detect and audit against

---

## Policy: Access Control

**Purpose.** To make sure people have the access they need to do their job, and no more, and that access is removed when it is no longer needed.

**Scope.** All `[ORGANISATION]` systems, applications and data, and all accounts including staff, contractors, service accounts and administrators.

### Principles

1. **Least privilege.** People get the minimum access needed for their role. Extra access is requested, justified and approved, not granted by default.
2. **Need to know.** Access to sensitive data is limited to those who need it for their work.
3. **Role-based where possible.** Access is granted through roles tied to job functions, not handed out one system at a time.
4. **Separation of duties.** No single person can both perform and approve a sensitive action (for example, request and approve their own access, or make and release a payment alone).

### Granting access

5. Access is **requested and approved** by `[the data or system owner and the person's manager]` before it is granted.
6. **Administrator and privileged access** is granted only where genuinely needed, approved separately, and reviewed more often.
7. Administrators use a **separate admin account** for admin work, not their everyday account, and that account is protected with strong MFA.
8. **Service accounts** have only the access they need, are documented with an owner, and their secrets are managed properly.

### Changing and removing access

9. When someone **changes role**, their old access is reviewed and removed, not just added to. Access creep is a real risk.
10. When someone **leaves**, all access is removed on their **last day** (or immediately if the departure is not amicable). HR notifies IT and the SOC of leavers in advance where possible.
11. **Access is reviewed regularly:** at least `[every 6 months]` for normal access and `[every 3 months]` for privileged access. Owners confirm who should still have access; the rest is removed.
12. **Dormant accounts** (no login for `[90]` days) are disabled after review.

### Roles

- **System and data owners** approve and review access.
- **IT** grants, changes and removes access and runs the reviews.
- **HR** notifies of joiners, movers and leavers.
- **The SOC** detects access abuse, new privileged accounts, and access that breaks this policy.

### Exceptions, enforcement, owner

Exceptions in writing to `[role]`, time-limited. Breaches handled under `[HR process]`. **Owner:** `[role]`. **Approved by:** `[role]`. **Next review:** `[date]`.

---

## Guidance (not part of the policy)

!!! warning "The leaver gap is a classic breach"
    Access that outlives the person's need for it is one of the most common findings after an incident. A leaver whose access was never removed, or a mover who kept every role they ever had, is a ready-made entry point. The leaver step on the **last day** is not a nicety; it is a control. Automate the joiner, mover and leaver process if you can.

!!! tip "Privileged access deserves extra care"
    Administrator accounts are the keys to everything. Keep them few, separate them from everyday accounts, protect them with the strongest MFA, review them most often, and watch them most closely. A single over-privileged, poorly protected admin account can undo every other control.

## What the SOC detects against this policy

- New administrator accounts or privilege grants ([account compromise](../04-playbooks/account-compromise.md)).
- Access used after someone has left.
- Dormant accounts suddenly active.
- Admin accounts used for everyday activity (a sign of misuse or compromise).
- Service accounts behaving like interactive users.

## Related pages

- [Password and MFA policy](password-and-mfa-policy.md)
- [Acceptable use and endpoint policy](acceptable-use-and-endpoint-policy.md)
- [Insider threat playbook](../04-playbooks/insider-threat.md)
- [Cloud account compromise playbook](../04-playbooks/cloud-account-compromise.md)
