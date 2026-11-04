# Writing Good Detections

Practical rules for logic, severity, naming and alert text. A good detection fires on the behaviour, carries enough context to triage without pivoting, and tells the analyst what to do next.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC analysts L2/L3
    - Time to read: 12 minutes
    - Outcome: you can write a rule, set its severity, name it and write an alert description that passes peer review

## Precision vs recall: pick deliberately

Precision = how many alerts are real. Recall = how many real attacks you catch. You cannot maximise both in one rule, so decide per rule.

| Rule purpose | Optimise for | Typical level | Example |
|---|---|---|---|
| Pages a human now | Precision | high / critical | Office app spawning PowerShell |
| Feeds a case for daily review | Balance | medium | PowerShell encoded command |
| Building block for correlation or hunting | Recall | low / informational | Any SSH password login accepted |

!!! tip
    If a rule needs high recall *and* pages people, split it: a low-level building block plus a high-level correlation on top.

## Behaviour beats indicators

Indicators of Compromise (IOCs) such as hashes, IP addresses and domains change in hours. Behaviours change slowly. Use IOCs for enrichment and retro-hunting; build alerts on behaviour.

| Weak (IOC) | Strong (behaviour) |
|---|---|
| Hash of a known stealer binary | Non-browser process reads `Login Data` / `logins.json` |
| One attacker IP in auth logs | Many failures then a success from the same source |
| Known phishing domain | Office application starts a script interpreter |

Same behaviour, three backends:

=== "Splunk SPL"
    ```spl
    index=edr sourcetype=sysmon EventCode=1
      ParentImage IN ("*\\WINWORD.EXE","*\\EXCEL.EXE","*\\POWERPNT.EXE","*\\OUTLOOK.EXE")
      Image IN ("*\\powershell.exe","*\\pwsh.exe","*\\cmd.exe","*\\wscript.exe","*\\cscript.exe","*\\mshta.exe")
    | table _time host User ParentImage Image CommandLine
    ```

=== "Microsoft KQL"
    ```kql
    DeviceProcessEvents
    | where InitiatingProcessFileName in~ ("winword.exe","excel.exe","powerpnt.exe","outlook.exe")
    | where FileName in~ ("powershell.exe","pwsh.exe","cmd.exe","wscript.exe","cscript.exe","mshta.exe")
    | project Timestamp, DeviceName, AccountName, InitiatingProcessFileName, FileName, ProcessCommandLine
    ```

=== "Wazuh rule XML"
    ```xml
    <group name="sysmon,office_child,">
      <rule id="100410" level="12">
        <if_sid>61603</if_sid>
        <field name="win.eventdata.parentImage" type="pcre2">(?i)\\(winword|excel|powerpnt|outlook)\.exe$</field>
        <field name="win.eventdata.image" type="pcre2">(?i)\\(powershell|pwsh|cmd|wscript|cscript|mshta)\.exe$</field>
        <description>Office application started $(win.eventdata.image) on $(win.system.computer)</description>
        <mitre><id>T1566.001</id><id>T1059</id></mitre>
      </rule>
    </group>
    ```

## Context fields every alert must carry

If the analyst has to run a second query to answer "who, where, what", the rule is incomplete.

| Question | Field examples |
|---|---|
| Who | user, account SID / ARN, source user for cloud |
| Where | host name, host IP, cloud account / tenant, region |
| What | process + command line, parent process, URL path, operation name |
| From where | source IP, geolocation, user agent |
| How much | count, first seen, last seen (for threshold rules) |
| So what | asset criticality, user is privileged (via lookup/enrichment) |

In Sigma, list them under `fields:`. In the SIEM, add them to the alert output (`table` in SPL, `project` in KQL).

## Severity matrix

Set severity from **confidence** that it is malicious and **impact** if it is.

| Confidence \ Impact | Low impact (single workstation) | Medium (server, normal user) | High (domain admin, prod cloud, payment system) |
|---|---|---|---|
| Low (often benign) | informational | low | medium |
| Medium | low | medium | high |
| High (rarely benign) | medium | high | critical |

Rules:

- The Sigma `level` is the default. Enrichment may raise it (privileged user, crown-jewel asset) but should never silently lower a `high`.
- `critical` requires SOC manager approval and a paging playbook.

## Naming standard

**Sigma file name:** `<platform_or_source>_<behaviour>.yml`, lowercase, underscores. Example: `linux_root_ssh_login.yml`.

**Alert title (what the analyst sees):** `<Behaviour> - <object>` in plain English, no jargon, no internal IDs.

| Bad | Good |
|---|---|
| `RULE_0451_PS_ENC` | PowerShell started with a Base64 encoded command |
| `Suspicious activity detected` | Office application launching a script interpreter or shell |
| `Brute force` | SSH password login accepted after repeated failures |

**SIEM search name:** `DET-<id> | <title> | <level>` so lists sort and filter cleanly.

## Alert description standard: What / Where / Why it matters / What to do

Every alert carries four short blocks. Template:

```text
WHAT:   <one sentence, the observed behaviour, with values filled from fields>
WHERE:  host=<host> user=<user> src=<source_ip> time=<UTC timestamp>
WHY IT MATTERS: <one or two sentences on the attacker goal and the risk>
WHAT TO DO:
  1. <first triage step>
  2. <decision point: benign if ..., escalate if ...>
  3. Playbook: <link>
```

Filled example:

```text
WHAT:   A new inbox rule on finance.user@example.com forwards all mail to an address outside the organisation.
WHERE:  user=finance.user@example.com client_ip=203.0.113.45 time=2026-10-27T08:14:02Z
WHY IT MATTERS: Attackers add forwarding rules after taking over a mailbox so they keep reading mail after a password reset. Finance mailboxes are a common invoice-fraud target.
WHAT TO DO:
  1. Check whether 203.0.113.45 matches the user's normal sign-in locations.
  2. Ask the user (out of band, by phone) whether they created the rule. If not, treat as compromise.
  3. Playbook: Business email compromise.
```

## Anti-patterns

| Anti-pattern | Why it hurts | Do this instead |
|---|---|---|
| `CommandLine contains "mimikatz"` only | Renamed in seconds | Detect the behaviour (LSASS memory access) |
| Filter on user name only (`not User=svc_backup`) | Attacker uses that account | Filter on user **and** host **and** parent process |
| Wildcard at both ends on large fields | Slow, noisy | Use `endswith` / exact field match |
| Threshold set without baseline | Either silent or flooding | Measure 30-day distribution, set at p99 |
| One giant rule for many behaviours | Cannot tune one part | One behaviour per rule |
| Alert text says "investigate" | Analyst does not know how | Use What/Where/Why/What-to-do |
| Severity high "just in case" | Alert fatigue | Use the severity matrix |
| Testing only in production | Breaks silently on parser change | Unit tests in CI |

!!! warning "Common mistakes"
    - Case sensitivity: Windows paths vary in case. Use case-insensitive matching (Sigma is case-insensitive by default; `in~` in KQL; `(?i)` in regex).
    - Time zones: always show UTC in the alert, and the local time only as an extra field.
    - Exclusions that never expire: every exception file entry needs an owner and a review date.

## Peer review checklist

- [ ] One behaviour, one rule
- [ ] Logic matches behaviour, not a single tool name
- [ ] Fields list answers who / where / what / from where
- [ ] Severity follows the matrix
- [ ] Title and file name follow the naming standard
- [ ] Description follows What / Where / Why / What to do
- [ ] False positives listed and realistic
- [ ] Positive and negative tests exist
- [ ] Playbook link present

## Related pages

- [Sigma primer](sigma-primer.md)
- [Testing and tuning](testing-and-tuning.md)
- [Alert tuning](../02-daily-operations/alert-tuning.md)
- [Alert fatigue and notifications](../07-automation-soar/alert-fatigue-and-notifications.md)
