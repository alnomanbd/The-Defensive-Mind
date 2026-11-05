---
id: PB-11
title: Web Application Attack
owner: SOC lead with the application security team
audience: SOC analyst L1 / L2, application owners
review: Every 12 months, and after every real incident that used this playbook
summary: "How to handle attacks against websites and APIs: SQL injection, cross-site scripting (XSS), path traversal, probing for secret files, and exploitation of known vulnerabilities. The key question is always the same: did any request succeed?"
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-11 |
| **Default severity** | P4 Low for blocked scanning; P3 Medium for targeted attempts; P2 High for a successful exploit (see Severity and SLA) |
| **Escalate to Critical when** | Data was extracted from the database, a web shell was uploaded, the server ran attacker commands, or customer personal or payment data is exposed |
| **MITRE ATT&CK** | T1190 Exploit Public-Facing Application, T1595.002 Vulnerability Scanning, T1595.003 Wordlist Scanning, T1505.003 Web Shell, T1059 Command and Scripting Interpreter, T1083 File and Directory Discovery, T1552.001 Credentials in Files |
| **Typical alerts** | WAF SQL injection or XSS block, many 404s from one source, requests for `/.env`, `/.git/config`, `/wp-config.php.bak`, `../` in URLs, a 200 response to an attack pattern, new script file in the web root, web server process spawning a shell |
| **Owner** | SOC lead with the application security team |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

Every public website is scanned all day by bots looking for known weaknesses. Most of these requests fail and are only noise. What matters is (a) a **targeted** attacker who has learned the application and adapts, (b) any attack request that receives a **successful response** (HTTP 200 with a large body, a 500 error that leaks data, or a time delay that shows blind SQL injection), and (c) signs that the server itself is compromised: a **web shell** or the web server starting a command shell. Success for the defender: noise is handled by the WAF, the one successful request is found quickly, and the vulnerability is fixed, not just blocked.

## 2. Triggers and detection

| Attack | Signal in logs | Log source |
|:---|:---|:---|
| SQL injection | `' OR 1=1`, `UNION SELECT`, `SLEEP(`, `information_schema` in URL or body; database errors in responses | WAF, web server access log, application log, database log |
| Cross-site scripting | `<script>`, `onerror=`, `javascript:` in parameters | WAF, access log |
| Path traversal and file inclusion | `../`, `%2e%2e%2f`, `/etc/passwd`, `php://filter` | WAF, access log |
| Secret file probing | Requests for `/.env`, `/.git/`, `/backup.zip`, `/config.php.bak`, `/.aws/credentials` | Access log, WAF |
| Known vulnerability exploit | Paths of known CVEs (for example `/cgi-bin/`, `/actuator/`, `/vendor/phpunit/`), JNDI strings (`${jndi:`) | WAF, IPS, access log |
| Web shell | New `.php`, `.jsp`, `.aspx` file in a web folder; requests to an unusual script with `cmd=` parameters; `w3wp.exe`, `php-fpm` or `java` starting `cmd.exe`, `sh`, `whoami` | File integrity monitoring, EDR, access log |
| Credential stuffing on the login page | Many POSTs to `/login` from many IPs | See Brute Force |

**Common false positives:** your own vulnerability scanner or penetration test (check the schedule and source IPs), search engine crawlers hitting old URLs, application features that legitimately send HTML or SQL-like text (CMS editors, report builders), uptime monitors.

## 3. Triage (first 15 to 30 minutes)

- [ ] Is the source a known scanner of ours, an approved pentest, or a search engine? Yes, tune and close.
- [ ] What was the response code and size for the attack requests? Any 200 with a large body, any 500, any unusually slow response?
- [ ] Did the WAF block or only log? Is the WAF in detection mode for this site?
- [ ] Is the attack generic (thousands of paths, many sites) or targeted (one parameter tried many ways)?
- [ ] Does the targeted software and version actually exist on this server? A WordPress exploit against a Java site is noise.
- [ ] Any new files in the web root, or shell processes from the web server, in the same time window?

Decision: all blocked or 404 and the software is not present, P4, confirm blocking and close; targeted attempts with no success, P3, block source and tell the application owner; any success, web shell or command execution, P2 at least and continue; data extracted or personal data exposed, P1.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Did any attack request succeed? | Access log: status 200 or 500 for requests with attack patterns; compare response size to normal |
| What data could the injection read? | Application and database logs: queries run, rows returned; the vulnerable parameter's access to tables |
| Were secret files downloaded? | Status 200 for `/.env`, `/.git/` paths; then treat every secret in that file as leaked |
| Is there a web shell? | New or modified files in web folders (FIM, `find -newer`), EDR child processes of the web server |
| What did the attacker run on the server? | EDR process tree, shell history, outbound connections from the web server |
| Did they move further? | Connections from the web server to internal databases, other servers, cloud metadata (`169.254.169.254`) |
| Is the vulnerability real? | Application security team reproduces it safely in a test environment |

### Queries: attack requests that got a success response

**Splunk SPL**


```spl
index=web sourcetype=access_combined
  (uri_query="*union*select*" OR uri_query="*sleep(*" OR uri="*../*" OR uri="*/.env*" OR uri="*/.git/*" OR uri_query="*<script*")
  status IN (200, 500)
| stats count values(uri) as uris max(bytes) as max_bytes by clientip, status
| sort - max_bytes
```

**Microsoft Sentinel KQL**


```kql
AzureDiagnostics
| where Category == "ApplicationGatewayAccessLog"
| where requestUri_s has_any ("union", "sleep(", "../", "/.env", "/.git/", "<script")
| where httpStatus_d in (200, 500)
| summarize Count = count(), Uris = make_set(requestUri_s, 20), MaxBytes = max(sentBytes_d) by clientIP_s, httpStatus_d
```

**Elastic**


```text
url.original : (*union*select* or *sleep\(* or *../* or */.env* or */.git/* or *<script*)
  and http.response.status_code : (200 or 500)
```

**IBM QRadar AQL**


```sql
SELECT sourceip, URL, "HTTP Response Code" AS status, COUNT(*) AS n
FROM events
WHERE (URL ILIKE '%union%select%' OR URL ILIKE '%sleep(%' OR URL ILIKE '%../%' OR URL ILIKE '%/.env%' OR URL ILIKE '%/.git/%')
  AND "HTTP Response Code" IN ('200', '500')
GROUP BY sourceip, URL, "HTTP Response Code" LAST 24 HOURS
```

**Wazuh**


```text
rule.groups:web and rule.groups:attack and data.id:(200 or 500)
```

### Web shell hunting

**osquery**


```sql
-- Script files changed in web roots in the last 7 days
SELECT path, size, datetime(mtime,'unixepoch') AS modified, uid
FROM file
WHERE (path LIKE '/var/www/%%' OR path LIKE 'C:\inetpub\wwwroot\%%')
  AND (filename LIKE '%.php' OR filename LIKE '%.jsp' OR filename LIKE '%.aspx')
  AND mtime > (strftime('%s','now') - 604800);
```

**Microsoft Defender KQL**


```kql
DeviceProcessEvents
| where InitiatingProcessFileName in~ ("w3wp.exe","php-cgi.exe","httpd.exe","nginx.exe","tomcat9.exe","java.exe")
| where FileName in~ ("cmd.exe","powershell.exe","whoami.exe","net.exe","certutil.exe","bitsadmin.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, FileName, ProcessCommandLine
```

**Linux command line**


```bash
find /var/www -type f \( -name "*.php" -o -name "*.jsp" \) -newermt "$(date -d '-7 days' +%F)" -ls
grep -rlE "eval\(base64_decode|system\(\\\$_(GET|POST|REQUEST)|assert\(\\\$_" /var/www 2>/dev/null
```

```yara
rule WebShell_PHP_Generic
{
    meta:
        description = "Common PHP web shell patterns, expect some false positives"
    strings:
        $a = /eval\s*\(\s*base64_decode/ nocase
        $b = /(system|passthru|shell_exec|exec)\s*\(\s*\$_(GET|POST|REQUEST)/ nocase
        $c = "assert($_" nocase
    condition:
        filesize < 200KB and any of them
}
```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Block the source IPs at WAF or CDN (time-limited) | SOC | Attackers rotate IPs; this buys time only |
| Add a virtual patch: a WAF rule for the exact vulnerable parameter | SOC / AppSec | Fast and safe; does not fix the code |
| Switch the WAF from detection to blocking mode for the site | AppSec, app owner approves | Test for false positives on key user journeys |
| Disable the vulnerable feature or page | App owner | Better than taking the whole site down |
| Remove any web shell, after collecting a copy and its hash | Server team | Look for more than one; attackers plant backups |
| Isolate the server if commands were executed | SOC / Infrastructure | May cause an outage; incident lead decides |
| Rotate every secret the application could read (database passwords, API keys, `.env` values) | App owner | Assume all are stolen if a shell ran or `.env` was downloaded |

## 6. Eradication and recovery

- [ ] Fix the root cause in code (parameterised queries, output encoding, input validation) and deploy through the normal pipeline.
- [ ] Patch or upgrade the vulnerable framework, plugin or server software.
- [ ] Rebuild the server from a clean image if the attacker ran commands; redeploy the application from source control.
- [ ] Remove secret files from the web root; block dot-files at the web server.
- [ ] Run a DAST scan (OWASP ZAP or similar) and a code scan before reopening the feature.
- [ ] Monitor the site for 14 days: same parameter, same sources, new files in the web root.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Application owner | Any targeted attack, any success | Analyst |
| Application security and development team | To fix the vulnerability | SOC lead |
| SOC lead | Any success | Analyst |
| CISO, legal, privacy | Data extracted, personal or payment data exposed | SOC lead |
| Customers | If legal decides there is a notifiable breach | Legal and communications |

See Escalation and Communication.

## 8. Evidence to keep

- Access logs, WAF logs and application logs for the full attack window (plus 30 days before, for earlier probing).
- Copies of any web shell or uploaded file, with hashes.
- Database query logs showing what was read.
- Server image or snapshot if commands were executed.

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review:

- Why did the vulnerability reach production? Was there code scanning (SAST), dependency scanning (SCA) and DAST in the pipeline?
- Was the WAF in blocking mode? Did anyone review its alerts?
- Were secrets stored in files inside the web root?
- Did the SOC have the access logs and response codes needed to answer "did it succeed"?

Detections to add or tune: attack pattern with a 200 or 500 response, any request to dot-files that returned 200, web server processes spawning shells, new script files in web roots.


## Related documents

- Brute Force, Data Exfiltration, Cloud Account Compromise, DDoS
- Alert Triage
- Incident Report template
