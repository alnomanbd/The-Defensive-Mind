# T02: SIEM Platforms

The SIEM is where you spend most of your day. This module teaches how the common platforms work and how to search them, so you can move between jobs without starting over. The same question, answered in every major query language.

!!! abstract "At a glance"
    - Level: L1 to L2
    - Time: 6 to 8 hours with labs
    - Outcome: you can search Splunk, Microsoft Sentinel, Elastic, IBM QRadar and Wazuh for the same answer

## Learning objectives

- [ ] Explain what a SIEM does: collect, parse, correlate, alert, search, retain.
- [ ] Read and write basic searches in SPL, KQL, Elastic, QRadar AQL and Wazuh.
- [ ] Filter, group and count events to answer a real question.
- [ ] Understand fields, parsing and why your data model matters.
- [ ] Keep a field-mapping note so you can move between SIEMs.

## Lessons

1. **What a SIEM does.** The pipeline from raw log to searchable, alertable data.
2. **The platforms.** Splunk, Microsoft Sentinel, Elastic and OpenSearch, IBM QRadar, Wazuh: what each is strong at, and how they are priced.
3. **Searching.** Filter, then transform (stats, summarize, table), in each language.
4. **Fields and parsing.** Why the same event looks different in each tool, and how to find the field you need.
5. **Correlation and alerts.** How a rule becomes an alert, and why severity and noise matter.
6. **Portability.** Keeping a one-page mapping from common fields to each SIEM's names.

## Query drill: failed logins grouped by source

The same question in five languages. Run it in your lab and compare.

=== "Splunk SPL"

    ```spl
    index=auth action=failure earliest=-24h
    | stats count by src_ip, user
    | sort - count
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    SigninLogs
    | where TimeGenerated > ago(24h) and ResultType != 0
    | summarize count() by IPAddress, UserPrincipalName
    | order by count_ desc
    ```

=== "Elastic"

    ```text
    event.category : "authentication" and event.outcome : "failure"
    (then a terms aggregation on source.ip and user.name, last 24h)
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT sourceip, username, COUNT(*) AS n
    FROM events
    WHERE qid IN (SELECT qid FROM qidmap WHERE qidname ILIKE '%authentication failure%')
    GROUP BY sourceip, username ORDER BY n DESC LAST 24 HOURS
    ```

=== "Wazuh"

    ```text
    rule.groups:authentication_failed   (then visualise count by data.srcip and data.srcuser)
    ```

## Lab

- [ ] Install Wazuh (or use Splunk free, or Elastic) and send it auth logs.
- [ ] Run the failed-login search above in your SIEM.
- [ ] Change it to show only sources with more than 10 failures.
- [ ] Add a second search: the same for successful logins, and find any source with both.
- [ ] Write a field-mapping note: how `src_ip` and `user` are named in your SIEM.

## Self-check

1. What are the two basic steps of almost every SIEM search?
2. Why does the same login event look different in Splunk and QRadar?
3. Why keep a field-mapping note?

??? note "Answers"
    1. Filter to the events you want, then transform them (count, group, table).
    2. Each SIEM parses raw logs into its own field names and data model; the underlying event is the same, the field names differ.
    3. So you can translate a detection or an investigation from one SIEM to another, which is how you stay useful across jobs and tools.

## Links to the handbook and kit

- [Alert triage](../../02-daily-operations/alert-triage.md)
- [Investigation cheat sheet](../../field-guide/investigation-cheatsheet.md)
- [Detection engineering](../../05-detection-engineering/index.md)

## Next module

[T03 Log Sources Every Analyst Must Know](../t03-log-sources/index.md).
