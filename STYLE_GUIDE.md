# Writing Style Guide

Every page in The Defensive Mind follows the same rules, so the handbook reads as one voice.

## Principles

1. **Universal.** Write for any organisation, any size, any sector. No company names, no internal hostnames, no customer data. Use neutral examples (`ACME`, `example.com`, `10.0.0.0/8`, `203.0.113.0/24`).
2. **Vendor-agnostic.** Describe the capability first ("a SIEM", "an EDR"). Name products only as examples, and always include at least one open-source option.
3. **Practical first, theory last.** Written for working analysts (L1-L3) and SOC managers. Intros are three lines at most. Every page answers *what do I do, how, and with which tool*: step-by-step procedures, real queries (Splunk SPL, Microsoft KQL, Elastic/OpenSearch, IBM QRadar AQL, Wazuh), sample log lines, commands, filled-in examples, checklists and "common mistakes".
4. **Original.** Write in your own words. Do not copy text from other projects, books or vendor documentation. Link to sources instead.
5. **Plain English.** Short sentences. Active voice. Expand every abbreviation the first time it appears on a page, e.g. "Endpoint Detection and Response (EDR)".

## Page layout

```markdown
# Page Title

One or two sentences: what this page is for and who should read it.

!!! abstract "At a glance"
    - Audience: SOC analyst / SOC lead / manager
    - Time to read: N minutes
    - Outcome: what the reader can do after reading

## Sections ...

## Checklist            (where useful)

## Related pages        (relative links to other pages)
```

## Formatting

- Headings: `#` once per page, then `##` and `###`. No numbering in headings.
- Use tables for comparisons, decision matrices and RACI.
- Use MkDocs Material admonitions: `!!! tip`, `!!! warning`, `!!! danger`, `!!! example`, `!!! note`.
- Use task lists for checklists: `- [ ] item`.
- Code and queries in fenced blocks with a language (`yaml`, `bash`, `kql`, `spl`, `sql`).
- Plain punctuation only: no em or en dashes, arrows, middle dots or typed bullet symbols. Use commas, colons, hyphens and `->` in code.
- File names: lowercase-with-hyphens.md.
- Links: relative (`../03-incident-response/ir-lifecycle.md`).

## Playbooks

Use [docs/04-playbooks/playbook-template.md](docs/04-playbooks/playbook-template.md) exactly. Every playbook maps to MITRE ATT&CK techniques and the NIST incident response phases.

## Detection rules

Sigma rules live in `docs/05-detection-engineering/rules/sigma/`. Each rule has a unique UUID, `status`, `level`, ATT&CK tags, `falsepositives` and a short description written by us.
