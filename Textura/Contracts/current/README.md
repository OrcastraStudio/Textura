# Contracts

This component owns common record vocabulary and local storage primitives. Read `record-contracts.md` before adding a writer. `storage.py` is the dependency shared by implemented components. It performs structural checks, not fact checking or author approval.

Inputs: component-owned records and explicit filesystem paths. Outputs: UTF-8 JSON, stable ASCII IDs, UTC timestamps and SHA-256 references. No network access. Persistent records belong to the component that owns their meaning; Contracts does not become a shared data warehouse.

Dependency direction: all implementation components may import Contracts; Contracts imports no other component's implementation. Settings and the component registry are owned by Configuration. Manuscripts and source text retain their original languages.

The [style and fiction protocol contracts](style-fiction-contracts.md) add shared vocabulary for agent-produced records. They do not add validators or CLI verbs to storage.py. Formal interface implementation and actual analysis remain distinct from blank templates.
