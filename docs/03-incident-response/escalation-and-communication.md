# Escalation and Communication

Who to tell, when, how and in what words during a security incident. Poor communication turns small incidents into big ones: leaders surprised, teams duplicating work, customers hearing it from the news.

!!! abstract "At a glance"
    - Audience: incident leads, SOC managers, CISO office
    - Time to read: 12 minutes
    - Outcome: an escalation matrix, a communication rhythm, and ready-made message templates

## Escalation matrix

| Severity | Inside the SOC | Outside the SOC | How | Within |
|---|---|---|---|---|
| P1 Critical | L2, incident lead, SOC manager | CISO, IT operations lead, system owner; CISO decides on executives, legal, privacy, communications | Phone first, then incident channel and bridge | 15 minutes |
| P2 High | L2, incident lead; SOC manager informed | System owner, IT operations | Phone for the lead, chat and ticket for others | 1 hour |
| P3 Medium | L2 if needed | System owner | Ticket and chat | 4 business hours |
| P4 Low | None | Weekly report | Report | Weekly |

!!! warning "No voicemail dead ends"
    If a P1 contact does not answer in 10 minutes (30 for P2), call their backup, then their manager. Write every attempt in the timeline.

## The five-point escalation call

Use this every time, by phone or in writing:

```text
1. Who I am, and that this is a security incident, severity P_.
2. What happened, in one sentence.
3. What is affected, and whether it is still going on.
4. What we have done so far.
5. What I need from you, and by when.
```

## Communication rhythm

| Audience | P1 | P2 | Channel | Format |
|---|---|---|---|---|
| Incident team | Continuous | Continuous | Bridge and incident channel | Live |
| CISO and IT leadership | Every hour | Every 4 hours | Sitrep by email or chat | [Situation report](../downloads/soc-kit/tpl/TPL-11-situation-report.docx) |
| Executives | Every 4 hours or at milestones | Daily if needed | Briefing by the CISO | Bottom line plus decisions |
| All staff | When they must act (password reset, do not open X) | Rarely | Email or intranet from communications | Short, action first |
| Customers and partners | Legal and communications decide | | Agreed statement | Reviewed by legal |
| Regulators | As law requires | | Formal notification | Legal leads |

## Out-of-band communication

If the attacker may be inside email or chat (domain admin compromise, mailbox access, compromised identity provider):

- [ ] Move the incident team to a pre-agreed out-of-band channel: phone bridge, a separate chat workspace, personal phones for calls
- [ ] Do not discuss the incident in channels the attacker might read
- [ ] Do not email the suspected compromised user about the investigation

## Legal and regulatory clocks

The SOC does not decide on notification, but must alert the CISO, privacy and legal **immediately** when any of these may be involved, because deadlines may already be running:

| Rule (examples) | Typical deadline |
|---|---|
| EU GDPR personal data breach | 72 hours to the supervisory authority after becoming aware |
| EU NIS2 significant incident | Early warning within 24 hours, notification within 72 hours |
| US SEC rule for listed companies | 4 business days after determining materiality |
| PCI DSS card data | Immediately to the acquiring bank and card brands as per contract |
| Sector or national rules | Check your country's CERT and regulator requirements |

Write down in advance which rules apply to your organisation and who decides.

## Message templates

### First notice to leadership (P1 or P2)

```text
Subject: [P1 SECURITY INCIDENT] <short title> - initial notice

What happened: <one or two sentences, facts only>
What is affected: <systems, users, data: confirmed / suspected / unknown>
Is it ongoing: <yes / no / unknown>
What we have done: <containment so far>
What we need: <decision or support, from whom, by when>
Next update: <time>
Incident lead: <name, phone>
```

### Staff action notice

```text
Subject: Action needed: reset your password today

We are dealing with a security issue affecting some staff accounts.
Please reset your password before 17:00 today at <official link typed by you, not copied from an email>.
IT will never ask for your password by phone or email.
Questions: <service desk number>.
```

### Holding statement (for communications and legal to adapt)

```text
We are investigating a cyber security incident affecting some of our systems.
We acted quickly to contain it and are working with specialists.
We will share more information as soon as we can. The security of our customers' data is our priority.
```

## Common mistakes

- Escalating by email at night.
- Calling leadership without a clear ask.
- Sending updates with speculation ("probably Russian hackers").
- Forgetting legal and privacy when personal data might be involved.
- Discussing a compromised identity provider over that same identity provider's chat.

## Downloads

- [SOP-05 Severity Assignment and Escalation](../downloads/soc-kit/sop/SOP-05-severity-assignment-and-escalation.docx)
- [TPL-07 Initial Notification](../downloads/soc-kit/tpl/TPL-07-incident-report-initial-notification.docx)
- [TPL-11 Situation Report](../downloads/soc-kit/tpl/TPL-11-situation-report.docx)

## Related pages

- [Incident classification](incident-classification.md)
- [IR lifecycle](ir-lifecycle.md)
- [Severity and SLA](../02-daily-operations/severity-and-sla.md)
