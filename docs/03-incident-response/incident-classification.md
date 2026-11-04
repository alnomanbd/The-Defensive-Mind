# Incident Classification

How to label an incident by type and severity in under a minute, the same way every time, so the right playbook starts, the right people are called, and the monthly numbers mean something.

!!! abstract "At a glance"
    - Audience: L1 / L2 analysts, incident leads
    - Time to read: 8 minutes
    - Outcome: you can classify any incident by type, severity and data impact, and know when to change the classification

## Step 1: Is it an incident?

| It is an incident when | It is not (yet) an incident when |
|---|---|
| Confidentiality, integrity or availability was harmed or is at clear risk | A blocked attempt with no follow-on activity |
| Security policy was broken in a way that matters (data copied to personal cloud) | A false positive or authorised activity |
| A credible outside report says we are breached | Unconfirmed rumours (investigate as a case first) |

## Step 2: Type

Use one primary type. Add secondary types in the case if more apply.

| Type | Examples | Playbook |
|---|---|---|
| Phishing and social engineering | Credential phishing, malicious attachment, vishing, deepfake call | [Phishing](../04-playbooks/phishing.md) |
| Business email compromise | Invoice fraud, CEO fraud, mailbox forwarding | Business email compromise |
| Account compromise | Stolen password, MFA fatigue, session theft, impossible travel | [Account compromise](../04-playbooks/account-compromise.md) |
| Credential exposure | Credentials in a breach dump, infostealer log or public code | [Credential leak](../04-playbooks/credential-leak-dark-web.md) |
| Brute force | Password guessing, spraying, credential stuffing | [Brute force](../04-playbooks/brute-force.md) |
| Malware | Infostealer, trojan, worm, cryptominer | Malware and infostealer |
| Ransomware and destructive | Encryption, wiper, extortion | Ransomware |
| Web and application attack | SQL injection, web shell, exploitation | Web application attack |
| Data loss or exposure | Exfiltration, misconfigured storage, misdirected email | Data exfiltration |
| Denial of service | Volumetric, application-layer, ransom DDoS | DDoS |
| Insider | Malicious or negligent employee or contractor | Insider threat |
| Cloud and SaaS | Stolen keys, rogue OAuth app, exposed bucket | Cloud account compromise |
| Supply chain and third party | Compromised vendor, malicious update, vendor breach | Supply chain |
| Policy violation | Unapproved software, shadow IT, misuse | Handled with HR and IT |

## Step 3: Severity

Score impact and urgency, then read the severity.

| Impact | Score |
|---|---|
| Many systems, a critical service, or regulated data (personal, payment, health) | 3 |
| One important system, a privileged account, or confidential data | 2 |
| One ordinary user or system, no sensitive data | 1 |

| Urgency | Score |
|---|---|
| Active and spreading, or data leaving now | 3 |
| Confirmed but contained | 2 |
| Attempt only, or past activity with nothing ongoing | 1 |

| Total | Severity | Response |
|---|---|---|
| 6 | P1 Critical | 15 minutes, 24x7, hourly updates |
| 5 | P2 High (P1 if regulated data) | 1 hour, 24x7, updates every 4 hours |
| 3 to 4 | P3 Medium | 4 business hours, daily update |
| 2 | P4 Low | Next business day, weekly report |

### Automatic P1

- [ ] Ransomware or wiper confirmed anywhere
- [ ] Domain admin, cloud root or global admin compromised
- [ ] Confirmed theft of personal, payment or health data
- [ ] Security team's own tools or accounts compromised
- [ ] Attacker has interactive access to production
- [ ] A regulator, law enforcement or the media reports a breach

## Step 4: Data impact

Data impact drives legal duties, so record it separately from severity.

| Data category | Examples | Who must be told inside |
|---|---|---|
| Personal data | Names, emails, ID numbers, location | Privacy officer, legal |
| Special category data | Health, biometrics, religion, union membership | Privacy officer, legal, CISO |
| Payment card data | Card numbers, CVV | PCI DSS owner, legal, acquiring bank via the business |
| Credentials and secrets | Passwords, API keys, tokens | System owners, IT |
| Confidential business data | Contracts, source code, strategy | Data owner, legal |
| None confirmed | | |

## Step 5: Re-classify as you learn

| Trigger | Action |
|---|---|
| New affected systems or data found | Raise severity now, do not wait |
| Containment confirmed and no data involved | Lower severity with evidence and the lead's agreement |
| Incident turns out to be a different type (phishing became account compromise) | Add the type, open the second playbook, keep one case |
| False positive after all | Close with evidence; keep the record |

Every change is written in the timeline with time, reason and who decided.

## Taxonomies you may need to map to

| Taxonomy | Used by |
|---|---|
| VERIS (Vocabulary for Event Recording and Incident Sharing) | Breach reporting and statistics |
| ENISA Reference Incident Classification Taxonomy | European CSIRTs |
| MITRE ATT&CK | Describing attacker behaviour, not incident type |
| Local regulator categories | National CERT or regulator reporting forms |

Keep your own simple list (above) and map to these when reporting outside.

## Related pages

- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
- [IR lifecycle](ir-lifecycle.md)
- [Escalation and communication](escalation-and-communication.md)
- [Playbooks](../04-playbooks/index.md)
