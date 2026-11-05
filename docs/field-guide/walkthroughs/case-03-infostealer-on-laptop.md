# Case 03: Infostealer on a Laptop

An EDR alert on a developer's laptop. The malware ran for seconds, but in those seconds an infostealer can take every saved password and session. This case is about proving it ran, working out what it stole, and killing the stolen access before it is used.

!!! abstract "At a glance"
    - Attack: infostealer malware
    - Starts from: an EDR detection
    - Playbook: [Malware and infostealer](../../04-playbooks/malware-infostealer.md)

## The alert

```text
14:22 UTC. EDR alert on laptop DEV-L-0471 (user: p.ramirez, a developer).
Detection: "Credential theft behaviour", action: DETECTED (not blocked).
Process: setup_v2.exe, run from C:\Users\p.ramirez\Downloads\
```

**Stop. The action says DETECTED, not BLOCKED. What does that mean for you?** Write it down.

## L1 triage

| Check | Finding |
|---|---|
| Blocked or detected? | Only detected: assume it ran until proven otherwise |
| Did it execute? | Yes: child processes and network connections after the alert time |
| Is it an infostealer? | It read browser credential stores and posted to a Telegram API endpoint |
| Whose laptop? | A developer: high value (cloud keys, source code, SSH keys) |
| How did it arrive? | Browser download from a cracked-software site |
| Same file on other hosts? | Hash search: only DEV-L-0471 |

A developer's machine plus confirmed credential theft is a high-severity case. Developers hold the most valuable secrets.

### Non-browser process reading credential stores

=== "Microsoft Sentinel KQL"

    ```kql
    DeviceFileEvents
    | where Timestamp > ago(1d) and DeviceName == "DEV-L-0471"
    | where FileName in~ ("Login Data","Cookies","Local State","key4.db","logins.json")
    | where InitiatingProcessFileName !in~ ("chrome.exe","msedge.exe","firefox.exe","brave.exe")
    | project Timestamp, InitiatingProcessFileName, InitiatingProcessFolderPath, FileName
    ```

## Escalation to L2

```text
Escalated 14:34 UTC by L1.
Verdict: infostealer executed on DEV-L-0471 (developer p.ramirez). Read Chrome and Edge
credential stores and posted to api.telegram.org. Single host.
Asks: isolate host; treat all credentials and sessions on it as stolen; developer secrets
(cloud keys, SSH) need rotation.
```

## L2 investigation

An infostealer steals and leaves; the damage is the stolen data being used elsewhere. Scope what was on the machine and watch for the stolen access being used.

| Time (UTC) | Finding | Source |
|---|---|---|
| 14:19 | setup_v2.exe launched from Downloads | EDR, Sysmon 1 |
| 14:19 | Read Chrome and Edge Login Data, Cookies, Local State | EDR file events |
| 14:20 | Outbound POST to api.telegram.org (data exfiltration) | EDR network, proxy |
| 14:20 | Accessed C:\Users\p.ramirez\.aws\credentials and an SSH private key | EDR file events |
| 14:22 | EDR raised the alert | EDR |
| 15:05 | A cloud API call using p.ramirez's AWS key from a new IP | Cloud audit (CloudTrail) |

The last line is the real danger: the stolen cloud key was used within the hour.

## Containment (with approvals)

| Action | Owner | Approval |
|---|---|---|
| Isolate DEV-L-0471 through the EDR | SOC | Pre-approved for confirmed malware on a laptop |
| Deactivate p.ramirez's AWS access key; revoke role sessions | Cloud team | L2, escalated to P1 on the cloud key use |
| Rotate the SSH key and any secrets on the laptop | p.ramirez with the cloud team | L2 |
| Reset passwords and revoke sessions for all accounts saved in the browser | Identity team and user | L2: cookies bypass MFA, so revoke sessions too |
| Block the hash and the download URL; add Telegram-API-from-non-chat detection | SOC | L2 |

The cloud team confirmed the stolen key had created no new resources before it was killed; the attacker was cut off during reconnaissance.

## Outcome

The malware ran, but fast containment and, crucially, rotating the developer's cloud and SSH secrets stopped the stolen credentials from being used for anything beyond one reconnaissance call. The browser-saved passwords and the cloud key were the real loss, not the laptop.

## Lessons learned

- [ ] The EDR only detected, it did not block: move the policy from detect to prevent for this class.
- [ ] Developers should not store cloud keys in plaintext files or passwords in the browser; move to short-lived credentials and a secrets manager.
- [ ] Detection added: non-browser process reading credential stores, and Telegram or Discord API traffic from non-chat processes.
- [ ] Block software installation from user folders and cracked-software sites.

## Quiz

1. Why was resetting passwords not enough on its own?
2. Why is a developer's laptop higher severity than a typical user's?
3. What single later log line turned this from "malware ran" into "P1"?

??? note "Answers"
    1. The stealer took session cookies, which bypass the password and MFA; sessions and tokens had to be revoked, and secrets like the cloud and SSH keys rotated.
    2. Developers hold high-value secrets: cloud keys, source code, SSH keys, CI tokens. Stealing those can lead straight to production.
    3. The cloud API call at 15:05 using the stolen AWS key from a new IP.

## Related pages

- [Malware and infostealer playbook](../../04-playbooks/malware-infostealer.md)
- [Cloud account compromise playbook](../../04-playbooks/cloud-account-compromise.md)
- [Credential leak playbook](../../04-playbooks/credential-leak-dark-web.md)
