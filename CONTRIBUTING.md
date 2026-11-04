# Contributing

Thank you for helping make The Defensive Mind more useful. Practical knowledge from real SOC work is the most valuable contribution.

## What helps most

- A query for another platform (Splunk SPL, Microsoft KQL, Elastic/OpenSearch, Wazuh, Chronicle, QRadar ...)
- A correction: a wrong technique ID, a broken link, an outdated tool name
- A real-world tip or "common mistake" from your own shifts (anonymised)
- A new playbook, case walkthrough, Sigma rule or template

## Ground rules

1. **Write in your own words.** Do not paste text from books, courses, vendor documentation or other repositories. Link to the source instead.
2. **No confidential data.** No real company names, hostnames, IP addresses, user names, customer data or incident details. Use `ACME`, `example.com`, `203.0.113.0/24`.
3. **Practical first.** Follow the [style guide](STYLE_GUIDE.md): short intro, then steps, queries, examples and checklists.
4. **One topic per pull request**, with a short description of what changed and why.

## How to contribute

1. Fork the repository and create a branch: `git checkout -b add-kql-brute-force`
2. Make your change in `docs/`. Preview it locally:
   ```bash
   pip install -r requirements-docs.txt
   mkdocs serve
   ```
3. Run `mkdocs build --strict`, it must finish without warnings (it catches broken links).
4. Open a pull request.

## New playbook or rule

- Playbooks: copy [docs/04-playbooks/playbook-template.md](docs/04-playbooks/playbook-template.md) and keep every heading.
- Sigma rules: put them in `docs/05-detection-engineering/rules/sigma/`, use a new UUID, `status: experimental` until tested, and add the rule to the table in the detection engineering index.

## License of contributions

By contributing you agree that documentation is published under [CC BY 4.0](LICENSE) and code/rules under [MIT](LICENSE-CODE).
