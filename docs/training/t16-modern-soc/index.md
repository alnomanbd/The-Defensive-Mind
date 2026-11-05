# T16: Modern SOC Architecture

Where the SOC is heading: the architectures and practices that define a modern operation, beyond a classic SIEM and a queue. This module is a map of the modern landscape so you can place each piece and decide what fits you.

!!! abstract "At a glance"
    - Level: L2 to lead
    - Time: 6 to 8 hours
    - Outcome: you understand modern SOC building blocks and when each matters

## Learning objectives

- [ ] Explain XDR, cloud-native SIEM, and security data lakes and pipelines.
- [ ] Understand detection as code and risk-based alerting.
- [ ] Explain identity and cloud detection and response (ITDR, CDR, CNAPP).
- [ ] Understand SaaS security, deception, breach and attack simulation, and continuous threat exposure management.
- [ ] Place OT and IoT monitoring and MDR models.

## Lessons

1. **Data architecture.** Cloud-native SIEM, security data lakes, and data pipelines with a common schema (OCSF) to control cost and avoid lock-in.
2. **Detection as code.** Detections versioned, tested and deployed through CI, treated like software.
3. **Risk-based alerting (RBA).** Scoring risk across many weak signals instead of paging on each, to cut noise.
4. **Identity and cloud.** ITDR (identity threat detection and response), CDR and CNAPP (cloud detection and posture), because identity and cloud are where attacks now live.
5. **SaaS and exposure.** SSPM (SaaS security posture), deception (honeytokens), breach and attack simulation (BAS), and CTEM (continuous threat exposure management).
6. **Edges.** OT and IoT monitoring, and the MDR models for buying coverage and depth.

## Lab

- [ ] Draw your current (or a fictional) SOC architecture and mark where each modern piece would fit.
- [ ] Pick one concept (for example risk-based alerting) and write how it would cut noise in your environment.
- [ ] Plant a honeytoken in your lab (a fake credential or file) and alert when it is touched.
- [ ] Map one BAS test to a detection you would expect to fire.

## Self-check

1. What problem does a security data lake with a common schema solve?
2. What is risk-based alerting trying to fix?
3. Why have ITDR and cloud detection become their own categories?

??? note "Answers"
    1. The cost and lock-in of pushing every log into an expensive SIEM; a lake with an open schema lets you store cheaply and keep detection portable.
    2. Alert fatigue: instead of paging on each weak signal, it scores risk across many signals and alerts when the combined risk is high.
    3. Because attacks increasingly use valid identities and cloud APIs rather than malware, so detecting identity and cloud abuse needs dedicated focus.

## Links to the handbook and kit

- [Technology stack](../../01-build-a-soc/technology-stack.md)
- [Detection engineering](../../05-detection-engineering/index.md)
- [Cloud account compromise playbook](../../04-playbooks/cloud-account-compromise.md)

## Next module

[T17 AI-Driven SOC](../t17-ai-driven-soc/index.md).
