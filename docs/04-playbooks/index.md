# Playbooks

Step-by-step procedures for the incident types a SOC meets most often. Open the playbook as soon as triage confirms what kind of incident you have, and work it top to bottom.

!!! abstract "At a glance"
    - Audience: SOC analyst L1 / L2, incident lead
    - Time to read: 3 minutes
    - Outcome: you know which playbook to open, how they are laid out, and when to leave one for another

## Available playbooks

| ID | Playbook | Open it when... | Default severity |
|---|---|---|---|
| PB-01 | [Phishing](phishing.md) | A user reports a suspicious email, or the mail gateway flags one that was delivered | Low to High |
| PB-02 | [Business email compromise](business-email-compromise.md) | A payment or bank detail change request, a hidden inbox rule, or an executive impersonated | High |
| PB-03 | [Account compromise](account-compromise.md) | A login, mailbox rule or token use looks like someone other than the owner | High |
| PB-04 | [Brute force](brute-force.md) | Repeated login failures, password spraying, or a success after failures | Low to Critical |
| PB-05 | [Credential leak (dark web)](credential-leak-dark-web.md) | Company credentials appear in a breach dump, paste, infostealer log or leak forum | Medium to High |
| PB-08 | [Malware and infostealer](malware-infostealer.md) | EDR or antivirus detects malware, or a process steals browser passwords and cookies | Medium to High |
| PB-09 | [Ransomware](ransomware.md) | Files are being encrypted, a ransom note appears, or backups and shadow copies are deleted | Critical |
| PB-11 | [Web application attack](web-application-attack.md) | SQL injection, XSS, path traversal, secret file probing, or a web shell | Low to Critical |
| PB-13 | [Data exfiltration](data-exfiltration.md) | Unusual outbound volume, uploads to personal cloud, DLP match, DNS tunnelling | High |
| PB-14 | [Insider threat](insider-threat.md) | An employee or contractor misuses legitimate access; HR or manager referral | High |
| PB-15 | [DDoS](ddos.md) | A site, API or link is flooded and slow or down | Medium to Critical |
| PB-16 | [Cloud account compromise](cloud-account-compromise.md) | A cloud key, console user or service principal is used by someone else | High to Critical |

IDs follow the full [SOC Document Kit](../soc-kit/index.md) catalogue of 46 playbooks, so gaps in the numbers are playbooks that exist in the plan and will be added. Every playbook here is also available as a Word document in the kit.

## How every playbook is laid out

All playbooks follow the [playbook template](playbook-template.md), so you always find the same thing in the same place:

| Section | What you get |
|---|---|
| Header table | ID, default severity, when to raise it to Critical, MITRE ATT&CK techniques, owner |
| 1. Summary | What the incident is and what "done" looks like |
| 2. Triggers and detection | The alerts and log sources that start this playbook |
| 3. Triage | The first 15 to 30 minutes: confirm, scope roughly, set severity |
| 4. Investigation | Queries and questions to find the full scope |
| 5. Containment | Actions to stop the damage, with who approves them |
| 6. Eradication and recovery | Remove the cause and return to normal |
| 7. Communication | Who to tell, when, and what to say |
| 8. Evidence to keep | What to save for the case and any later review |
| 9. Lessons learned | What to fix so it does not happen again |

## Rules for using playbooks

- [ ] Note in the case which playbook you are following and the step you reached.
- [ ] Skip a step only with a written reason in the case notes.
- [ ] If the incident turns into another type (phishing that led to account compromise), open the second playbook and link both in the case.
- [ ] Containment steps that affect users or production need the approval named in the playbook.
- [ ] After every real incident, update the playbook if any step was wrong, missing or slow.

## Related pages

- [Alert triage](../02-daily-operations/alert-triage.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [Incident report template](../09-templates/incident-report.md)
- [Post-incident review template](../09-templates/post-incident-review-template.md)
