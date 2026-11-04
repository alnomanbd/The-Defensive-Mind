# External Attack Surface Management

External Attack Surface Management (EASM) means continuously finding everything you expose to the internet and checking it the way an attacker would. This page gives the Security Operations Center (SOC) a discovery procedure, a daily scan-and-diff routine, alert rules and a reference build with open-source tools.

!!! abstract "At a glance"
    - Audience: SOC analyst L2/L3, SOC manager, infrastructure owners
    - Time to read: 15 minutes
    - Outcome: you can build an internet-facing inventory, scan it daily, alert on change, and route findings to owners

## Rules before you scan

!!! danger "Authorisation first"
    - Scan **only** IP ranges and hostnames your organisation owns or has written permission to test.
    - Get a signed scope document from the infrastructure owner listing ranges, times and allowed intensity.
    - Cloud providers and hosting companies have their own scanning policies; read them.
    - Hosts behind a shared service (CDN, SaaS, shared hosting) belong to someone else: inventory them, do not port-scan them.
    - Tell the network team and your upstream provider the scanner's source IP so it is not reported as an attack.
    - Use polite timing (`-T3` or lower) for production; never run exploit or brute-force scripts in EASM.

## Step 1: Discover assets

| Method | What it finds | Example command / source |
|---|---|---|
| Internal DNS zone export | Every name you publish | `dig axfr example.com @ns1.example.com` (only from an allowed host) or export from DNS provider |
| Certificate transparency | Every hostname that ever got a public TLS certificate, including forgotten ones | `crt.sh` JSON query (below) |
| Passive DNS | Historical name-to-IP mappings | Passive DNS services (free tiers exist) |
| Own IP ranges | Hosts with no DNS name | Regional internet registry records, cloud account public IP lists |
| Cloud account inventory | Load balancers, buckets, functions with public endpoints | Cloud CLI: list public IPs and endpoints per account |
| Subdomain enumeration (passive) | Names from public datasets | Open-source tools such as `subfinder` or `amass` in passive mode |
| Shodan InternetDB | Ports and known issues seen by a public scanner | `https://internetdb.shodan.io/<ip>` |

```bash
# Hostnames from certificate transparency
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | jq -r '.[].name_value' | tr 'A-Z' 'a-z' | sed 's/^\*\.//' | sort -u > ct-hosts.txt

# Passive subdomain enumeration
subfinder -d example.com -silent > sf-hosts.txt

# Merge and resolve
cat ct-hosts.txt sf-hosts.txt | sort -u > all-hosts.txt
while read h; do ip=$(dig +short A "$h" | tail -1); echo "$h,$ip"; done < all-hosts.txt > host-ip.csv
```

## Step 2: Build the inventory

Every row needs an owner. A host without an owner is a finding in itself.

| Field | Example |
|---|---|
| Hostname | `portal.example.com` |
| IP | `203.0.113.20` |
| Hosted by | Own data centre / cloud account / SaaS / CDN |
| Owner (team + person) | Web team / A. Patel |
| Business function | Customer portal |
| Scan allowed | Yes / No (third party) |
| Monitored by SIEM | Yes / No |
| Expected ports | 443 |
| Status | Active / decommission pending / unknown |

!!! tip "Unknown and shadow assets"
    Names found in certificate transparency or DNS that nobody claims are shadow assets: old test servers, marketing microsites, forgotten admin panels. Send the list to IT management weekly until every row has an owner or is shut down. Never delete an unknown row from the inventory; mark it "not ours" with evidence if it belongs to a third party.

## Step 3: Daily scan and diff

```bash
#!/usr/bin/env bash
# easm-daily.sh - scan authorised ranges, diff with yesterday
set -euo pipefail
D=$(date +%F); Y=$(date -d yesterday +%F)
OUT=/opt/easm/results

nmap -sS -Pn -T3 --top-ports 1000 -sV --version-light \
     -iL /opt/easm/scope-authorised.txt -oX "$OUT/scan-$D.xml"

# Open ports as host:port/service lines
xmllint --xpath '//host[ports/port/state/@state="open"]' "$OUT/scan-$D.xml" >/dev/null 2>&1 || true
python3 /opt/easm/xml2lines.py "$OUT/scan-$D.xml" | sort > "$OUT/open-$D.txt"

# Change detection
comm -13 "$OUT/open-$Y.txt" "$OUT/open-$D.txt" > "$OUT/new-$D.txt"     # newly opened
comm -23 "$OUT/open-$Y.txt" "$OUT/open-$D.txt" > "$OUT/closed-$D.txt"  # closed since yesterday
```

`ndiff` (ships with nmap) is a quick alternative: `ndiff scan-Y.xml scan-D.xml`.

Enrich each public IP with what a public scanner sees:

```bash
curl -s https://internetdb.shodan.io/203.0.113.20
# {"ip":"203.0.113.20","ports":[22,443],"cpes":["cpe:/a:openbsd:openssh:8.2"],
#  "hostnames":["portal.example.com"],"tags":[],"vulns":["CVE-2023-XXXXX"]}
```

## Step 4: Risky services list

Any of these exposed to the whole internet is a finding. Tune by business need and record accepted exceptions.

| Port(s) | Service | Risk | Default severity |
|---|---|---|---|
| 3389 | Remote Desktop Protocol (RDP) | Brute force, ransomware entry | Critical |
| 22 | SSH (Secure Shell) | Brute force; acceptable only with keys + allow-list | Medium |
| 23 | Telnet | Plaintext logins | Critical |
| 445, 139 | SMB (Server Message Block) | Wormable exploits, data theft | Critical |
| 21 | FTP (File Transfer Protocol) | Plaintext logins, anonymous access | High |
| 1433, 3306, 5432, 1521 | Databases | Direct data access | Critical |
| 6379, 27017, 9200, 11211 | Redis, MongoDB, Elasticsearch, Memcached | Often no authentication | Critical |
| 2375, 2376, 6443, 10250 | Docker API, Kubernetes API, kubelet | Full host / cluster takeover | Critical |
| 5900 | VNC (Virtual Network Computing) | Weak or no auth | Critical |
| 161/udp | SNMP (Simple Network Management Protocol) | Information leak, default communities | High |
| 8080, 8443, 9000, 10000 | Admin panels, app servers | Default credentials, unpatched panels | High |
| 500, 4500/udp, 443 VPN | VPN gateways | Frequently exploited edge devices; patch fast | High (watch version) |

## Step 5: Certificate expiry and hygiene

```bash
# Days until expiry for each HTTPS host
while read h; do
  end=$(echo | timeout 5 openssl s_client -servername "$h" -connect "$h:443" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  [ -n "$end" ] && echo "$h,$(( ( $(date -d "$end" +%s) - $(date +%s) ) / 86400 ))"
done < https-hosts.txt | sort -t, -k2 -n
```

| Days left | Action |
|---|---|
| < 0 | Critical: expired, users see errors, attackers can impersonate trust failures |
| 0-7 | High: ticket to owner, daily reminder |
| 8-30 | Medium: ticket to owner |
| > 30 | None |

Also flag: self-signed certificates on public services, hostname mismatch, weak protocols (TLS 1.0/1.1).

## Step 6: Known-CVE matching by version

Match service banners and Common Platform Enumeration (CPE) strings to Common Vulnerabilities and Exposures (CVE) entries, then prioritise anything in a known-exploited catalogue.

```bash
# Version detail for one host
nmap -sV -p 443,22 portal.example.com
# Check product+version against the known-exploited catalogue
jq -r '.vulnerabilities[] | select(.product|test("OpenSSH";"i")) | .cveID' kev.json
```

!!! warning "Version matching produces false positives"
    Many Linux distributions back-port security fixes without changing the version string. A banner saying "OpenSSH 8.2" may already be patched. Before raising a critical ticket: confirm with the owner's package version (`dpkg -l`, `rpm -q`), the vendor advisory, or an authenticated scan. Record the outcome so the same false positive is suppressed next time.

## Step 7: Alert on change, report persistence

| Finding | Alert channel | Repeat? |
|---|---|---|
| New open port on any host | Immediate ticket + alert | No; once per change |
| New risky service (table above) | Immediate, high/critical | No |
| New hostname in certificate transparency, not in inventory | Ticket to L2 | No |
| Cert expires in ≤ 7 days | Ticket, daily reminder | Yes until fixed |
| Known-exploited CVE on exposed service | Immediate, critical | Daily until fixed or accepted |
| Persistent known findings | Weekly digest to owners and SOC manager | Weekly |
| Scanner failed or scope file empty | Ops alert | Yes |

!!! tip "Keep alerting while risk persists, without spamming"
    The SOC's job is to make risk visible until it is fixed or formally accepted. Use one alert at first detection, then a weekly digest that lists every open item with its age. Close only on fix or a signed [risk acceptance](../09-templates/risk-acceptance.md).

## Reference architecture (open source)

```text
 [scope-authorised.txt] [domains.txt]
          |                  |
          v                  v
   nmap daily scan     crt.sh + subfinder + DNS resolve
          |                  |
          +--------+---------+
                   v
          normaliser (python): host, port, service, version, cert days
                   |
         +---------+-----------+
         v                     v
  InternetDB / KEV       inventory DB (owner, allowed, expected ports)
  enrichment                   |
         +---------+-----------+
                   v
          diff vs yesterday -> new / closed / persistent
                   |
     +-------------+--------------+
     v             v              v
  SIEM index    tickets to     weekly digest
  (dashboards)  owners         (email/chat)
```

Run it from a dedicated small VM with a fixed public IP, scheduled by cron or your automation platform. Keep 90 days of raw results for trend charts.

## Worked example

```text
06:10  Daily diff: new line "203.0.113.45:3389/ms-wbt-server"
06:11  Ticket EASM-221 (Critical): RDP exposed on 203.0.113.45 (inventory: test-app, owner Infra team)
08:00  L1 confirms in yesterday's scan port was closed; InternetDB already lists 3389
08:15  L2 checks firewall change log: temporary rule for vendor support, no expiry set
08:20  L2 searches SIEM for failed RDP logons on host: 1,400 attempts from 37 IPs since 02:00
08:30  Owner removes rule; vendor moved to VPN access. L2 checks no successful external logons.
Next day: port closed -> ticket closed with root cause "temporary firewall rule without expiry"
```

## Metrics

| Metric | Target |
|---|---|
| Inventory rows with an owner | 100% |
| Median days new critical exposure -> fixed | < 2 |
| Critical risky services open > 7 days | 0 (or formally accepted) |
| Certificates expired on public services | 0 |
| Shadow assets found this month / resolved | Tracked |
| Daily scan success rate | 100% |

## Checklist

- [ ] Written scan authorisation and scope file
- [ ] Inventory with owner per row
- [ ] Daily scan + diff scheduled, failure alert in place
- [ ] Risky services list tuned and exceptions documented
- [ ] Cert expiry check running
- [ ] CVE matches verified before critical tickets
- [ ] Weekly persistent-findings digest

## Related pages

- [Threat Intelligence overview](index.md)
- [The Intelligence Lifecycle](ti-lifecycle.md)
- [IOC Management](ioc-management.md)
- [Automation catalogue](../07-automation-soar/automation-catalog.md)
- [Risk acceptance template](../09-templates/risk-acceptance.md)
- [Technology stack](../01-build-a-soc/technology-stack.md)
