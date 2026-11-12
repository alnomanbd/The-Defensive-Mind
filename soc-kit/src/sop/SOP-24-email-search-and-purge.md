---
id: SOP-24
title: Email Search and Purge
owner: SOC Lead
audience: L2 analysts, email administrators
review: Every 12 months
summary: How to find every copy of a malicious email across all mailboxes and remove it safely, so a phishing campaign is pulled before more people fall for it.
---
## 1. Purpose

When one malicious email is confirmed, others usually received it too. This procedure finds every copy across the organisation and removes it, so the campaign is contained before more people click. It also keeps a copy as evidence first.

## 2. Scope

Searching and purging email across [ORGANISATION] mailboxes, done by an authorised email administrator with the SOC.

## 3. Before you purge

- [ ] Confirm the email is malicious, not just unwanted; purging the wrong mail removes legitimate messages.
- [ ] Keep a copy as evidence (the .eml with headers) before removal.
- [ ] Record the search criteria you will use.

> WARNING: Purge removes mail from people's mailboxes. A too-broad search can delete legitimate email. Define the search tightly (specific sender, subject, time window, attacker URL) and confirm the match count looks right before purging.

## 4. Procedure

### 4.1 Search

1. Build the search from reliable criteria: sender address, subject, attacker URL or domain, and a time window.
2. Run the search across all mailboxes.
3. Review the match count and a sample; confirm the matches are the malicious email, not a broader set.

### 4.2 Scope

- [ ] How many recipients, and who? Note any high-value recipients (finance, executives, admins).
- [ ] Who already clicked or interacted? Those accounts need follow-up (SOP-23, SOP-25).

### 4.3 Purge

1. Soft-delete (move to a recoverable location) rather than hard-delete where the tool allows, so a mistake can be undone.
2. Purge the confirmed malicious email from all matched mailboxes.
3. Confirm the removal succeeded.

### 4.4 Block and prevent recurrence

- [ ] Block the sender, domain and URL at the mail gateway so new copies do not arrive.
- [ ] Add the indicators to watchlists.

## 5. Platform notes

Use your platform's eDiscovery or search-and-purge feature (for example a content search and purge action, or the equivalent admin tool). Keep the exact steps for your platform in a short runbook alongside this procedure.

## 6. Records

Record the search criteria, the number removed, high-value recipients, who interacted, and the blocks applied.

## 7. Review

Reviewed every 12 months.
