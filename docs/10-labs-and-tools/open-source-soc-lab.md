# Open-Source SOC Lab

How to build a working SOC on your own machine with free tools, so you can practise triage, write and test detections, and break things safely. The best analysts have stood up their own stack and watched an attack flow through it end to end.

!!! abstract "At a glance"
    - Audience: analysts and engineers who learn by doing
    - Time to read: 15 minutes
    - Outcome: a plan for a lab from a single SIEM to a full stack, with safe attack practice

!!! danger "Lab safety first"
    Keep the lab on an isolated or separate virtual network. Anything that generates attacks (Atomic Red Team, Caldera, malware samples) must never reach production or the open internet. Use host-only or internal networking, snapshots you can roll back, and disposable virtual machines. Never run a real malware sample outside a sandbox with no network path you care about.

## What you need

| Resource | Minimum | Comfortable |
|---|---|---|
| A host machine | 16 GB RAM, 4 cores, 100 GB free | 32 GB RAM, 8 cores, SSD |
| Virtualisation | VirtualBox, VMware, Proxmox, or Docker | Any of these |
| Target machines | One Windows and one Linux VM to generate logs | A small Windows domain plus Linux hosts |
| Patience | A weekend to get the basics flowing | - |

You do not need all of this to start. A single SIEM VM collecting logs from your own laptop teaches a lot.

## Build it in phases

Each phase works on its own. Stop whenever you have enough for what you want to practise.

### Phase 1: a SIEM and one log source

- [ ] Stand up a SIEM. Wazuh (single-node Docker) is the fastest free start and includes agents.
- [ ] Install the agent on one Windows and one Linux VM.
- [ ] Confirm logs arrive and you can search them.
- [ ] Log in to the dashboard and find the alerts view.

You now have the core loop: a log source, a SIEM, and alerts. Most learning happens here.

### Phase 2: endpoint visibility

- [ ] Add Sysmon on Windows with a good configuration (a community config gives rich process, network and file events).
- [ ] Add osquery on Windows and Linux for live queries across hosts.
- [ ] Confirm process-creation and network events reach the SIEM.

Now you can see what processes do, which is where most detection lives.

### Phase 3: network sensors

- [ ] Add Zeek for network metadata (connections, DNS, HTTP) and Suricata for signature alerts.
- [ ] Feed their logs into the SIEM.
- [ ] Generate some traffic and watch the DNS and connection logs appear.

### Phase 4: case management and automation

- [ ] Add a case tool (TheHive or IRIS) so alerts become cases.
- [ ] Add an automation tool (Shuffle, n8n) and build one enrichment workflow: on an alert, look up an IP and attach the result.
- [ ] Wire the SIEM to open a case automatically on a high-severity alert.

### Phase 5: threat intel and forensics

- [ ] Add MISP or OpenCTI for indicators; load a free feed as a watchlist.
- [ ] Add Velociraptor for live response and triage collection.
- [ ] Practise pulling a triage collection from a VM.

At the end you have a full small SOC: collection, detection, cases, automation, intel and forensics, all free.

## Generate attacks to practise on

A SOC with no attacks is boring and teaches little. Generate safe, known attacks and watch them flow through.

| Tool | What it does | Safety |
|---|---|---|
| Atomic Red Team | Runs single ATT&CK techniques | Small, documented, has cleanup; test VMs only |
| MITRE Caldera | Chained adversary emulation with agents | Test network only |
| Infection Monkey | Lateral movement and segmentation testing | Isolated lab only |
| Your own hands | Create a new admin, run an encoded command, exfiltrate a file to a test endpoint | You control it exactly |

```powershell
# On an isolated Windows test VM, with Atomic Red Team installed:
Invoke-AtomicTest T1059.001 -TestNumbers 1 -ShowDetailsBrief   # look first
Invoke-AtomicTest T1059.001 -TestNumbers 1                      # run it
# now go to the SIEM and see if it fired, then:
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
```

## The learning loop

The point of the lab is this loop, run again and again:

```text
Run a technique -> did a detection fire?
  -> if yes: investigate it as if it were real, write the case notes
  -> if no:  find out why (no log source? no rule?) -> fix it -> run again
```

- [ ] Run an attack technique on a test VM.
- [ ] Check whether anything fired in the SIEM.
- [ ] If it fired, investigate it like a real case: pivot, build a timeline, decide a verdict.
- [ ] If it did not fire, work out whether you lack the log source or the detection, then fix it.
- [ ] Write a Sigma rule for it and test it ([Testing and tuning](../05-detection-engineering/testing-and-tuning.md)).

This single loop builds triage skill, detection skill and tool skill at once.

## Starter exercises

- [ ] Exercise 1: create a new local admin on the Windows VM. Find the event, write the alert.
- [ ] Exercise 2: run an encoded PowerShell command. Trace it in Sysmon and build the timeline.
- [ ] Exercise 3: copy a file to a test endpoint over the network. Detect the transfer.
- [ ] Exercise 4: simulate failed logins then a success. Write the success-after-failures detection.
- [ ] Exercise 5: request a secret file over HTTP against a test web server. Tell a 200 hit from a 404.

Each maps to a [walkthrough](../field-guide/walkthroughs/index.md); compare your work with the worked case.

## Related pages

- [Tool selection guide](tool-selection-guide.md)
- [Useful resources](useful-resources.md)
- [Technology stack](../01-build-a-soc/technology-stack.md)
- [Testing and tuning](../05-detection-engineering/testing-and-tuning.md)
- [Case walkthroughs](../field-guide/walkthroughs/index.md)
