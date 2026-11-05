# Case 06: Cloud Key Leak and Cryptomining

A billing alert about unexpected GPU instances leads to a leaked access key, a cryptominer, and an attacker who tried to stay in. This case is about scoping a cloud compromise: every region, every identity the attacker created, and whether logging was ever turned off.

!!! abstract "At a glance"
    - Attack: leaked cloud access key used for cryptomining and persistence
    - Starts from: a billing or threat-detection alert
    - Playbook: [Cloud account compromise](../../04-playbooks/cloud-account-compromise.md)

## The alert

```text
06:40 UTC. Two alerts within minutes:
- Billing anomaly: compute spend up sharply overnight.
- Cloud threat detection (GuardDuty-style): "CryptoCurrency:EC2/BitcoinTool" and
  "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration".
Several large GPU instances started in a region the company never uses.
```

**Stop. Cloud attacks use the API, not malware. What do you scope first?** Write it down.

## L1 triage

| Check | Finding |
|---|---|
| What is running and costing money? | 40 large GPU instances in an unused region, mining |
| Which identity started them? | An access key belonging to a CI/CD service user |
| Does the owner recognise it? | Asked the platform team by chat (not email): no, unexpected |
| Where did the key leak? | Secret-scanning alert: the key was committed to a public code repository two days ago |
| Is logging still on? | To be confirmed across all regions |

A leaked key is often used within minutes of being published. This is active and expensive.

## Escalation to L2

```text
Escalated 06:55 UTC by L1, raised to P1.
Verdict: leaked CI/CD access key used to run cryptomining in an unused region. Key was
committed to a public repo 2 days ago.
Asks: scope everything the key did in ALL regions; find any identities or persistence the
attacker created; confirm logging was not disabled; contain the key.
```

## L2 investigation

In the cloud the attacker uses the same API calls your engineers do. Scope by the key and by any identity it created, across every region.

| Time (UTC) | Finding | Source |
|---|---|---|
| 2 days ago | Access key committed to a public repo | Secret scanning |
| 2 days ago, +6 min | First use of the key: GetCallerIdentity, then List and Describe calls (reconnaissance) | Cloud audit log |
| 2 days ago | CreateUser and CreateAccessKey: the attacker made a second identity to persist | Cloud audit log |
| Overnight | 40 GPU instances launched in an unused region | Cloud audit log |
| Overnight | GetObject calls against a storage bucket with customer exports | Storage access logs |
| Throughout | No StopLogging or DeleteTrail: logging stayed on | Cloud audit log |

Two things stand out: the attacker created a second identity (so killing the leaked key alone would not eject them), and they listed a customer-data bucket (a possible data exposure, not just mining).

### Everything the key did, all regions

=== "Splunk SPL"

    ```spl
    index=cloudtrail userIdentity.accessKeyId="AKIAEXAMPLEKEY" earliest=-7d
    | stats count values(eventName) as actions values(awsRegion) as regions min(_time) as first by sourceIPAddress
    ```

=== "Microsoft Sentinel KQL"

    ```kql
    AWSCloudTrail
    | where TimeGenerated > ago(7d) and UserIdentityAccessKeyId == "AKIAEXAMPLEKEY"
    | summarize Count = count(), Actions = make_set(EventName, 100), Regions = make_set(AWSRegion) by SourceIpAddress
    ```

### High-risk events across all identities

=== "Microsoft Sentinel KQL"

    ```kql
    AWSCloudTrail
    | where EventName in ("CreateUser","CreateAccessKey","AttachUserPolicy","StopLogging","DeleteTrail","PutBucketPolicy")
    | where UserIdentityType != "AWSService"
    | project TimeGenerated, UserIdentityArn, SourceIpAddress, EventName, AWSRegion
    ```

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Deactivate the leaked key (do not delete yet; keep it for log searches) | Cloud team | P1 pre-approved |
| Delete the attacker-created user and its key | Cloud team | L2 |
| Revoke active role sessions so stolen temporary credentials expire | Cloud team | L2 |
| Stop and terminate the mining instances (after noting their details) | Cloud team | L2 |
| Remove any public access added to the customer bucket; check access logs for downloads | Cloud team | L2, data exposure assessment |
| Rotate every secret the key could read; remove the key from the repo history; enable push protection | Platform team | L2 |

The storage logs showed the bucket was listed but no large downloads completed before containment; legal was still informed because customer data was reachable.

## Outcome

The leaked key gave the attacker an easy way in, and they immediately built a second identity to persist and started mining. Scoping every region and spotting the attacker-created user is what made the eradication complete; killing only the leaked key would have left the second identity active. Logging was never disabled, which is why the whole story was recoverable.

## Lessons learned

- [ ] Replace long-lived access keys with short-lived credentials (OIDC federation for CI/CD). A key that cannot leak cannot be leaked.
- [ ] Enable secret scanning and push protection on all repositories so a key is blocked before it is ever public.
- [ ] Protect audit logging from being disabled, and alert on StopLogging and DeleteTrail.
- [ ] Detection added: key use from a new ASN, activity in unused regions, GPU instance launches, new IAM users and keys, and GetCallerIdentity from a new IP (attackers test a key with it first).
- [ ] Set a billing alarm; the spend anomaly was a real detection here.

## Quiz

1. Why was deactivating the leaked key not enough to eject the attacker?
2. Why scope every region, not just the one with the mining instances?
3. What made this more than a cryptomining case?

??? note "Answers"
    1. The attacker created a second IAM user and key for persistence. Killing the leaked key leaves that second identity active; you must find and remove everything the attacker created.
    2. Cloud attackers operate in any region, and often start resources in unused ones precisely because nobody watches them. Reconnaissance and persistence can be spread across regions.
    3. The attacker listed a storage bucket containing customer exports, making it a potential data exposure, which brings in legal and notification duties, not just a cost problem.

## Related pages

- [Cloud account compromise playbook](../../04-playbooks/cloud-account-compromise.md)
- [Data exfiltration playbook](../../04-playbooks/data-exfiltration.md)
- [Credential leak playbook](../../04-playbooks/credential-leak-dark-web.md)
