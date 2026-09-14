# Generated integrity boundary

Only [the explicit refresh command](../scripts/refresh.py) writes this directory
or the registered generated projections. `validate.py --check` is read-only.
Every generated file is non-authoritative, hash-bound, and fails stale or
partial. Checksums establish byte identity only.
