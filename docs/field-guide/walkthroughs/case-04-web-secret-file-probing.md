# Case 04: Web Secret-File Probing

Thousands of web requests for files like `/.env` and `/.git/config` hit every public site all day. Almost all get a 404 and mean nothing. This case is about finding the one request that got a 200, and deciding whether a secret actually leaked.

!!! abstract "At a glance"
    - Attack: scanning for exposed configuration and secret files
    - Starts from: web and WAF alerts
    - Playbook: [Web application attack](../../04-playbooks/web-application-attack.md)

## The alert

```text
01:26 UTC. Rule: "Repeated requests for sensitive files from one source".
Source: 78.153.140.156
Target: shop.example.com
180 requests in 10 minutes for paths like /.env, /.git/config, /config.php.bak, /backup.zip
```

**Stop. What one field decides whether this matters?** Write it down.

## L1 triage

| Check | Finding |
|---|---|
| Is it a scanner of ours or an approved test? | No, not on the allow list; external hosting IP |
| Generic or targeted? | Generic: a wordlist of hundreds of common secret-file paths |
| What response codes did the attack requests get? | Mostly 404. But two requests returned 200 |
| Does the targeted software exist here? | Some paths are for software we do not run (noise); some are generic |

The decider is the **response code and size**. A 404 is a miss. A 200 might be a hit, or it might be the site returning its homepage for any path.

### Attack requests that got a success response

=== "Splunk SPL"

    ```spl
    index=web sourcetype=access_combined host=shop.example.com
      (uri="*/.env*" OR uri="*/.git/*" OR uri="*.bak" OR uri="*backup.zip*") status=200
    | table _time clientip uri status bytes
    ```

=== "IBM QRadar AQL"

    ```sql
    SELECT starttime, sourceip, URL, "HTTP Response Code" AS status
    FROM events
    WHERE (URL ILIKE '%/.env%' OR URL ILIKE '%/.git/%' OR URL ILIKE '%.bak')
      AND "HTTP Response Code" = '200' LAST 1 DAYS
    ```

## Escalation to L2

```text
Escalated 01:40 UTC by L1.
Verdict: secret-file scanning from 78.153.140.156. Two requests returned 200:
GET /.env and GET /.git/config. Need to confirm whether real secrets were served
or the app returns its homepage for unknown paths.
Asks: confirm with response size and content; if real, rotate exposed secrets.
```

## L2 investigation

A 200 is not proof. Single-page apps often return the homepage (a large HTML file) for any path, which also scores 200. The response size tells them apart.

| Request | Status | Size | Verdict |
|---|---|---|---|
| GET /.env | 200 | 41,603 bytes | Same size as the homepage: SPA fallback, not the real `.env` |
| GET /.git/config | 200 | 48 bytes | Small, distinct from the homepage: this looks like a real file |

The `.git/config` response is small and specific. The analyst confirms, carefully, that it is a real git config file, which means the `.git` directory is exposed and an attacker could reconstruct source code and any secrets committed to it.

!!! warning "Confirm without leaking further"
    When checking whether a secret file is served, an analyst should look at the response the server already returned in the logs or retrieve it into a controlled environment, not paste secrets around. If a real `.env` were served, its contents are the sensitive data; treat them as such.

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Block access to dot-files and the `.git` directory at the web server or WAF | Web team | L2, virtual patch |
| Block 78.153.140.156 (time-limited) | SOC | L2 |
| Rotate every secret that was in the exposed git history | App owner | L2, escalated: assume exposed |
| Remove the `.git` directory from the web root; fix the deployment that put it there | App owner | L2 |

The git history contained an old database password and an API key; both were rotated.

## Outcome

Most of the scan was noise, and one of the two 200s was a false positive (the SPA homepage). But `.git/config` was genuinely exposed, which meant the source code and its committed secrets were reachable. The case turned on reading response sizes, not just status codes, and on knowing that a 200 can be a homepage fallback.

## Lessons learned

- [ ] Detection tuned: a `.env` or `.git` request that returns 200 **and** a response size different from the homepage. This cuts the SPA-fallback false positives that otherwise bury real hits.
- [ ] Deployments must never ship the `.git` directory or dot-files to the web root; add a pipeline check.
- [ ] Secrets must not live in source control; add secret scanning to the repository.

## Quiz

1. Why is a 200 response not enough to confirm a secret leaked?
2. What distinguished the real hit from the false positive?
3. Why rotate secrets from the git history even though you only saw `.git/config`?

??? note "Answers"
    1. Many apps return their homepage (a large HTML page, status 200) for any unknown path. The status alone does not tell you a real file was served.
    2. The response size: the fake hit matched the homepage size; the real `.git/config` was small and distinct.
    3. An exposed `.git` directory lets an attacker reconstruct the whole repository, including any secrets ever committed. Assume everything in that history is exposed.

## Related pages

- [Web application attack playbook](../../04-playbooks/web-application-attack.md)
- [Data exfiltration playbook](../../04-playbooks/data-exfiltration.md)
- [Cloud account compromise playbook](../../04-playbooks/cloud-account-compromise.md)
