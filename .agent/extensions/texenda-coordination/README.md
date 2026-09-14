# Texenda coordination extension

This restrictions-only adapter registers the existing local coordinator and
routing policy by exact path/hash. It does not copy the live roster, work-package
state machine, task records, receipts, gates, decisions, evidence, or product
schemas. It may add validation and restrictions; it may never expand authority.

The machine contract is [`extension.json`](extension.json). Any bound source
change makes validation fail until an exact reviewed refresh of this adapter.
