# Policy Framework

How to write, approve, publish and keep security policies alive, so they guide real behaviour instead of gathering dust. This page is the method; the other pages in this section are the policies themselves.

!!! abstract "At a glance"
    - Audience: CISO, security governance, SOC manager
    - Time to read: 8 minutes
    - Outcome: a simple structure for policies and a process that keeps them current

## The document hierarchy

Keep the layers clear. People confuse these and end up with policies full of technical detail that date fast.

| Layer | What it is | Example | Changes |
|---|---|---|---|
| Policy | What must happen and why. Short, stable | "All remote access requires MFA" | Rarely |
| Standard | The specific rules that meet the policy | "MFA means an authenticator app or hardware key, not SMS" | Occasionally |
| Procedure | The step-by-step how | "How to enrol a hardware key" | Often |
| Guideline | Recommended good practice, not mandatory | "Prefer a password manager" | As needed |

Put the lasting intent in the policy and the changeable detail in standards and procedures. Then a new tool means updating a procedure, not reopening the policy.

## What every policy contains

Keep it to a page or two. A simple structure:

| Section | Content |
|---|---|
| Purpose | One or two sentences: why this policy exists |
| Scope | Who and what it applies to |
| Policy statements | The rules, as short numbered points |
| Roles | Who is responsible for what |
| Exceptions | How to request an exception, who approves, time-limited |
| Enforcement | What happens if it is not followed |
| Owner and review | Who owns it and when it is next reviewed |

## The lifecycle

A policy is not done when it is written. It lives or dies by this cycle.

```text
Draft -> Review (security, legal, affected teams) -> Approve (named authority)
  -> Publish (where people can find it) -> Communicate (so people know)
  -> Follow -> Review on schedule and after incidents -> Update -> repeat
```

- [ ] Draft it short and in plain language.
- [ ] Review with security, legal or HR where relevant, and the teams who must follow it.
- [ ] Get it approved by a named authority with the standing to enforce it.
- [ ] Publish it somewhere everyone can find, not buried in a shared drive.
- [ ] Communicate it; a policy nobody was told about is not in force in practice.
- [ ] Review on a schedule (yearly is common) and after any incident it touched.

!!! tip "Approval needs authority"
    A policy approved by someone who cannot enforce it is a suggestion. Get sign-off from a role with the standing to require compliance, usually an executive or the CISO, and record who approved it and when.

## Exceptions, done right

People will have genuine reasons they cannot meet a policy. Handle exceptions openly so they do not become quiet, permanent holes.

- [ ] Every exception is requested in writing, with a reason.
- [ ] A named person approves it, weighing the risk.
- [ ] It is time-limited and has a review date; no permanent exceptions by default.
- [ ] Exceptions are recorded in one place, so the real risk is visible.

An undocumented exception is just a rule being broken. A documented, time-limited one is a managed risk.

## Mapping to standards and compliance

If you follow a framework (ISO/IEC 27001, NIST CSF, SOC 2, PCI DSS, CIS Controls), map your policies to its requirements. This shows coverage, avoids gaps, and makes audits far easier. You do not need to adopt a framework to have good policies, but mapping to one helps you check you have not missed something important.

## Common mistakes

| Mistake | Fix |
|---|---|
| Fifty-page policies nobody reads | One or two pages, plain language |
| Technical detail in the policy itself | Detail goes in standards and procedures |
| Approved once, never reviewed | A review date and owner on every policy |
| Published where nobody looks | One known home, and active communication |
| No exception process | A written, time-limited exception process |
| Copied from a template and never adapted | Fill in every placeholder; make it yours |

## Related pages

- [Security Policies index](index.md)
- [Incident reporting policy](incident-reporting-policy.md)
- [Maturity model](../01-build-a-soc/maturity-model.md)
- [Post-incident review](../03-incident-response/post-incident-review.md)
