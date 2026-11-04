# Detection Engineering

How to turn an attacker behaviour into a tested, owned, version-controlled alert that analysts trust. Start here, then follow the pages in order.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC analysts L2/L3, SOC leads
    - Time to read: 5 minutes
    - Outcome: you know where every detection page and every Sigma rule in this handbook lives, and which playbook each rule feeds

## Pages in this section

| Page | Use it when you need to |
|---|---|
| [Detection lifecycle](detection-lifecycle.md) | Take an idea from request to production, and later retire it, using git and a CI pipeline |
| [Writing good detections](writing-good-detections.md) | Decide logic, severity, naming and the alert text an analyst will read at 03:00 |
| [Sigma primer](sigma-primer.md) | Write a Sigma rule and convert it to Splunk, Elastic/OpenSearch, Microsoft Sentinel or Wazuh |
| [Testing and tuning](testing-and-tuning.md) | Prove a rule fires, prove it stays quiet on normal traffic, and record every tuning change |
| [Coverage mapping](coverage-mapping.md) | Map rules to MITRE ATT&CK, build a heatmap and choose the next gap to close |

## Sigma rule library

All rules are original, written for this handbook, `status: experimental` and vendor-neutral. Treat them as a starting point: run them in your environment for at least two weeks in "log only" mode before they page anyone.

| File | Title | ATT&CK | Level | Related playbook |
|---|---|---|---|---|
| [web_secret_file_probe.yml](rules/sigma/web_secret_file_probe.yml) | Web request for sensitive configuration or repository files | T1595.003, T1552.001 | medium | [Web application attack](../04-playbooks/web-application-attack.md) |
| [ssh_successful_login_after_failures.yml](rules/sigma/ssh_successful_login_after_failures.yml) | SSH password login accepted (brute-force success candidate) | T1110.001, T1078 | low (high with threshold) | [Brute force](../04-playbooks/brute-force.md) |
| [windows_new_local_admin_user.yml](rules/sigma/windows_new_local_admin_user.yml) | Local account created or added to Administrators | T1136.001, T1098 | medium | [Account compromise](../04-playbooks/account-compromise.md) |
| [powershell_encoded_command.yml](rules/sigma/powershell_encoded_command.yml) | PowerShell started with an encoded command | T1059.001, T1027 | medium | [Malware / infostealer](../04-playbooks/malware-infostealer.md) |
| [office_spawning_script_interpreter.yml](rules/sigma/office_spawning_script_interpreter.yml) | Office application launching a script interpreter or shell | T1566.001, T1204.002, T1059 | high | [Phishing](../04-playbooks/phishing.md) |
| [browser_credential_store_access_by_unusual_process.yml](rules/sigma/browser_credential_store_access_by_unusual_process.yml) | Browser saved-password store read by a non-browser process | T1555.003 | medium | [Malware / infostealer](../04-playbooks/malware-infostealer.md) |
| [mailbox_forwarding_rule_external.yml](rules/sigma/mailbox_forwarding_rule_external.yml) | Mailbox rule forwards mail to an external address | T1114.003, T1564.008 | high | [Business email compromise](../04-playbooks/business-email-compromise.md) |
| [cloud_console_login_without_mfa.yml](rules/sigma/cloud_console_login_without_mfa.yml) | Cloud console login succeeded without MFA | T1078.004 | medium | [Cloud account compromise](../04-playbooks/cloud-account-compromise.md) |
| [linux_root_ssh_login.yml](rules/sigma/linux_root_ssh_login.yml) | Direct SSH login as root accepted | T1078.003, T1021.004 | high | [Account compromise](../04-playbooks/account-compromise.md) |
| [dns_query_to_known_paste_or_file_sharing_from_server.yml](rules/sigma/dns_query_to_known_paste_or_file_sharing_from_server.yml) | Server resolving a paste or anonymous file-sharing service | T1105, T1102, T1567.002 | medium | [Malware / infostealer](../04-playbooks/malware-infostealer.md) |

## Quick start: from zero to first deployed rule

1. Clone the handbook repository and copy `docs/05-detection-engineering/rules/sigma/` into your own detection repo.
2. Install the converter:
    ```bash
    python -m pip install sigma-cli
    sigma plugin install splunk elasticsearch microsoft365defender
    ```
3. Check the rules are valid:
    ```bash
    sigma check rules/sigma/
    ```
4. Convert one rule for your SIEM (Security Information and Event Management):
    ```bash
    sigma convert -t splunk -p sysmon rules/sigma/office_spawning_script_interpreter.yml
    ```
5. Paste the output into your SIEM as a scheduled search with **no notification**, run it for 14 days, then follow [Testing and tuning](testing-and-tuning.md).
6. Record the rule in your coverage sheet ([Coverage mapping](coverage-mapping.md)).

!!! warning "Common mistakes"
    - Deploying all ten rules straight to paging. Start them silent and measure volume first.
    - Forgetting placeholders. `example.com` in the mailbox rule and the `10.10.0.0/16` ranges in the DNS rule must be replaced.
    - Assuming the data exists. The browser credential rule needs file-access telemetry from an Endpoint Detection and Response (EDR) agent or object auditing.

## Checklist before a rule leaves this library

- [ ] Placeholders replaced with your domains and network ranges
- [ ] Log source confirmed present in the SIEM (see [Detection lifecycle](detection-lifecycle.md), data check step)
- [ ] Positive test passed and negative test passed
- [ ] Owner, playbook link and severity agreed
- [ ] Added to the ATT&CK coverage sheet

## Related pages

- [Use case prioritisation](../01-build-a-soc/use-case-prioritization.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
- [Automation and SOAR](../07-automation-soar/index.md)
