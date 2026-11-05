# T18: Securing AI Systems

As organisations deploy AI, the SOC has to defend it and detect attacks that use it. This module covers the new attack surface of AI systems and the AI-powered attacks you will start to see.

!!! abstract "At a glance"
    - Level: L2 to L3
    - Time: 6 to 8 hours
    - Outcome: you understand how AI systems are attacked and how to monitor and detect against them

## Learning objectives

- [ ] Explain the main attacks on AI and LLM systems.
- [ ] Use the OWASP Top 10 for LLM Applications and MITRE ATLAS.
- [ ] Monitor an LLM application for abuse.
- [ ] Detect AI-powered attacks such as deepfakes and AI-generated phishing.

## Lessons

1. **The new attack surface.** When your organisation runs an AI application, it becomes a target with its own weaknesses.
2. **Core attacks.** Prompt injection (making the model follow attacker instructions), data poisoning (corrupting training data), model theft, sensitive-data leakage, and insecure plugins or tools.
3. **Frameworks.** The OWASP Top 10 for LLM Applications and MITRE ATLAS (the ATT&CK equivalent for AI systems).
4. **Monitoring LLM applications.** Logging prompts and outputs, watching for injection attempts, data-leakage patterns, and abuse; treating the AI app like any other internet-facing application.
5. **AI-powered attacks.** Deepfake voice and video fraud, AI-generated phishing at scale, and how they change the threat; verification through known channels matters more than ever.

## Lab

- [ ] Take a simple LLM application (or a described one) and list its attack surface using the OWASP LLM Top 10.
- [ ] Craft a basic prompt-injection test against a lab chatbot and see if it follows injected instructions.
- [ ] Write what you would log from an LLM application to detect abuse.
- [ ] Write an awareness note for staff on deepfake and AI-phishing red flags.

## Self-check

1. What is prompt injection, and why is it dangerous?
2. What does MITRE ATLAS give you?
3. How does the rise of deepfakes change advice to staff?

??? note "Answers"
    1. Making a model follow attacker-supplied instructions hidden in its input (a page, a document, a message). It is dangerous because the model may then leak data, call tools, or act against its intended rules.
    2. A knowledge base of adversary tactics and techniques against AI and machine-learning systems, the AI equivalent of ATT&CK, for mapping and defending.
    3. Verification through a known, separate channel becomes essential: a convincing voice or video is no longer proof of identity. "Confirm by calling a known number" applies to voice and video too, not just email.

## Links to the handbook and kit

- [T17 AI-Driven SOC](../t17-ai-driven-soc/index.md)
- [Phishing playbook](../../04-playbooks/phishing.md)
- [Employee security guide](../../08-security-policies/employee-security-guide.md)

## You have reached the end of the training track

Go back to the [training index](../index.md) to review, or into the [field guide](../../field-guide/index.md) and [walkthroughs](../../field-guide/walkthroughs/index.md) to practise.
