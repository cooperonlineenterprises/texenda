# Texenda project dossier

This mapped dossier distinguishes intended product authority, current
observation, conformance, future plans, evidence, provenance, transition, and
handoff. It does not grant permission, clear a gate, or copy sealed authority.

From `/Users/jamesryancooper/Projects/texenda/repo`, the ordinary validation is:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

Read in this order:

1. [Authority and information roles](AUTHORITY.md)
2. [Validation](validation/README.md) for the one ordinary repository-root command
3. [Handoff](handoff/START_HERE.md), [current observed state](current-state/README.md),
   and [conformance findings](conformance/README.md)
4. [Canonical source map](CANONICAL_SOURCE_MAP.md), [plans](plans/README.md), and
   [RAIDQ](registers/README.md)
5. [Evidence index](evidence/README.md) and [provenance](provenance/README.md)

The [transition status](transition/README.md) and [history](history/README.md) are
maintenance routes, not prerequisites for ordinary development.

The [artifact catalog](ARTIFACT_CATALOG.json) owns per-path information roles.
The generated path-authority mirror is never independently edited.
