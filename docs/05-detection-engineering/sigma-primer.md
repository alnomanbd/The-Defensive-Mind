# Sigma Primer

Sigma is a vendor-neutral YAML format for log detections: write the rule once, convert it to your SIEM's query language with a tool. This page is the hands-on minimum to write, check and convert rules.

!!! abstract "At a glance"
    - Audience: detection engineers, SOC analysts L2/L3
    - Time to read: 15 minutes (plus 20 minutes lab)
    - Outcome: you can read any Sigma rule, write your own, and convert it to Splunk SPL, Elastic/OpenSearch, Microsoft KQL and a Wazuh rule

## Anatomy of a rule (annotated)

```yaml
title: PowerShell Started with a Base64 Encoded Command   # what the analyst sees
id: 7316cce5-80e4-4377-8e98-4e3a2cb19435               # random UUID v4, never reused
status: experimental        # experimental -> test -> stable -> deprecated
description: |              # what / why it matters / how to triage
    Detects PowerShell launched with the encoded command switch ...
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: The Defensive Mind
date: 2026-10-27            # created; add "modified:" when you change logic
tags:                       # ATT&CK tactic + technique, lowercase
    - attack.execution
    - attack.t1059.001
logsource:                  # WHICH logs - mapped to indexes/tables by a pipeline
    category: process_creation
    product: windows
detection:                  # WHAT to match
    selection_image:        # list of maps = OR between the maps
        - Image|endswith:
              - '\powershell.exe'
              - '\pwsh.exe'
        - OriginalFileName: 'PowerShell.EXE'
    selection_switch:       # values in a list = OR; keys in one map = AND
        CommandLine|contains|windash:
            - ' -enc '
            - ' -ec '
    condition: all of selection_*   # boolean logic over the named blocks
fields:                     # context to show in the alert
    - ParentImage
    - CommandLine
falsepositives:             # honest list, drives tuning
    - Software deployment agents
level: medium               # informational | low | medium | high | critical
```

Matching rules to remember:

| Construct | Meaning |
|---|---|
| Keys inside one map | AND |
| Items in a list of values | OR |
| List of maps | OR between maps |
| Strings | Case-insensitive, exact match unless a modifier or `*` wildcard is used |
| `keywords:` (list of plain strings) | Full-text search in the raw message (use for syslog-style sources) |

## Logsource taxonomy

`logsource` describes the data, not the product. A pipeline maps it to your index or table.

| Field | Typical values | Example use |
|---|---|---|
| `category` | `process_creation`, `file_access`, `file_event`, `network_connection`, `dns`, `webserver`, `proxy`, `registry_set`, `image_load` | Endpoint and network behaviours that many tools produce |
| `product` | `windows`, `linux`, `macos`, `aws`, `azure`, `gcp`, `m365`, `okta` | Platform |
| `service` | `security`, `system`, `sysmon`, `auth`, `sshd`, `cloudtrail`, `exchange`, `audit` | Specific log channel of the product |

Examples from this handbook: `category: webserver`; `product: linux, service: auth`; `product: windows, service: security`; `product: aws, service: cloudtrail`.

## Modifiers you will use daily

| Modifier | Meaning | Example |
|---|---|---|
| `contains` | Substring | `CommandLine|contains: 'Invoke-WebRequest'` |
| `startswith` / `endswith` | Prefix / suffix | `Image|endswith: '\cmd.exe'` |
| `all` | All list values must match (AND) | `CommandLine|contains|all: ['-nop', '-w hidden']` |
| `re` | Regular expression | `query|re: '^[a-z0-9]{30,}\.'` |
| `cidr` | IP in network range | `src_ip|cidr: '10.10.0.0/16'` |
| `windash` | Also match `/`, en-dash and em-dash variants of `-` | `CommandLine|contains|windash: ' -enc '` |
| `base64offset` | Match a string inside Base64 at any alignment | `CommandLine|base64offset|contains: 'IEX'` |
| `exists` | Field is present or absent | `ParentImage|exists: false` |
| `fieldref` | Compare two fields | `TargetUserName|fieldref: SubjectUserName` |

Conditions: `selection and not filter`, `1 of selection_*`, `all of selection_*`, `1 of them`, brackets for grouping.

## Lab: write, check and convert (20 minutes)

### Step 1, install

```bash
python -m venv sigma-venv && source sigma-venv/bin/activate   # Windows: sigma-venv\Scripts\activate
pip install sigma-cli
sigma plugin list                 # shows available backends and pipelines
sigma plugin install splunk
sigma plugin install elasticsearch
sigma plugin install opensearch
sigma plugin install kusto        # Microsoft Defender XDR / Sentinel (older versions: microsoft365defender)
sigma list targets                # confirm target names for your installed versions
```

### Step 2, validate

```bash
sigma check rules/sigma/
```

Fix every error and every warning about missing tags or duplicate IDs before converting.

### Step 3, convert

```bash
# Splunk SPL, with Sysmon field mapping
sigma convert -t splunk -p sysmon rules/sigma/powershell_encoded_command.yml

# Elastic Lucene query with ECS (Elastic Common Schema) mapping for Windows
sigma convert -t lucene -p ecs_windows rules/sigma/powershell_encoded_command.yml

# Elastic EQL / ES|QL (newer elasticsearch plugin)
sigma convert -t eql -p ecs_windows rules/sigma/powershell_encoded_command.yml

# OpenSearch
sigma convert -t opensearch_lucene -p ecs_windows rules/sigma/powershell_encoded_command.yml

# Microsoft KQL for Defender XDR advanced hunting
sigma convert -t kusto -p microsoft_xdr rules/sigma/powershell_encoded_command.yml
```

Expected output shapes (abbreviated):

=== "Splunk SPL"
    ```spl
    (Image IN ("*\\powershell.exe", "*\\pwsh.exe") OR OriginalFileName IN ("PowerShell.EXE", "pwsh.dll"))
    (CommandLine IN ("* -e *", "* /e *", "* -en *", "* /en *", "* -enc *", "* /enc *", ...))
    ```

=== "Microsoft KQL"
    ```kql
    DeviceProcessEvents
    | where (FolderPath endswith @"\powershell.exe" or FolderPath endswith @"\pwsh.exe"
             or ProcessVersionInfoOriginalFileName in~ ("PowerShell.EXE", "pwsh.dll"))
      and (ProcessCommandLine contains " -e " or ProcessCommandLine contains " /e "
           or ProcessCommandLine contains " -enc " or ProcessCommandLine contains " /enc " ...)
    ```

=== "Elastic Lucene"
    ```text
    (process.executable:(*\\powershell.exe OR *\\pwsh.exe) OR process.pe.original_file_name:("PowerShell.EXE" OR "pwsh.dll"))
    AND process.command_line:(*\ \-e\ * OR *\ \/e\ * OR *\ \-enc\ * ...)
    ```

### Step 4, Wazuh (manual translation)

There is no maintained official pySigma backend for Wazuh, so translate by hand. Map each Sigma block to a `<field>` match on the decoded event and chain to the parent rule for that log source with `<if_sid>` or `<if_group>`.

```xml
<group name="sysmon,powershell,">
  <!-- Sigma id 7316cce5-80e4-4377-8e98-4e3a2cb19435 -->
  <rule id="100420" level="8">
    <if_sid>61603</if_sid>   <!-- Sysmon event 1 parent rule in the default ruleset -->
    <field name="win.eventdata.image" type="pcre2">(?i)\\(powershell|pwsh)\.exe$</field>
    <field name="win.eventdata.commandLine" type="pcre2">(?i)\s[-/\x{2013}\x{2014}](e|en|enc|enco\w*|ec)\s</field>
    <description>PowerShell started with an encoded command on $(win.system.computer)</description>
    <mitre><id>T1059.001</id><id>T1027</id></mitre>
  </rule>
</group>
```

Test it on the manager:

```bash
/var/ossec/bin/wazuh-logtest     # paste a sample JSON event, confirm rule 100420 fires
```

Level mapping used in this handbook: Sigma `low` = Wazuh 5-6, `medium` = 7-9, `high` = 10-12, `critical` = 13-15.

## Pipelines: making field names match

Converters only know your field names if a pipeline tells them. When your SIEM uses custom names, write a small pipeline file:

```yaml
name: acme-field-mapping
priority: 100
transformations:
  - id: map_process_fields
    type: field_name_mapping
    mapping:
      CommandLine: proc.cmdline
      Image: proc.path
      ParentImage: proc.parent_path
  - id: index_for_windows
    type: add_condition
    conditions:
      index: edr_windows
    rule_conditions:
      - type: logsource
        product: windows
```

```bash
sigma convert -t splunk -p acme-field-mapping.yml rules/sigma/office_spawning_script_interpreter.yml
```

## Testing a converted rule

1. Convert the rule.
2. Run the query over 30 days in the SIEM with no alerting. Record hit count.
3. Replay a positive sample (see [Testing and tuning](testing-and-tuning.md)) and confirm one hit.
4. Compare the converted query with the Sigma intent: wildcards placed correctly, `not` filters present, case-insensitivity kept.

!!! warning "Common mistakes"
    - Backslashes: Sigma `'\cmd.exe'` becomes `\\cmd.exe` in SPL and Lucene. Never "fix" this by hand in the YAML.
    - Missing pipeline: converting without `-p` produces generic field names that match nothing. Zero hits is not proof of zero activity.
    - `keywords` rules convert to slow full-text searches. Scope them with an index or source type in your pipeline.
    - Copying converted queries into the SIEM and editing them there. The YAML in git must stay the single source of truth.

## Checklist

- [ ] `sigma check` clean
- [ ] Correct `logsource` for your data
- [ ] Pipeline maps every field the rule uses
- [ ] Converted query reviewed by eye
- [ ] Positive sample returns a hit in the SIEM
- [ ] Wazuh translation (if used) tested with `wazuh-logtest`

## Related pages

- [Detection lifecycle](detection-lifecycle.md)
- [Writing good detections](writing-good-detections.md)
- [Testing and tuning](testing-and-tuning.md)
- [Detection engineering home and rule library](index.md)
