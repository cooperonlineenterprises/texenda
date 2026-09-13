# Optional explanatory visualizations

Use this guidance only when a diagram or interactive view materially improves
review of a relationship, sequence or state boundary. None is required for
routine work. Prefer the smallest useful representation; do not add decorative
diagrams, speculative architecture or new rendering services.

Derive the view from named authoritative files and a full source revision or
file hashes. Include provenance, an explanation of the relationship and a
complete accessible text equivalent. Label the view explanatory and
non-authoritative. Preserve source semantics, including denials, uncertainty,
scope and recovery branches. A visual must not simplify away a safety boundary,
invent a dependency or imply that a product/external gate passed.

Inspect the rendered result against the source. Any source change invalidates
the view; regenerate and recheck it before reuse. Keep the source and prior
review evidence intact. The [operating guide](operating-guide.md) and normative
topic owners continue to govern; a generated view cannot amend them.
