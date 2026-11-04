# Dark Web and Credential Monitoring

Stolen logins are the cheapest way into most organisations. This page gives the Security Operations Center (SOC) a daily, automatable procedure to find exposed company credentials and leak-site mentions early, using free sources first, and a clear response workflow. Terms used below: Single Sign-On (SSO), Virtual Private Network (VPN), Multi-Factor Authentication (MFA), Remote Desktop Protocol (RDP), Kusto Query Language (KQL), Endpoint Detection and Response (EDR).

!!! abstract "At a glance"
    - Audience: SOC analyst L1/L2/L3, SOC manager
    - Time to read: 15 minutes
    - Outcome: you can run a daily credential and leak check, read the results, decide what to alert on, and respond without breaking privacy rules

## How company data reaches the dark web

| Route | What happens | What the attacker gets | Typical signal for you |
|---|---|---|---|
| Infostealer malware | Malware on a personal or work device copies browser-saved passwords, cookies and autofill, then uploads a "log" | Working username + password + session cookies for every site the user visited, including your SSO and VPN | Infostealer lookup shows a compromised machine with your login URLs |
| Third-party breach | A website where staff used their work email is breached | Email + password (often hashed, sometimes plaintext) | Breach notification service lists employee emails |
| Combo lists | Old breaches are merged and re-sold as email:password lists | Large lists used for credential stuffing | Same emails reappear across many "new" leaks |
| Phishing kits | Fake login pages capture credentials live | Fresh credentials and sometimes MFA codes | Lookalike domain, staff phishing report |
| Initial access brokers | Criminals sell working access (VPN, RDP, admin panel) to ransomware groups | Ready-to-use foothold | Forum listing mentioning your sector, size, country, revenue |
| Ransomware leak sites | Group posts victim name and stolen data to pressure payment | Public exposure of your or a supplier's data | Company or supplier name on a leak site tracker |

!!! danger "Infostealer logs are the most urgent"
    A stealer log usually contains live session cookies. These can bypass MFA until the session is revoked. Treat a fresh stealer hit on a work account as an active incident, not a hygiene issue.

## What to monitor

| Watch item | Example | Source type | Priority |
|---|---|---|---|
| Company email domains | `@example.com`, `@example.co.uk` | Breach services, infostealer lookups | High |
| Login URLs (employee-facing) | `sso.example.com`, `vpn.example.com`, `mail.example.com` | Infostealer lookups ("URLs found in logs") | Critical |
| Customer-facing login pages | `app.example.com/login` | Infostealer lookups | High (customer account takeover) |
| Executive and admin personal emails (with consent) | CEO, finance, IT admins | Breach services | High |
| Brand and product keywords | `ACME`, `acmepay` | Leak site trackers, paste monitors, forums (paid) | Medium |
| Ransomware leak sites | Company, key suppliers, key customers | Leak site trackers | Critical for self, high for suppliers |
| Lookalike domains | `examp1e.com`, `example-login.com` | Certificate transparency | High |
| Code and secrets | API keys, tokens in public repos | Secret scanning on public code platforms | High |

## Free sources and example calls

Endpoints and limits change; check each provider's documentation and terms of use before automating. Store API keys in a secrets store, never in the script.

### Have I Been Pwned (HIBP): domain search

You must verify ownership of the domain in the HIBP dashboard first. API access requires a key (paid subscription tier).

```bash
# All breached accounts on a verified domain
curl -s -H "hibp-api-key: $HIBP_KEY" -H "user-agent: acme-soc-check" \
  "https://haveibeenpwned.com/api/v3/breacheddomain/example.com" | jq .
# Returns: { "alias": ["BreachName1","BreachName2"], ... }   alias = part before @

# Details of one breach (date, data classes)
curl -s "https://haveibeenpwned.com/api/v3/breach/BreachName1" | jq '{Name,BreachDate,DataClasses}'
```

### Hudson Rock free OSINT tools (infostealer exposure)

```bash
# Infostealer exposure for a domain (employees, users, third-party URLs)
curl -s "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain=example.com" | jq .

# Single email (use only for company accounts you are authorised to check)
curl -s "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email=j.doe@example.com" | jq .
```

Fields to read: total employees/users affected, date compromised, computer name / OS (often masked), the login URLs found. Free results are partly masked by design.

### ransomware.live (leak site tracker)

```bash
# Search victims by keyword
curl -s "https://api.ransomware.live/v2/searchvictims/acme" | jq -r '.[] | [.post_title,.group_name,.discovered] | @tsv'

# Recent victims (filter for suppliers and customers locally)
curl -s "https://api.ransomware.live/v2/recentvictims" | jq -r '.[].post_title' | grep -iFf watch-names.txt
```

### Certificate transparency (lookalike domains)

```bash
curl -s "https://crt.sh/?q=%25example%25&output=json" \
  | jq -r '.[].name_value' | sort -u | grep -v -E '(^|\.)example\.com$'
```

## Commercial categories (when free is not enough)

| Category | Adds | Consider when |
|---|---|---|
| Infostealer log intelligence | Full, unmasked hits, near-real-time, cookie data | Free lookups show recurring hits |
| Dark web / forum monitoring | Closed forums, access broker listings, chat channels | You are a likely target (finance, health, SaaS) |
| Digital risk protection | Lookalike domains, fake apps, social impersonation, takedowns | Brand abuse affects customers |
| Breach data aggregation | Large searchable breach corpus via API | You run many customer accounts |

## The daily automated check

Run once a day (for example 06:00) from your automation platform or a cron job. Results go to the ticket queue, not to a chat channel alone.

```text
1. Load watch lists: domains.txt, login-urls.txt, watch-names.txt (company, suppliers, customers)
2. For each domain:
     a. Query breach service      -> list of (alias, breach)
     b. Query infostealer lookup  -> counts + compromise dates + URLs
3. Query leak site tracker for each name in watch-names.txt
4. Query certificate transparency for lookalikes
5. Mask sensitive values (see rules below)
6. Compare with yesterday's state file (state.json)
     NEW item         -> create ticket, alert
     SAME item        -> no alert; include in weekly digest
     GONE item        -> note only
7. Save today's state; write a run log (counts, errors)
8. If any source failed -> alert "check did not run fully" (silent failure is the worst outcome)
```

Python outline:

```python
import json, os, hashlib, requests, datetime

state = json.load(open("state.json")) if os.path.exists("state.json") else {}
today, findings = {}, []

def key(*parts):                       # stable ID for diffing, no raw secrets
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]

for domain in open("domains.txt").read().split():
    r = requests.get(f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain",
                     params={"domain": domain}, timeout=30)
    r.raise_for_status()
    data = r.json()
    k = key("stealer", domain, str(data.get("total")))
    today[k] = {"type": "stealer", "domain": domain, "total": data.get("total")}
    if k not in state:
        findings.append(today[k])

# ... same pattern for breach service and leak-site tracker ...

json.dump(today, open("state.json", "w"))
for f in findings:
    print("NEW:", f)                   # replace with ticket/alert API call
```

## Reading results: what to alert on

| Finding | Alert? | Severity | Why |
|---|---|---|---|
| New infostealer hit, work account, compromised < 90 days, SSO/VPN/mail URL in log | Yes, immediately | Critical | Live credentials and cookies likely valid |
| New infostealer hit on customer-facing login URL | Yes | High | Customer account takeover risk |
| Infostealer hit older than 1 year, account already reset | No (digest) | Low | Already handled; confirm once |
| Employee email in a new third-party breach with passwords | Yes | Medium | Password reuse risk |
| Employee email in an old breach already processed | No | Info | Already handled |
| Company name on a ransomware leak site | Yes, immediately | Critical | Possible breach; IR lead + management |
| Supplier or customer on a leak site | Yes | High | Third-party risk; your data may be included |
| New lookalike domain certificate | Yes | Medium | Likely phishing preparation |
| Source API failed / returned nothing unusual | Yes (ops alert) | Low | Check reliability |

## Privacy and legal rules

!!! warning "Non-negotiable handling rules"
    - **Never store plaintext passwords** in tickets, chat, spreadsheets or logs. Store only "password exposed: yes" and, if needed, the first and last character plus length (`P******1 (12)`).
    - **Mask tokens and cookies**: keep at most the first 4 characters (`eyJh...[masked]`).
    - **Do not buy stolen data** or log in to criminal forums yourself. Use providers who carry that legal risk.
    - **Do not test leaked passwords** against live systems. Force a reset instead.
    - Check only accounts the organisation owns. Personal emails of staff only with written consent.
    - Follow your data protection law: minimise, restrict access to the SOC, set retention (for example 12 months), record the processing purpose.
    - Get legal review of the monitoring programme once, before launch.

## Response workflow

```text
NEW FINDING
   |
   v
L1: validate (is it our account/asset? is it new?) ---- no ---> close as not relevant
   |
   yes
   v
L1: open ticket, masked evidence, severity from table above
   |
   v
L2: account action within SLA
     - reset password, revoke all sessions and refresh tokens
     - check MFA methods for new/unknown devices
     - review sign-in logs 30 days back (new IPs, countries, impossible travel)
   |
   +-- stealer hit? --> find infected device, run infostealer playbook
   +-- suspicious logins found? --> incident, IR lifecycle
   +-- leak site mention? --> IR lead + legal + management, ransomware procedure
   |
   v
L2: notify user (plain language, what to do on personal devices)
   |
   v
Close with root cause (reuse / stealer / phishing / third party) for metrics
```

| Severity | Account action SLA | Who is told |
|---|---|---|
| Critical | 1 hour | SOC manager, IR lead, identity team |
| High | 4 hours | SOC manager, identity team |
| Medium | 2 business days | User, identity team |

Sign-in log check example (KQL, adapt field names to your identity provider):

```kql
SigninLogs
| where UserPrincipalName =~ "j.doe@example.com"
| where TimeGenerated > ago(30d)
| summarize count(), Countries=make_set(Location), IPs=make_set(IPAddress) by AppDisplayName, ResultType
```

## Worked example

```text
06:00  Daily check: infostealer lookup for example.com: employees 3 (yesterday 2)  -> NEW
06:05  Ticket TI-0412 (Critical): compromised 2026-10-24, URLs include sso.example.com, vpn.example.com
08:05  L1 validates: account j.doe@example.com active; no earlier ticket
08:20  L2: password reset, sessions revoked, MFA devices reviewed (1 unknown device removed)
08:40  Sign-in logs: 2 successful VPN logins from unfamiliar country on 2026-10-25 -> incident IR-0098
09:00  Infostealer playbook: user's home PC used for webmail; work laptop EDR scan clean
10:30  User briefed; personal device cleaned by user; browser password saving disabled by policy
Root cause: infostealer on personal device + saved browser passwords
```

## Metrics

| Metric | Target |
|---|---|
| Daily check success rate | 100% (alert on failure) |
| Median time new finding -> account reset (critical) | < 1 hour |
| Exposed accounts reset within SLA | > 95% |
| Repeat exposures of the same user in 12 months | Falling |
| Findings by root cause (stealer / reuse / phishing / third party) | Tracked monthly to steer awareness |

## Checklist

- [ ] Watch lists for domains, login URLs, brand, suppliers, customers
- [ ] Domain verified with breach service; API keys in secrets store
- [ ] Daily check with state diff and failure alert
- [ ] Masking rules enforced in code
- [ ] Legal review of the programme done
- [ ] Response SLAs agreed with identity team
- [ ] Metrics in monthly report

## Related pages

- [Credential leak / dark web playbook](../04-playbooks/credential-leak-dark-web.md)
- [Infostealer malware playbook](../04-playbooks/malware-infostealer.md)
- [Phishing playbook](../04-playbooks/phishing.md)
- [Incident response lifecycle](../03-incident-response/ir-lifecycle.md)
- [Automation catalogue](../07-automation-soar/automation-catalog.md)
- [Employee security guide](../08-security-policies/employee-security-guide.md)
