# AI Workflow Rules

These rules apply to any coding agent or collaborator modifying this repository.

1. Read all context documents, the build plan, and the active feature spec before modifying code.
2. Work on one approved feature unit at a time.
3. Do not implement deferred Reply Copilot, Delegating Operator, cloud hosting, or transient-processing features during the MVP.
4. Do not make speculative refactors or unrelated changes.
5. Surface missing, ambiguous, or contradictory requirements before encoding them.
6. Preserve user-owned, generated, secret, migration, and fixture data.
7. Keep Gmail access read-only. Stop before adding any external mutation or consequential action.
8. Keep all tenant data and operations explicitly workspace-scoped.
9. Require confirmation before a proposed founder priority becomes active.
10. Use product-owned typed schemas between LangGraph/LangChain and provider adapters.
11. Keep ranking deterministic after structured extraction; models may not directly choose final ordering.
12. Record confidence and evidence for inferred actions, dates, urgency, and priority matches.
13. Route uncertain results to review rather than inventing certainty.
14. Never expose OAuth tokens, secrets, email bodies, or raw prompts in logs.
15. Use synthetic email fixtures for routine tests and demonstrations.
16. Verify acceptance criteria, tests, types, migrations, and relevant runtime paths before declaring a unit complete.
17. Run model capability evaluations before changing a model, adapter, prompt, schema, or ranking-relevant extraction.
18. Update context documentation and `progress-tracker.md` after meaningful implementation changes.
19. Preserve rollback boundaries and document migrations or irreversible changes.
20. Stop for explicit approval before repository publication, cloud deployment, live-email testing beyond the approved mailbox, or any external write.

