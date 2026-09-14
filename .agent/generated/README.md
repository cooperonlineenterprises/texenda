# Generated integrity boundary

This README is maintained source navigation. Only
[the explicit refresh command](../scripts/refresh.py) writes the two generated
files in this directory or the other nine registered projections (eleven total).
`validate.py --check` is read-only. Every generated output is non-authoritative, hash-bound, and fails stale or
partial. Check deterministically rebuilds and byte-compares all eleven outputs,
including Markdown, current-state mirrors, report claims, and the manifest's
generation-ID derivation. `--check --all` never dispatches a `refresh_writer`.
Checksums establish byte identity only.

The exclusion list is exact, not directory-wide. This README and any additional
code placed here are source-scoped and invalidate stale generated projections.
