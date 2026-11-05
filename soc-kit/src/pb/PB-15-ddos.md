---
id: PB-15
title: DDoS
owner: SOC lead with the network team
audience: SOC analyst L1 / L2, network and infrastructure teams
review: Every 12 months, and after every real incident that used this playbook
summary: "How to respond to a distributed denial of service (DDoS) attack: traffic floods or request floods that make a website, API, DNS or network link slow or unavailable. The SOC rarely stops a DDoS alone; it confirms the attack, calls the right provider fast, and watches for anything hiding behind it."
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-15 |
| **Default severity** | P2 High while a customer-facing service is degraded; P3 Medium if mitigated with no impact (see Severity and SLA) |
| **Escalate to Critical when** | A critical service is down for more than 30 minutes, there is a ransom demand (RDoS), or the DDoS hides another intrusion |
| **MITRE ATT&CK** | T1498.001 Direct Network Flood, T1498.002 Reflection Amplification, T1499.002 Service Exhaustion Flood, T1499.003 Application Exhaustion Flood |
| **Typical alerts** | CDN or WAF DDoS event, bandwidth at link capacity, SYN flood alert on firewall, spike in HTTP 503 or 504, uptime monitor failures from many regions, sudden rise in requests per second to one URL |
| **Owner** | SOC lead with the network team |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

DDoS attacks come in three layers. **Volumetric** attacks fill your internet link with traffic (UDP floods, DNS or NTP amplification). **Protocol** attacks exhaust firewalls and load balancers (SYN floods). **Application layer (L7)** attacks send many valid-looking HTTP requests to expensive pages such as search or login. Attackers include extortionists (pay or we continue), hacktivists, competitors, and attackers creating noise to hide a real intrusion. Success for the defender: the provider mitigates within minutes, the business knows what is happening, and nothing else happens unseen in the meantime.

## 2. Triggers and detection

| Type | Signal | Log source |
|:---|:---|:---|
| Volumetric | Link usage near 100%, huge UDP volume, traffic from source port 53, 123, 389, 11211 | Router and firewall interface stats, NetFlow, ISP alert |
| Protocol | Firewall session table full, many half-open TCP connections | Firewall, load balancer |
| Application (L7) | Requests per second 10 to 100 times normal to one path, many IPs, same or random user agent | CDN or WAF analytics, web access logs |
| Ransom DDoS | Email threatening an attack unless paid, often with a short demonstration attack | Mail, abuse mailbox |

**Common false positives:** a marketing campaign or news mention (real users), a sale or launch, a search engine crawl, a broken client retrying in a loop, a load test nobody announced, an outage of your own system that looks like an attack.

## 3. Triage (first 15 minutes)

- [ ] Is the service actually degraded? Check from outside (uptime monitor, mobile network).
- [ ] What type: link full (volumetric), firewall or load balancer exhausted (protocol), or web servers busy (L7)?
- [ ] Is the traffic real users? Look at referrers, geographic spread, user agents, logged-in sessions. A campaign spike has normal browsing patterns.
- [ ] Is there a planned event, load test or deployment? Ask the service owner and change calendar.
- [ ] Is the CDN or DDoS protection already mitigating? Check its dashboard.
- [ ] Any ransom email or claim on social media?

Decision: real users, not an attack, hand to IT operations for capacity; attack mitigated with no impact, P3, record and monitor; service degraded, P2, start provider mitigation now; critical service down or ransom demand, P1.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Which service, IP or URL is targeted? | CDN analytics, firewall top destinations, access logs top URLs |
| What does the attack traffic look like? | Top source countries, ASNs, user agents, request paths, packet sizes, protocols |
| Is the origin server exposed directly, bypassing the CDN? | Traffic to origin IP from non-CDN ranges |
| Is anything else happening at the same time? | Login anomalies, new admin activity, data transfer, alerts on other systems |
| Who claims it? | Ransom email headers, hacktivist channels in threat intel |

### Queries: request rate and top sources during the attack

**Splunk SPL**


```spl
index=web earliest=-2h
| timechart span=1m count
```
```spl
index=web earliest=-30m
| stats count dc(clientip) as ips by uri_path, useragent
| sort - count | head 20
```

**Microsoft Sentinel KQL**


```kql
AzureDiagnostics
| where Category == "FrontDoorAccessLog" or Category == "ApplicationGatewayAccessLog"
| where TimeGenerated > ago(2h)
| summarize Requests = count(), IPs = dcount(clientIp_s) by bin(TimeGenerated, 1m)
| render timechart
```

**Elastic**


```text
Lens: count of records per minute, last 2 hours, split by url.path (top 5).
Then table: top source.geo.country_iso_code, source.as.organization.name, user_agent.original.
```

**IBM QRadar AQL**


```sql
SELECT sourceip, destinationip, destinationport, SUM(bytessent + bytesreceived) AS bytes, COUNT(*) AS flows
FROM flows
GROUP BY sourceip, destinationip, destinationport
ORDER BY bytes DESC LIMIT 20 LAST 30 MINUTES
```

**Wazuh**


```text
rule.groups:web   (then Visualize: date histogram per minute, split by data.srcip, top 10;
                   the web access log must be collected by the agent on the web server)
```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Call the DDoS mitigation provider or ISP (number in the runbook, not looked up during the attack) | Network team | The single most effective step for volumetric attacks |
| Turn on the CDN "under attack" or challenge mode for the affected site | SOC / Web team | Adds a browser check; may affect API clients |
| Apply rate limits on the targeted path (login, search, API) | Web team | Per IP and per session |
| Block or challenge by geography, ASN or user agent seen only in attack traffic | SOC | Time-limited; review false positives with the business |
| Restrict the origin server to accept traffic only from CDN IP ranges | Infrastructure | Stops attackers bypassing the CDN |
| Scale out or cache expensive pages | Infrastructure | Cost rises; agree a cap |
| Keep monitoring the rest of the environment for intrusion | SOC | A DDoS is a classic distraction |

## 6. Eradication and recovery

- [ ] Keep mitigation in place for at least 24 hours after the attack stops; attacks often return.
- [ ] Remove emergency blocks that hurt real users once traffic is normal.
- [ ] Change the origin IP if it was exposed, and keep it secret.
- [ ] Confirm with the provider what was mitigated and get their report.
- [ ] Update the DDoS runbook with contacts and steps that were missing.

> WARNING: Ransom DDoS. Do not pay and do not reply without legal. Many ransom DDoS emails are bluffs; others follow up with larger attacks. Inform the provider in advance so they can prepare.


## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Network team and service owner | Immediately | Analyst |
| SOC lead | Any customer impact | Analyst |
| CISO and IT leadership | Service degraded more than 15 minutes, or ransom demand | SOC lead |
| Customer support and communications | When customers notice; prepare a status page message | Incident lead |
| Law enforcement | Ransom DDoS, as legal decides | Legal |

See Escalation and Communication.

## 8. Evidence to keep

- CDN, WAF and firewall reports for the attack window (top sources, volume, duration).
- NetFlow or traffic samples (a short packet capture if possible).
- Provider tickets and mitigation reports.
- Any ransom or claim message with full headers.

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review:

- How long from first impact to provider mitigation? Was the provider contact ready?
- Was every public service behind the CDN or DDoS protection, including DNS?
- Was the origin server reachable directly?
- Did anything else happen during the attack?

Detections to add or tune: requests per minute per site against a baseline, origin traffic from non-CDN ranges, uptime monitor from multiple regions.


## Related documents

- Web Application Attack, Brute Force
- Escalation and Communication
- Tabletop Exercises
