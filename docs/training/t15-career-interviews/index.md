# T15: Career and Interviews

How to build a SOC career and get through the interviews. Skill paths from L1 to L3 and beyond, which certifications are worth it, and an interview question bank with model answers.

!!! abstract "At a glance"
    - Level: all
    - Time: 4 to 6 hours
    - Outcome: a plan for your next step and the confidence to interview for it

## Learning objectives

- [ ] Map the skill paths from L1 to L3 and into specialisms.
- [ ] Choose certifications that match your goal, without wasting money.
- [ ] Build a portfolio that proves your skills.
- [ ] Answer the common SOC interview questions well.

## Lessons

1. **The paths.** L1 to L2 to L3, and the specialisms (detection engineering, threat intel, DFIR, cloud, management).
2. **Certifications.** Which help at which stage, and why hands-on skill and a portfolio beat a wall of certificates.
3. **A portfolio.** A home lab, a few detections you wrote, a hunt you ran, a write-up of a case you worked. Proof beats claims.
4. **Interviewing.** Thinking out loud, saying "I am not sure, here is how I would find out", and showing judgement over memorised facts.

## Interview question bank

Try each before reading the model answer.

| Question | What they are testing |
|---|---|
| Walk me through triaging a phishing alert | Method, not trivia |
| How do you tell a true positive from a false positive? | Judgement |
| A login succeeded after many failures. What now? | Prioritisation and the key pivot |
| How would you tune a noisy rule without going blind? | Precision vs blind spots |
| What do you do first in a suspected ransomware case? | Calm under pressure |
| How do you keep learning? | Curiosity and self-direction |

??? note "Model answer: login succeeded after failures"
    Treat it as possible account compromise. Confirm the success is real and from the same source as the failures. Check what the account did after the login (new processes, connections, mailbox rules, further logins). If there is post-login activity, escalate and contain (reset, revoke sessions). Check whether MFA was in place and how it was bypassed. The point is the success-after-failure pivot and acting on it, not the failures.

??? note "Model answer: tune a noisy rule without going blind"
    Understand what is really causing the false positives first. Prefer tightening the logic (parent process, command pattern, outcome) over broad exclusions. If you must exclude, make it specific and documented with a review date. Re-test that the rule still catches the attack after tuning. The key idea: tune the logic to be precise, not the scope to be blind.

??? note "Model answer: keep learning"
    A home lab where I run attacks and build detections, reading incident write-ups and threat reports, practising on free platforms, and sharing what I learn. Concrete examples beat "I read a lot".

## Lab

- [ ] Write your own one-page skills plan: where you are, your next role, the gaps.
- [ ] Build or extend a home lab and document one thing you did in it.
- [ ] Prepare answers to the six questions above in your own words.
- [ ] Do a mock interview with a colleague.

## Self-check

1. Why does a portfolio beat a list of certifications?
2. What is a strong way to answer a question you do not know?

??? note "Answers"
    1. A portfolio proves you can actually do the work; certifications show you studied. Employers hire for demonstrated skill and judgement.
    2. Say so honestly and explain how you would find out: where you would look, what you would check. Showing method beats guessing.

## Links to the handbook and kit

- [Career paths](../../00-start-here/career-paths.md)
- [Field guide by role](../../field-guide/index.md)
- [Team and roles](../../01-build-a-soc/team-and-roles.md)

## Next module

[T16 Modern SOC Architecture](../t16-modern-soc/index.md).
