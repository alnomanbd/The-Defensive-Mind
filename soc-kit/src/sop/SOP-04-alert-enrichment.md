---
id: SOP-04
title: Alert Enrichment (IP, domain, URL, hash, user, host)
owner: SOC Lead
audience: L1 analyst, L2 analyst
review: Every 6 months, and when an enrichment source is added or removed
summary: Which context to add to an alert, where to get it, how to read the result, and what must never be sent to outside services.
---
## 1. Purpose

An alert on its own rarely tells you if something is bad. Enrichment adds the context: is this IP known for attacks, who is this user, what does this server do, have we seen this file before. Done the same way every time, enrichment turns a 30-minute guess into a 5-minute decision.

## 2. Scope

- Every indicator and entity in an alert that the analyst relies on for a verdict.
- Manual enrichment by analysts and automatic enrichment by the SOAR or automation platform. Automation does not remove the need to read and judge the result.

## 3. Definitions

| Term | Meaning |
|---|---|
| Indicator of Compromise (IOC) | An observable linked to malicious activity: IP address, domain, URL, file hash, email address |
| Entity | A thing in your own environment: user, host, application, cloud account |
| Reputation | What threat intelligence sources say about an indicator |
| Passive DNS | History of which IPs a domain pointed to, and which domains pointed to an IP |
| Traffic Light Protocol (TLP) | Labels (CLEAR, GREEN, AMBER, RED) that say how far information may be shared |

## 4. Approved enrichment sources

Fill in the sources your SOC is allowed to use. Examples are given; keep at least one free option for each type.

| Type | Internal source | External examples | Data we may send |
|---|---|---|---|
| IP address | Firewall, proxy and VPN logs, asset inventory, threat intelligence platform (MISP, OpenCTI) | AbuseIPDB, GreyNoise, Shodan, VirusTotal, AlienVault OTX, IP geolocation | Public IPs only |
| Domain and URL | Proxy and DNS logs, email gateway | VirusTotal, URLscan.io, URLhaus, WHOIS, passive DNS | Domains and URLs that contain no internal data or personal data |
| File hash | EDR, threat intelligence platform | VirusTotal, MalwareBazaar, Hybrid Analysis | Hashes only. Files only with SOC Lead approval (SOP-40) |
| Email | Email gateway, mail trace | Header analysers | Headers with internal data removed |
| User | Directory (Active Directory, Entra ID, Okta), HR data | None | Never sent outside |
| Host | Asset inventory or CMDB, EDR, vulnerability scanner | None | Never sent outside |
| Cloud account | Cloud audit logs, cloud security posture tool | None | Never sent outside |

> WARNING: Submitting a URL to a public scanner can make it visible to everyone, including the attacker. Never submit URLs that contain tokens, session IDs, email addresses or internal host names. Never upload documents or files from users to public sandboxes.

## 5. Procedure

### 5.1 List what to enrich

1. Read the alert and the raw event.
2. List every indicator and entity that matters for the verdict: source and destination IP, domain, URL, file hash, user, host, process.
3. Check what automation already added. Do not repeat it; read it.

### 5.2 Enrich indicators

For each indicator, record the result in the triage note:

| Indicator | Check | Read it like this |
|---|---|---|
| Public IP | Reputation score, number of reports, last report date, ASN and hosting type, country, open ports | A residential IP with no reports is different from a hosting provider IP with 500 reports last week. Old reports matter less. Cloud and CDN IPs are shared, so judge carefully |
| Private IP | Asset inventory: what host, which owner, which network zone | An unknown internal IP is a finding in itself |
| Domain | Age (WHOIS creation date), registrar, reputation, passive DNS, look-alike of our brand | A domain created in the last 30 days in a login link is high risk |
| URL | Reputation, scan screenshot, redirect chain, final landing page | Look at what the page does, not only its score |
| File hash | Detection count, first seen date, file name, signer, sandbox behaviour | Zero detections does not mean safe: new malware often has none. Unknown plus unsigned plus odd location is suspicious |
| Email sender | SPF, DKIM, DMARC results, reply-to mismatch, display name spoofing | A pass on all three does not mean safe; attackers use real accounts |

### 5.3 Enrich entities

| Entity | Check |
|---|---|
| User | Job role, department, manager, privileged or not, service account or human, normal working hours and locations, recent password reset or MFA change, account age |
| Host | Owner, function (laptop, server, domain controller), criticality, operating system and patch level, EDR status, known vulnerabilities, internet facing or not |
| Process | Parent process, command line, signer, file path, how often it runs across the fleet |

### 5.4 Internal history

1. Search 7 days (30 days for High and Critical) for the same indicator across all logs (Appendix A).
2. Check if the indicator is already in the threat intelligence platform, the block list, or the allow list.
3. Check past cases for the same user, host or indicator.

### 5.5 Record and share

1. Put the enrichment summary in the triage note under "Enrichment", with the source and time for each result.
2. New malicious indicators confirmed in a TP: submit them through SOP-32 IOC Lifecycle so they are blocked and swept.
3. Respect TLP labels when copying intelligence into tickets or emails.

## 6. Automation

The SOAR or automation platform should enrich automatically on alert creation:

- [ ] Public IP reputation and geolocation
- [ ] Domain age and reputation
- [ ] File hash reputation
- [ ] User and host details from the directory and asset inventory
- [ ] Previous alerts for the same entity in the last 7 days

Automation must cache results and respect the rate limits of free services. The analyst still reads the results and makes the decision.

## 7. Records

- Enrichment section in the triage note, with sources and times.
- Indicators submitted to the threat intelligence platform with the case reference.

## 8. Metrics

| Metric | Target |
|---|---|
| Alerts with automatic enrichment | 90 percent or more |
| Median manual enrichment time per alert | Under 5 minutes |
| Incidents of sensitive data sent to outside services | Zero |

## 9. Common mistakes

- Treating "0 detections" or "no reports" as proof that something is clean.
- Trusting geolocation for VPN, cloud and mobile IPs.
- Uploading a user's document to a public sandbox.
- Enriching the indicator but not the user and host. The same IP means different things on a developer laptop and on a domain controller.
- Copying TLP:AMBER or TLP:RED intelligence into a ticket that other teams can read.

## 10. Related documents

- SOP-03 Alert Triage and Classification, SOP-32 IOC Lifecycle, SOP-40 Malware Sample Handling and Sandbox Analysis
- GOV-10 Privacy and Data Handling in Investigations, TPL-19 IOC Submission

---page---

## Appendix A. Indicator sweep queries (30 days)

Splunk (SPL):

```spl
index=* ("203.0.113.10" OR "bad-domain.example" OR "44d88612fea8a8f36de82e1278abb02f") earliest=-30d
| stats count min(_time) as first max(_time) as last values(host) as hosts by index, sourcetype
| convert ctime(first) ctime(last)
```

Microsoft Sentinel (KQL):

```kql
search in (CommonSecurityLog, DeviceNetworkEvents, DeviceFileEvents, DnsEvents, EmailUrlInfo)
    "203.0.113.10" or "bad-domain.example" or "44d88612fea8a8f36de82e1278abb02f"
| where TimeGenerated > ago(30d)
| summarize Count = count(), First = min(TimeGenerated), Last = max(TimeGenerated) by $table
```

Elastic (KQL in Discover, last 30 days):

```text
source.ip : "203.0.113.10" or destination.ip : "203.0.113.10" or dns.question.name : "bad-domain.example" or file.hash.md5 : "44d88612fea8a8f36de82e1278abb02f"
```

IBM QRadar (AQL):

```sql
SELECT LOGSOURCENAME(logsourceid) AS source, sourceip, destinationip, COUNT(*) AS n,
  MIN(starttime) AS first_seen, MAX(starttime) AS last_seen
FROM events
WHERE sourceip = '203.0.113.10' OR destinationip = '203.0.113.10'
   OR UTF8(payload) ILIKE '%bad-domain.example%'
GROUP BY logsourceid, sourceip, destinationip LAST 30 DAYS
```

Payload searches are slow in QRadar. Prefer a reference set of IOCs and a rule that tests against it.

Wazuh (dashboard query):

```text
data.srcip:"203.0.113.10" or data.dstip:"203.0.113.10" or data.url:*bad-domain.example* or syscheck.md5_after:"44d88612fea8a8f36de82e1278abb02f"
```
