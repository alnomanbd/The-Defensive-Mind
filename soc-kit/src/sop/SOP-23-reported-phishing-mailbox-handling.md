---
id: SOP-23
title: Reported Phishing Mailbox Handling
owner: SOC Lead
audience: L1 and L2 analysts
review: Every 12 months
summary: How to handle an email a user reported as suspicious, from the shared reporting mailbox or the report button, quickly and consistently, so real phishing is caught and the reporter is thanked.
---
## 1. Purpose

Users are the SOC's largest sensor. A reported email is often the first sign of a phishing campaign. This procedure handles reports fast and consistently, so a real attack is caught early and reporters keep reporting because it is easy and valued.

> NOTE: Thank every reporter, even for a false alarm. Reporting is a behaviour you want to encourage. One dismissive response and people stop reporting, and the next real phish goes unreported.

## 2. Scope

Emails reported by staff through the report button or the shared phishing mailbox for [ORGANISATION].

## 3. Procedure

### 3.1 Triage (first 15 minutes)

- [ ] Get the email safely: as an attachment (.eml or .msg) with full headers, not forwarded inline.
- [ ] Check the sender: real domain versus display name, SPF, DKIM and DMARC results, Reply-To.
- [ ] Check links: where they really go; look-alike domains; a credential-harvesting login page.
- [ ] Check attachments: type, and whether they ask to enable content or macros.
- [ ] Confirm it is not an authorised simulation (check the awareness schedule).

### 3.2 Decide the verdict

| Verdict | Action |
|---|---|
| Benign (legitimate mail) | Reply to the reporter: safe, thanks for checking. Close |
| Spam, not malicious | Mark as spam; close with a note |
| Malicious phishing, nobody interacted | Purge the campaign (SOP-24); block the sender and domain |
| Malicious and someone clicked or entered credentials | Escalate: run the phishing and account compromise playbooks |

### 3.3 Ask the key question

- [ ] Did anyone click the link or enter credentials? Check URL-click logs and ask the reporter.
- [ ] If yes, treat the affected account as possibly compromised (SOP-25 and the account compromise playbook).

### 3.4 Scope the campaign

- [ ] Find everyone who received it: message trace by sender, subject, or attacker URL.
- [ ] Check who clicked or replied.
- [ ] Extract indicators (sender, domain, URL, hash) for blocking and watchlisting.

### 3.5 Respond and close

- [ ] Purge the malicious email from all mailboxes (SOP-24).
- [ ] Block the sender, domain and URL.
- [ ] Reset any accounts whose credentials were entered.
- [ ] Reply to the reporter with thanks and the outcome in plain terms.
- [ ] Record the verdict, scope, indicators and actions.

## 4. Feeding improvement

Use real reported phishing to tune detections and to inform awareness training. A campaign that got through is a detection gap and a training opportunity.

## 5. Review

Reviewed every 12 months.
