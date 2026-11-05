# Case Walkthroughs

Six realistic cases, each told from the first alert to the lessons learned, the way a SOC actually works them. Read the alert, decide what you would check, then follow the investigation and compare. Each case ends with a short quiz.

!!! abstract "At a glance"
    - Audience: analysts at every level, and anyone training
    - Time to read: 15 to 25 minutes per case
    - Outcome: you have worked six common attacks end to end, with the queries and decisions

## How to use these

1. **Read the alert** as it arrives. Stop and write what you would check first.
2. **Follow the triage** and run the queries in your own lab if you can.
3. **Read the escalation note** and compare it with yours.
4. **Follow the investigation and timeline.** Watch how each finding leads to the next pivot.
5. **Note the containment** and who approved each action.
6. **Answer the quiz** before opening the answers.

!!! tip "The point is the reasoning, not the answer"
    The value is in why each pivot was made, not in the final verdict. If you can explain why the analyst looked where they did, you can work the next case that looks nothing like this one.

## The cases

| Case | Attack | Starts from | Teaches |
|---|---|---|---|
| [01](case-01-phishing-to-credential-theft.md) | Phishing to credential theft | A reported email | Email triage, "did they click", account takeover scoping |
| [02](case-02-brute-force-then-success.md) | Brute force then a success | Many failed logins | Noise vs targeted, the success-after-failure pivot |
| [03](case-03-infostealer-on-laptop.md) | Infostealer on a laptop | An EDR detection | Did it run, what it stole, session and credential reset |
| [04](case-04-web-secret-file-probing.md) | Web secret-file probing | Web and WAF alerts | Scanning vs a hit, "did any request succeed", secrets |
| [05](case-05-suspicious-mailbox-forwarding-bec.md) | Mailbox forwarding (BEC) | A finance query | Hidden inbox rules, payment recall, out-of-band comms |
| [06](case-06-cloud-key-leak-cryptomining.md) | Cloud key leak and cryptomining | A billing or GuardDuty alert | Leaked key scoping, all-regions, persistence, logging |

## A note on realism

These cases use invented names, IPs and domains. The behaviours, queries and decisions are real and match the [playbooks](../../04-playbooks/index.md). When you meet the real thing, it will look different in the details and the same in the shape. Learn the shape.

## Related pages

- [Playbooks](../../04-playbooks/index.md)
- [Investigation cheat sheet](../investigation-cheatsheet.md)
- [Alert triage](../../02-daily-operations/alert-triage.md)
- [IR lifecycle](../../03-incident-response/ir-lifecycle.md)
