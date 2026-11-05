# T05: Network Security Monitoring

The network sees what the endpoint sometimes hides: who talked to whom, what was asked of DNS, where data went. This module teaches the free tools and the signals that matter.

!!! abstract "At a glance"
    - Level: L2
    - Time: 6 to 8 hours with labs
    - Outcome: you can read network metadata and spot command and control, tunnelling and exfiltration

## Learning objectives

- [ ] Explain the difference between full packet capture, flow data and metadata, and when each is used.
- [ ] Use Zeek to turn traffic into readable logs (connections, DNS, HTTP).
- [ ] Use Suricata for signature-based alerts.
- [ ] Spot beaconing, DNS tunnelling and large outbound transfers.
- [ ] Read proxy and DNS logs for investigation.

## Lessons

1. **Levels of network visibility.** Packet capture (everything, expensive), flow or NetFlow (who to whom, cheap), metadata (Zeek: structured facts about each connection).
2. **Zeek.** The logs it produces (conn, dns, http, ssl) and how to read them.
3. **Suricata.** Signature alerts, when they help and when they are noise.
4. **Command and control.** Beaconing: regular callbacks to one destination; how to spot the rhythm.
5. **DNS as a signal.** Tunnelling (long, high-entropy subdomains), newly registered domains, DNS to unusual resolvers.
6. **Exfiltration on the wire.** Large outbound transfers, uploads to personal cloud, odd protocols.

## Lab

- [ ] Run Zeek against a sample PCAP or your lab traffic.
- [ ] Read the `conn.log` and `dns.log`; find the top talkers and the most-queried domains.
- [ ] Generate steady callbacks from a test host to one destination; find the beaconing pattern.
- [ ] Simulate DNS tunnelling (long subdomains to one domain) and detect it.

### DNS tunnelling check (Zeek)

```bash
zeek-cut query < dns.log | awk -F. '{print $(NF-1)"."$NF, length($1)}' \
  | awk '$2>30 {c[$1]++} END {for (d in c) if (c[d]>200) print c[d], d}' | sort -rn | head
```

## Self-check

1. When would you use flow data instead of full packet capture?
2. What does beaconing look like in connection logs?
3. Why is a long, random-looking subdomain a red flag?

??? note "Answers"
    1. When you need to know who talked to whom at scale and cheaply, without the storage and privacy cost of capturing full packet contents.
    2. Regular, repeated connections to the same destination at a steady interval, often small and persistent.
    3. It can be data encoded into DNS queries (tunnelling) to smuggle information out or run command and control through DNS, which many defences do not inspect.

## Links to the handbook and kit

- [Data exfiltration playbook](../../04-playbooks/data-exfiltration.md)
- [Threat hunting](../../02-daily-operations/threat-hunting.md)
- [Investigation cheat sheet](../../field-guide/investigation-cheatsheet.md)

## Next module

[T06 Email, Identity and Cloud Security](../t06-email-identity-cloud/index.md).
