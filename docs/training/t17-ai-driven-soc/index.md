# T17: AI-Driven SOC

Where artificial intelligence genuinely helps a SOC, where it fails, and how to use it safely. This module separates the hype from the useful, and shows how to add AI to the SOC with a human kept in control.

!!! abstract "At a glance"
    - Level: L2 to lead
    - Time: 6 to 8 hours with labs
    - Outcome: you can use AI to speed up SOC work without trusting it blindly

!!! warning "AI assists, it does not decide"
    AI in a SOC is a fast assistant, not an analyst. It can enrich, summarise, draft and suggest; it can also be confidently wrong, be manipulated, and leak data. Keep a human in control of every decision and every action that matters. Treat AI output as a lead to verify, not a verdict.

## Learning objectives

- [ ] Explain where AI helps in a SOC and where it fails.
- [ ] Use an LLM copilot for enrichment, summarising and query drafting.
- [ ] Understand AI triage agents and natural-language-to-query.
- [ ] Understand machine-learning anomaly detection and its false positives.
- [ ] Build an AI triage workflow with a human approval step.
- [ ] Measure AI accuracy and set guardrails and privacy controls.

## Lessons

1. **Where AI helps.** Summarising long alerts and cases, drafting queries from plain language, enriching, drafting reports, suggesting next steps.
2. **Where AI fails.** It hallucinates, it can be prompt-injected, it can leak data, and it has no accountability. Never let it act unchecked.
3. **LLM copilots.** Using an assistant to speed up the analyst, with the analyst verifying.
4. **AI triage agents.** Automating first-pass triage with an agent, always behind human approval for action.
5. **Machine learning anomaly detection.** Useful for finding the unusual, noisy on its own; a signal to investigate, not an alert to trust.
6. **Agentic workflows.** Chaining AI steps (enrich, summarise, recommend) with a human approving any action.
7. **Guardrails.** Measuring accuracy, limiting what AI can touch, protecting data privacy, and logging what it did.

## Lab

- [ ] Take a long alert or case and have an AI assistant summarise it; check the summary for errors.
- [ ] Ask an assistant to draft a SIEM query from a plain-language question; test and correct it.
- [ ] Sketch an AI triage workflow: enrich, summarise, recommend, then human approval before any action.
- [ ] Write the guardrails: what the AI may read, what it may never do, how its output is checked.

## Self-check

1. Name two things AI is good at in a SOC and two ways it fails.
2. Why keep a human approval step in an AI triage workflow?
3. Why is AI output a lead, not a verdict?

??? note "Answers"
    1. Good at: summarising, drafting queries, enriching, drafting reports. Fails by: hallucinating, being prompt-injected, leaking data, and having no accountability.
    2. Because AI can be confidently wrong or manipulated; a human must approve any business-affecting action so a bad suggestion does not become a bad action at machine speed.
    3. Because it can be wrong or manipulated and cannot be held accountable; every AI conclusion must be verified against the evidence before you act on it.

## Links to the handbook and kit

- [Automation and SOAR](../../07-automation-soar/index.md)
- [SOAR principles](../../07-automation-soar/soar-principles.md)
- [T18 Securing AI Systems](../t18-securing-ai/index.md)

## Next module

[T18 Securing AI Systems](../t18-securing-ai/index.md).
