---
id: SOP-20
title: Endpoint Agent Deployment and Health
owner: SOC Engineer
audience: SOC engineers, endpoint team
review: Every 12 months
summary: How to deploy the endpoint agent everywhere it should be, and keep it healthy, so coverage is complete and a missing or disabled agent is noticed fast.
---
## 1. Purpose

An EDR is only as good as its coverage. A host without the agent, or with a disabled one, is a blind spot an attacker can hide in. This procedure keeps the agent deployed everywhere it should be and healthy, and makes a missing agent an alert, not a surprise.

> WARNING: Attackers disable or uninstall the endpoint agent to go dark. A sudden drop in an agent's reporting is not just an IT glitch; treat it as a possible security event, as with any silent source (SOP-12).

## 2. Scope

The endpoint security agent (EDR, and Sysmon or osquery where used) on all covered endpoints and servers for [ORGANISATION].

## 3. Coverage

- [ ] Maintain a list of all hosts that should run the agent, from the asset inventory.
- [ ] Compare the agent fleet against that list regularly; every gap is either a missing agent or an unmanaged host.
- [ ] Include servers, cloud instances and new builds, not just laptops.

## 4. Deployment

1. Deploy the agent through the standard method (management tool, image, MDM or UEM).
2. Bake the agent into the standard build so new hosts have it from the start.
3. Confirm the agent reports in and shows healthy after deployment.
4. Record the host and agent in the inventory.

## 5. Health

Check agent health as part of the daily routine (SOP-01):

- [ ] Agents reporting versus the expected total; investigate the gap.
- [ ] Agents that stopped reporting (disconnected), and for how long.
- [ ] Agents on old versions that need updating.
- [ ] Agents in a degraded or tamper-alert state.

## 6. When an agent goes missing or silent

1. Confirm the host should have the agent and is actually online.
2. Check for a benign cause: the host is off, a planned rebuild, a known maintenance.
3. If there is no benign explanation, treat it as a possible security event: could the agent have been disabled by an attacker? Investigate the host.
4. Restore the agent and confirm it reports healthy; assess any gap in coverage.

> NOTE: Keep a short list of hosts that legitimately have no agent (appliances, unsupported systems) with the reason, so "no agent" there is expected and does not hide a real gap. Everything else should be covered or explained.

## 7. Records

Keep the agent inventory current: which hosts have the agent, versions, health, and the list of accepted exceptions.

## 8. Review

Reviewed every 12 months.
