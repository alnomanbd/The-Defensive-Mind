# Incident Reporting Policy

A ready-to-adapt policy for how anyone reports something suspicious, quickly and without fear of blame. Most incidents are first noticed by an ordinary employee: a strange email, a lost laptop, a mistake. Whether they report it in minutes or hide it for days decides how bad the incident gets.

!!! abstract "At a glance"
    - Audience: all staff (as the rule), security, HR, managers
    - Time to read: 6 minutes
    - Outcome: one clear, blameless way for anyone to report a security concern

---

## Policy: Security Incident Reporting

**Purpose.** To make sure every suspected security problem at `[ORGANISATION]` is reported quickly to the people who can act on it, so it can be contained before it grows.

**Scope.** Everyone: all staff, contractors and anyone working with `[ORGANISATION]` systems or data.

### Statements

1. **Report anything suspicious**, even if you are not sure it is real. A false alarm costs minutes; an unreported incident can cost the organisation dearly.
2. **Report it fast.** Minutes matter. Do not wait to be certain, to investigate yourself, or until the next working day for anything urgent.
3. **How to report:** `[contact method: for example, email security@ORGANISATION, call the service desk on NUMBER, or use the REPORT button in email]`. For anything urgent or out of hours: `[urgent contact]`.
4. **What counts** as something to report:
    - A suspicious or phishing email, or one you clicked or replied to.
    - A lost or stolen laptop, phone or access card.
    - A password you think someone else may know, or that you entered on a suspicious site.
    - Unusual computer behaviour (unexpected programs, files encrypted or renamed, pop-ups).
    - Data sent to the wrong person, or a document shared too widely by mistake.
    - Anyone asking for passwords, payments or data in an unusual or urgent way.
    - Anything else that feels wrong.
5. **If you think you made a mistake** (clicked a link, entered a password, paid a suspicious invoice), report it **immediately**. Early reporting lets the SOC contain it; hiding it lets the attacker win.
6. **No blame for honest reporting.** Nobody is punished for reporting a genuine mistake or a false alarm in good faith. `[ORGANISATION]` treats honest reporting as helping, not failing.

### What happens after you report

- The security team confirms they received it and may ask a few questions.
- They assess and, if needed, act: contain the problem, reset a password, lock a device.
- You may be asked to help (do not delete anything, keep the suspicious email).
- You will not be blamed for reporting.

### Roles

- **Everyone** reports suspected incidents.
- **The security team or SOC** receives, assesses and acts on reports.
- **Managers** support their teams in reporting and never discourage it.
- **HR** ensures the no-blame principle is upheld.

### Owner and review

**Owner:** `[role]`. **Approved by:** `[role]`. **Next review:** `[date]`.

---

## Guidance (not part of the policy)

!!! danger "Blame kills reporting, and silence kills organisations"
    The single biggest factor in whether people report early is whether they are afraid of being blamed. If clicking a phishing link gets someone shouted at, the next person who clicks will stay quiet, and the attacker gets hours or days of free rein. A genuine no-blame culture for honest reporting is a security control, not a soft nicety. Protect it fiercely.

!!! tip "Make reporting effortless"
    The easier it is to report, the more you hear. One well-known address, a one-click report button in email, and a friendly response make reporting a habit. Thank people for reporting, even false alarms, so they keep doing it.

## What the SOC does with reports

- Triages the report like any alert, with the human context it adds.
- Uses reported phishing to find and purge the same campaign from other mailboxes ([phishing playbook](../04-playbooks/phishing.md)).
- Acts fast on reported mistakes: reset credentials, isolate devices, recall payments.
- Feeds patterns back into awareness training and detections.

## Related pages

- [Employee security guide](employee-security-guide.md)
- [Phishing playbook](../04-playbooks/phishing.md)
- [Escalation and communication](../03-incident-response/escalation-and-communication.md)
- [IR lifecycle](../03-incident-response/ir-lifecycle.md)
