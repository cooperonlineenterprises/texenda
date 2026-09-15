# Conformance

[`findings.json`](findings.json) is the authoritative owner for new mapped
workspace/adoption findings. It compares direct observations with the reviewed
structural contract; it does not assess or pass Texenda product criteria.
[`machine-readable/findings.json`](../machine-readable/findings.json) is a
refresh-only mirror.

The authoritative [remediation register](remediation-register.json) records all
review findings, validity, impact, dependencies, chosen dispositions, validation
and completion limits. Each deferred row has one closed `deferred_ref` naming
the sole RAIDQ owner path and record ID. Repository validators resolve it into
owner, blocker, trigger, risk, required evidence, exact next action and recovery;
inline overrides, unknown fields and missing sources fail. No row is a live
task or lease, and the register does not duplicate editable deferral details.
