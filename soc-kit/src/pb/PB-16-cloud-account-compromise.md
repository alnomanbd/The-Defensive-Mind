---
id: PB-16
title: Cloud Account Compromise
owner: SOC lead with the cloud platform team
audience: SOC analyst L2 / L3, cloud platform team
review: Every 12 months, and after every real incident that used this playbook
summary: "How to respond when an attacker controls a cloud identity or credential in AWS, Microsoft Azure or Google Cloud: a leaked access key, a stolen console session, a compromised CI/CD token, or an abused workload role. Cloud attacks move fast: a leaked key is often used within minutes of being published."
---
## Playbook card

| Field | Value |
|:---|:---|
| **ID** | PB-16 |
| **Default severity** | P2 High (see Severity and SLA) |
| **Escalate to Critical when** | Administrator or organisation-level access, production data accessed, resources deleted, new identities or trust relationships created, or large unexpected spend |
| **MITRE ATT&CK** | T1078.004 Valid Accounts: Cloud Accounts, T1552.001 Credentials in Files, T1552.005 Cloud Instance Metadata API, T1098.001 Additional Cloud Credentials, T1136.003 Create Cloud Account, T1580 Cloud Infrastructure Discovery, T1530 Data from Cloud Storage, T1496 Resource Hijacking, T1562.008 Disable or Modify Cloud Logs |
| **Typical alerts** | GuardDuty, Defender for Cloud or Security Command Center finding; access key used from a new country or ASN; secret scanning alert on a public repository; `CreateAccessKey`, `CreateUser`, `AttachUserPolicy` by an unusual identity; `StopLogging`; GPU instances started in an unused region; billing anomaly |
| **Owner** | SOC lead with the cloud platform team |
| **Last reviewed** | 2026-11-05 |

## 1. Summary

In the cloud, **identity is the perimeter**. An attacker with a valid key does not need malware; they use the same API calls as your engineers. Typical paths in: access keys committed to a public repository, keys in a laptop hit by an infostealer, phished console logins without phishing-resistant MFA, CI/CD secrets, and server-side request forgery (SSRF) reading the instance metadata service. Typical goals: cryptomining, data theft from storage buckets, ransom by deleting data and backups, and staying in by creating new users, keys or cross-account roles. Success for the defender: the credential is dead within minutes, every attacker-created resource and identity is found in all regions, and logging was never off long enough to lose the story.

## 2. Triggers and detection

| Signal | AWS | Azure | Google Cloud |
|:---|:---|:---|:---|
| Key or session used from unusual place | GuardDuty `UnauthorizedAccess:IAMUser/*`, CloudTrail `sourceIPAddress` | Entra ID risky sign-in, Defender for Cloud | Security Command Center (SCC) anomalous IAM grant |
| New identities and keys | `CreateUser`, `CreateAccessKey`, `CreateLoginProfile` | New service principal, new client secret | `CreateServiceAccountKey` |
| Privilege change | `AttachUserPolicy`, `PutRolePolicy`, `UpdateAssumeRolePolicy` | Role assignment Owner or User Access Administrator | `SetIamPolicy` with `roles/owner` |
| Logging tampering | `StopLogging`, `DeleteTrail`, `PutEventSelectors` | Diagnostic setting deleted | Log sink deleted |
| Discovery burst | Many `List*`, `Describe*`, `GetCallerIdentity` from one key | Many reads across subscriptions | Many `list` calls |
| Resource hijacking | `RunInstances` with GPU types in unused regions | New VMs or scale sets | New Compute Engine instances |
| Data access | `GetObject` volume spike, `PutBucketPolicy` making a bucket public | Storage account SAS created, public access | Bucket IAM `allUsers` |
| Leak found | Secret scanning on GitHub or GitLab, AWS notification email about an exposed key | Same | Same |

**Common false positives:** an engineer travelling or using a new VPN, a new automation or Terraform pipeline, a scheduled cost-saving job, a red team or cloud security posture tool (CSPM) scanning with read-only roles.

## 3. Triage (first 15 minutes)

- [ ] Which credential: IAM user key, role session, console user, service principal, service account key?
- [ ] Who owns it, and do they recognise the activity? Ask them directly (phone or chat), not by email to a possibly compromised account.
- [ ] What permissions does it have? Admin or wide `*` permissions raise severity.
- [ ] What has it done in the last 24 hours, in **all regions**?
- [ ] Is logging still on in every region and account?
- [ ] Is anything running that costs money (GPU instances, many VMs)?

Decision: owner confirms and activity matches a known change, close with a note; unknown activity with read-only effect, P2, contain the credential; writes, new identities, logging changes, data access or high spend, P1, contain and call the cloud team lead.

## 4. Investigation

| Question | Where to look |
|:---|:---|
| Where did the credential leak? | Public repositories (secret scanning), CI logs, laptop infostealer logs, SSRF evidence in web logs |
| First malicious use? | Cloud audit logs (CloudTrail, Azure Activity and Entra audit, Google Cloud Audit Logs) filtered by key ID or principal |
| Everything the attacker created or changed? | All write events by the principal and by any identity the attacker created |
| Persistence? | New users, keys, login profiles, roles with external trust, OAuth apps, Lambda or Functions, EC2 key pairs, SSH keys in metadata |
| Data accessed? | S3 data events, storage logs, database snapshots shared or copied, `GetSecretValue` |
| Other accounts or subscriptions? | `AssumeRole` chains, cross-account trusts, management group access |

### Queries: everything one access key or principal did

**Splunk SPL**


```spl
index=aws sourcetype=aws:cloudtrail userIdentity.accessKeyId="AKIAEXAMPLEKEY123"
| stats count min(_time) as first max(_time) as last values(eventName) as actions values(awsRegion) as regions by sourceIPAddress, userAgent
| convert ctime(first) ctime(last)
```

**Microsoft Sentinel KQL**


```kql
AWSCloudTrail
| where TimeGenerated > ago(14d)
| where UserIdentityAccessKeyId == "AKIAEXAMPLEKEY123"
| summarize Count = count(), First = min(TimeGenerated), Last = max(TimeGenerated),
    Actions = make_set(EventName, 100), Regions = make_set(AWSRegion) by SourceIpAddress, UserAgent
```
```kql
// Azure: role assignments and new credentials in the last 7 days
AzureActivity
| where TimeGenerated > ago(7d)
| where OperationNameValue has_any ("roleAssignments/write", "Microsoft.Authorization/elevateAccess")
| project TimeGenerated, Caller, CallerIpAddress, OperationNameValue, ResourceGroup
```

**Elastic**


```text
event.dataset : "aws.cloudtrail" and aws.cloudtrail.user_identity.access_key_id : "AKIAEXAMPLEKEY123"
(table: event.action, cloud.region, source.ip, user_agent.original)
```

**IBM QRadar AQL**


```sql
SELECT sourceip, username, QIDNAME(qid) AS action, "AWS Region" AS region, COUNT(*) AS n
FROM events
WHERE LOGSOURCETYPENAME(devicetype) ILIKE '%CloudTrail%'
  AND UTF8(payload) ILIKE '%AKIAEXAMPLEKEY123%'
GROUP BY sourceip, username, action, region LAST 14 DAYS
```

**Wazuh**


```text
data.aws.userIdentity.accessKeyId:"AKIAEXAMPLEKEY123"
```

**AWS CLI**


```bash
# Who is the key, and what did it do (run per region, management events only)
aws iam list-access-keys --user-name suspected-user
aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIAEXAMPLEKEY123 \
  --max-results 50 --region us-east-1
# Persistence check
aws iam list-users --query 'Users[?CreateDate>=`2026-11-01`]'
aws iam list-roles --query 'Roles[?CreateDate>=`2026-11-01`].[RoleName,AssumeRolePolicyDocument]'
```

High-risk events to alert on across all identities:

**Microsoft Sentinel KQL**


```kql
AWSCloudTrail
| where EventName in ("StopLogging","DeleteTrail","CreateUser","CreateAccessKey","CreateLoginProfile",
    "AttachUserPolicy","PutUserPolicy","UpdateAssumeRolePolicy","PutBucketPolicy","DeleteBucketPolicy","PutBucketAcl")
| where UserIdentityType != "AWSService"
| project TimeGenerated, UserIdentityArn, SourceIpAddress, EventName, AWSRegion, RequestParameters
```

**Splunk SPL**


```spl
index=aws sourcetype=aws:cloudtrail eventName IN ("StopLogging","DeleteTrail","CreateUser","CreateAccessKey","CreateLoginProfile","AttachUserPolicy","PutUserPolicy","UpdateAssumeRolePolicy","PutBucketPolicy","PutBucketAcl")
| table _time userIdentity.arn sourceIPAddress eventName awsRegion
```

## 5. Containment

| Action | Owner | Notes / risk |
|:---|:---|:---|
| Deactivate (do not delete yet) the leaked access key | Cloud team | Deactivating is reversible and keeps the key ID for log searches; check which apps use it first if possible |
| Revoke active role sessions (AWS: "Revoke active sessions" adds a deny for tokens issued before now) | Cloud team | Stolen temporary credentials stay valid until expiry otherwise |
| Disable console login, reset password and MFA for compromised users | Identity team | Federated users: revoke in the identity provider |
| Azure and Google Cloud: remove secrets or keys of the service principal or service account; revoke refresh tokens | Cloud team | Check for multiple secrets |
| Delete or deactivate every attacker-created user, key, role and trust | Cloud team | Record each before removal |
| Stop or delete attacker resources (mining instances) after snapshots if needed | Cloud team | Spend stops only when resources stop |
| Restore logging and protect it (organisation trail, deny `StopLogging` by policy) | Cloud team | Logging gaps hide what happened |
| Remove public access added to buckets and storage | Cloud team | Then check access logs for downloads |
| Apply a deny policy or service control policy (SCP) to the compromised identity or account | Cloud security | Fast, wide stop when scope is unclear |

## 6. Eradication and recovery

- [ ] Rotate every secret the compromised identity could read (Secrets Manager, Key Vault, Secret Manager, parameter stores).
- [ ] Replace long-lived access keys with roles and short-lived credentials (OIDC federation for CI/CD).
- [ ] Remove the leak source: delete the secret from repository history, rotate the CI token, fix the SSRF and enforce IMDSv2.
- [ ] Enable secret scanning and push protection on all repositories.
- [ ] Ask the cloud provider for a billing adjustment for fraudulent usage (open a support case quickly).
- [ ] Monitor the account for 30 days: new identities, keys, regions and spend anomalies.

## 7. Communication

| Who | When | By whom |
|:---|:---|:---|
| Credential owner and cloud platform team | Immediately | Analyst |
| SOC lead | Any confirmed misuse | Analyst |
| CISO | Admin access, data access, destruction, or large spend | SOC lead |
| Finance | Unexpected spend over the agreed threshold | Cloud team lead |
| Legal and privacy | Personal or customer data in accessed storage | CISO |
| Cloud provider support | Billing adjustment, abuse reports, help with forensics | Cloud team |

See Escalation and Communication.

## 8. Evidence to keep

- Cloud audit logs for all regions and accounts for the incident window, exported to separate storage before retention removes them.
- IAM state snapshots: users, keys, roles, policies before and after cleanup.
- Disk snapshots of attacker-created or compromised instances.
- Storage access logs and data event logs.
- The leak source (repository commit URL, CI log) captured with timestamps.

Follow Evidence Handling.

## 9. Lessons learned

For the Post-Incident Review:

- Why did a long-lived key with wide permissions exist?
- Were data events and all regions logged? Was the trail protected from deletion?
- How long between the key's first misuse and the alert? Between the alert and deactivation?
- Was there a billing alarm, and did anyone receive it?

Detections to add or tune: the high-risk event list above, key use from new ASN, activity in unused regions, GPU instance launches, public bucket policy changes, `GetCallerIdentity` from a new IP (attackers often check the key with it first).


## Related documents

- Account Compromise, Data Exfiltration, Credential Leak / Dark Web
- Tabletop Exercises (scenario: cloud keys leaked in a public repository)
- Evidence Handling
