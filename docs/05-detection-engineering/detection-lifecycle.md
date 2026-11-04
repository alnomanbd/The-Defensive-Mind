# Detection Lifecycle

A repeatable path for every rule: idea, requirement, data check, write, test, deploy, tune, retire. Each stage has a clear exit gate so nothing reaches analysts untested or unowned.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC analysts L2/L3, SOC managers
    - Time to read: 10 minutes
    - Outcome: you can run a detection request end to end with git, a CI (Continuous Integration) pipeline and named owners

## The stages and their exit gates

| Stage | What you do | Exit gate (must be true to move on) | Owner |
|---|---|---|---|
| 1. Idea | Capture the request: incident lesson, threat report, red team finding, audit gap | Ticket exists with source and example | Anyone |
| 2. Requirement | Write the detection requirement (template below) | ATT&CK technique, scope and expected volume agreed | Detection engineer |
| 3. Data check | Prove the log source and fields exist and are parsed | Query returns real events with the needed fields | Detection engineer + platform team |
| 4. Write | Write Sigma (or native) rule in a branch | `sigma check` passes, peer review requested | Detection engineer |
| 5. Test | Positive test (fires), negative test (quiet on normal data) | Both tests pass in CI and in the SIEM | Detection engineer |
| 6. Deploy | Merge, CI converts and pushes; run silent for 14 days | Daily volume and false-positive (FP) rate measured | Detection engineer |
| 7. Tune | Add filters, adjust threshold, then enable notifications | FP rate below target, playbook linked | Detection engineer + L2 |
| 8. Retire | Disable and archive when no longer useful | Retirement reason recorded, coverage sheet updated | Rule owner |

## Stage 1-2: the requirement template

Copy this into the ticket. If a field cannot be filled, the idea is not ready.

```yaml
request_id: DET-0142
title: Mailbox forwarding to external address
source: incident IR-2026-031 lesson learned
attack: [T1114.003]
threat_scenario: >
  Attacker with stolen mailbox password adds rule forwarding all mail
  to a free webmail address to keep access after password reset.
log_source: hosted mail audit log (Operation, Parameters, UserId, ClientIP)
scope: all user and shared mailboxes
expected_volume: < 5 per week
severity_proposed: high
response: ../04-playbooks/business-email-compromise.md
owner: detection-team
```

## Stage 3: data check

Never write logic against fields you have not seen. Run a 24-hour query and look at five real events.

=== "Splunk SPL"
    ```spl
    index=mail sourcetype=*audit* Operation IN ("New-InboxRule","Set-InboxRule")
    | head 5
    | table _time UserId Operation Parameters ClientIP
    ```

=== "Microsoft KQL"
    ```kql
    OfficeActivity
    | where TimeGenerated > ago(1d)
    | where Operation in ("New-InboxRule", "Set-InboxRule")
    | take 5
    | project TimeGenerated, UserId, Operation, Parameters, ClientIP
    ```

=== "Elastic / OpenSearch (KQL bar)"
    ```text
    event.action : ("New-InboxRule" or "Set-InboxRule")
    ```

Data check record (paste into the ticket):

- [ ] Index / table name confirmed
- [ ] Event arrives within ___ minutes of real time (ingest delay)
- [ ] Every field used by the rule is populated and parsed (not inside a raw blob)
- [ ] Retention covers the look-back window of the rule
- [ ] Source covers the full scope (all hosts / all tenants), not a pilot group

!!! danger "Common mistake"
    The field exists in one parser version but not another. Check counts per host or per collector: `| stats count by host` (SPL) or `| summarize count() by Computer` (KQL). A source with zero events is a blind spot, not a quiet network.

## Stage 4: detection-as-code repository

```text
detections/
  rules/sigma/                  # one rule per file, snake_case.yml
  rules/native/splunk/          # only when Sigma cannot express it
  tests/
    <rule_name>/
      positive.jsonl            # events that MUST match
      negative.jsonl            # events that MUST NOT match
  pipelines/                    # pySigma field-mapping pipelines
  exceptions/                   # reviewed allow-lists, one file per rule
  CODEOWNERS
  .ci/pipeline.yml
```

Branch and review rules:

1. One rule or one tuning change per pull request.
2. Pull request title: `DET-0142 add mailbox_forwarding_rule_external`.
3. At least one reviewer who is not the author; for `high`/`critical` rules, one L2/L3 analyst reviews the alert text.
4. `CODEOWNERS` maps each folder to an owning team so reviews route automatically.

## Stage 5-6: the CI pipeline

Generic pipeline steps. Adapt to GitHub Actions, GitLab CI, Jenkins or any runner.

```yaml
stages: [lint, test, convert, deploy]

lint:
  script:
    - pip install sigma-cli yamllint
    - yamllint -d relaxed rules/
    - sigma check rules/sigma/
    - python .ci/check_metadata.py rules/sigma/   # id unique, owner, level, tags present

test:
  script:
    - python .ci/run_rule_tests.py rules/sigma/ tests/   # see testing-and-tuning.md

convert:
  script:
    - sigma plugin install splunk
    - mkdir -p out/splunk
    - for f in rules/sigma/*.yml; do
        sigma convert -t splunk -p sysmon "$f" > "out/splunk/$(basename "$f" .yml).spl";
      done
  artifacts: [out/]

deploy:
  when: branch == main
  script:
    - python .ci/push_to_siem.py out/ --mode silent   # creates/updates saved searches via API
```

`check_metadata.py` should fail the build when:

- [ ] `id` is missing, not a UUID, or reused by another file
- [ ] `level`, `status`, `author`, `date`, `falsepositives` or `tags` is missing
- [ ] no `attack.tXXXX` tag exists
- [ ] `level` is `high` or `critical` and no playbook link is in the description or a `related_playbook` custom field

## Stage 7: promote from silent to live

Move a rule from `silent` to `live` only after 14 days of data and this check:

| Metric | Target to go live |
|---|---|
| Alerts per day | Within the volume agreed in the requirement |
| False-positive rate (FP / total reviewed) | < 30% for medium, < 10% for high/critical |
| Analyst can triage from alert text alone | Yes, verified by one L1 |
| Playbook linked | Yes |

Then change `status: experimental` to `status: test`, and after 90 days stable to `status: stable`.

## Stage 8: retirement

Retire a rule when any of these is true:

- The log source was decommissioned.
- A better rule covers the same behaviour with higher precision.
- The rule produced only false positives for 180 days and tuning failed.
- The attacked technology no longer exists in the estate.

Steps:

1. Set `status: deprecated` and add a line to the description: `Retired 2026-12-01: replaced by <id>.`
2. Disable the SIEM search; do not delete it for 30 days.
3. Update the coverage sheet so the ATT&CK cell does not overstate coverage.
4. Close the ticket with the reason.

## Ownership model

| Role | Responsible for |
|---|---|
| Rule owner (named person or team) | Quarterly review, tuning requests, retirement decision |
| Detection engineer | Writing, testing, CI, conversion |
| L1/L2 analyst | Feedback on every closed alert (true positive / false positive / benign true positive) |
| Platform team | Log source health and parser changes |
| SOC manager | Approves `critical` level and paging rules |

!!! tip "Quarterly rule review in one hour"
    Export last-90-day stats per rule: alert count, FP rate, mean time to triage. Sort by FP count. Fix the top five, retire anything with zero alerts and no test run in 90 days.

## Checklist

- [ ] Requirement ticket complete
- [ ] Data check recorded with real sample events
- [ ] Rule in git, reviewed, CI green
- [ ] Positive and negative tests in `tests/`
- [ ] Deployed silent, 14-day stats reviewed
- [ ] Promoted live with playbook and owner
- [ ] Review date in calendar

## Related pages

- [Writing good detections](writing-good-detections.md)
- [Testing and tuning](testing-and-tuning.md)
- [Coverage mapping](coverage-mapping.md)
- [Use case prioritisation](../01-build-a-soc/use-case-prioritization.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
