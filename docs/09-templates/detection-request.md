# Detection Request Template

Use this form to ask detection engineering for a new detection rule or a change to an existing one. Anyone can raise it: analysts, threat intel, incident handlers or other teams.

!!! abstract "At a glance"
    - Audience: SOC analyst L1-L3 (requester) / detection engineer (owner)
    - Time to complete: 15-30 minutes
    - Outcome: a request with enough detail to build, test and deploy a rule without a long back-and-forth

!!! tip "How to use"
    - Describe the **behaviour** you want to catch, not just one indicator. Hashes and IPs belong in a block list, not a rule.
    - Attach at least one real or simulated log sample. No sample usually means no rule.
    - Say what the analyst should do when the alert fires; a rule without a response is noise.
    - For tuning requests, include alert IDs that show the false positives.

---

## Detection request: `<DET-YYYY-NNNN>`

### Request details

| Field | Value |
|---|---|
| Request type | `<New rule / Tune existing rule / Retire rule>` |
| Existing rule ID (if tuning) | `<rule ID or N/A>` |
| Requested by | `<name, team>` |
| Date | `<YYYY-MM-DD>` |
| Priority | `<Urgent (active threat) / High / Normal / Low>` |
| Trigger | `<Incident / Threat intel / Post-incident review action / Audit / Coverage gap>` |
| Related record | `<INC-..., PIR-..., intel report>` |

### What should be detected

| Field | Value |
|---|---|
| Behaviour (plain English) | `<...>` |
| MITRE ATT&CK technique(s) | `<T....>` |
| Affected platforms | `<Windows / Linux / macOS / Cloud / Network / SaaS>` |
| Scope | `<All hosts / Domain controllers / Finance users / ...>` |

### Data needed

| Log source | Event / field | Already in SIEM? |
|---|---|---|
| `<...>` | `<...>` | `<Yes / No, needs onboarding request>` |

### Detection logic (draft)

```text
<plain-language or pseudo-query logic: WHEN ... AND ... WITHIN ... THEN alert>
```

### Test data

- Sample event(s): `<attach or link>`
- Simulation method: `<Atomic Red Team test ID / manual steps / replay>`

### Expected volume and false positives

| Question | Answer |
|---|---|
| Expected alerts per day | `<...>` |
| Known legitimate activity that looks the same | `<...>` |
| Suggested exclusions | `<...>` |

### Response

| Field | Value |
|---|---|
| Suggested severity | `<Critical / High / Medium / Low>` |
| Analyst first steps | `<...>` |
| Linked playbook | `<name>` |
| Automation possible? | `<Yes: enrichment / containment / No>` |

### Detection engineering use only

| Field | Value |
|---|---|
| Accepted / rejected | `<...>` (reason if rejected) |
| Rule ID and version | `<...>` |
| Tested on | `<date, method, result>` |
| Deployed on | `<date, change ID>` |
| Review date | `<+90 days>` |

---

## Worked example

??? example "Filled-in request: DET-2026-0144, Inbox rule after risky sign-in"
    | Field | Value |
    |---|---|
    | Request type | New rule |
    | Requested by | L2 analyst, SOC |
    | Priority | High |
    | Trigger | Post-incident review action PIR-A2 for INC-2026-0042 |

    **Behaviour:** A user signs in from a country never seen for that user, then within 60 minutes creates an inbox rule that forwards, redirects or deletes mail. **ATT&CK:** T1078 Valid Accounts, T1114.003 Email Forwarding Rule. **Platform:** cloud email and identity provider.

    | Log source | Event / field | In SIEM? |
    |---|---|---|
    | Identity provider sign-in logs | user, source IP, country, result | Yes |
    | Mail audit log | new inbox rule, rule actions, target address | Yes |

    ```text
    WHEN sign-in success for user U from country C
      AND C not in U's countries over the last 30 days
    AND within 60 minutes: inbox rule created by U
      with action forward / redirect / delete
    THEN alert High, include rule details and sign-in IP
    ```

    **Test:** replay of INC-2026-0042 events; second test with a lab account signing in through a VPN exit in another country.

    **Expected volume:** 0-2 per week. **Known false positives:** staff travelling who also tidy their mailbox. **Exclusion:** none at first; review after 30 days.

    **Analyst first steps:** check the rule target address; if external, disable the account, revoke sessions and remove the rule, then follow the account compromise playbook.

    **Result:** accepted; rule `det-email-0031` v1.0 deployed 2026-04-02 under CHG-2026-0291; test fired 2 of 2 times; review 2026-07-01.

## Checklist

- [ ] Behaviour described, not just indicators
- [ ] ATT&CK technique mapped
- [ ] Log source confirmed in the SIEM
- [ ] Sample event or simulation attached
- [ ] Analyst response steps written
- [ ] Review date set after deployment

## Related pages

- [Log source onboarding request](log-source-onboarding-request.md)
- [Change request template](change-request.md)
- [Open-source SOC lab](../10-labs-and-tools/open-source-soc-lab.md)
- [Templates overview](index.md)
