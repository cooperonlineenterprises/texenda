# Validation

The single command registry is [`.agent/validators.json`](../../.agent/validators.json).
From `/Users/jamesryancooper/Projects/texenda/repo`, the ordinary complete
read-only command is:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 -B .agent/scripts/validate.py --check --all --state-root /Users/jamesryancooper/Projects/texenda/local/agent-state/texenda
```

It runs the registered local, sealed, package, schema/link/owner/evidence, and
negative/recovery checks while skipping refresh writers. PASS is bounded evidence
only; it clears no product or external gate. Use explicit refresh only when a
declared generated view is stale and the underlying source change is understood.

`validate.py --check` performs no explicit project writes and must preserve file
content, path membership, mode, size, modification time (`mtime`), metadata-change
time (`ctime`), generated outputs, caches, locks, and live state. The operating
system may advance access time (`atime`) merely because validation reads a file.
Portable Python cannot prevent or restore that filesystem-managed update without
performing a mutation, so atime stability is explicitly outside the no-write
guarantee. Only `refresh.py --refresh` may update generated views.

`validate.py --check --all` resolves shell-free registry argv from a validated
repository/project-home/state-root context. It categorically skips every
`refresh_writer`; state-root options precede coordinator subcommands. Both check
modes reject an interrupted-refresh marker before delegation and deterministically
reconstruct all eleven generated outputs byte-for-byte.

Shared facade/coordinator readers use nonblocking no-follow opens, require a
regular descriptor before content access, and recheck path/inode identity. FIFO,
socket, device, directory, and post-preflight substitutions fail promptly.

Only those exact eleven paths are excluded from the source fingerprint.
`.agent/generated/README.md` and any additional implementation file under that
directory remain source; adding one makes an unrefreshed or uncommitted
projection stale. Complete synthetic check-all proofs cover both the default
pre-binding layout and an active external binding.
