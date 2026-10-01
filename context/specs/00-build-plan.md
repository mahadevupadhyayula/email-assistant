# MVP Build Plan

Implement only one approved unit at a time. A unit is complete only when its acceptance evidence is recorded and `progress-tracker.md` is updated.

| Unit | Result | Prerequisites | Acceptance evidence | Recording opportunity | Independent rollback |
|---|---|---|---|---|---|
| 01 Local foundation | Reproducible local, workspace-scoped Django system | Approved context | Local services healthy; migrations/tests pass | Architecture and local startup | Yes, before product data |
| 02 Google identity and Gmail consent | Separate sign-in and read-only mailbox connection | 01 | Scope, token, disconnect, and authorization tests | Consent and trust walkthrough | Yes |
| 03 Gmail sync and normalization | Complete active threads from the last 10 days | 02 | Fixture and sandbox sync evidence; idempotency | Data-flow demonstration | Yes, with schema rollback plan |
| 04 Founder priorities | Confirmed, time-aware priority system | 01 | Proposal/confirmation/history tests | Onboarding and priority demo | Yes |
| 05 AI extraction | Validated provider-neutral thread intelligence | 03, 04 | Eval report and schema/failure tests | Graph and eval walkthrough | Yes by adapter/prompt version |
| 06 Deterministic ranking | Reproducible Priorities, Actions, Urgency ordering | 05 | Golden ranking fixtures and explanations | Rule visualization | Yes by rule-set version |
| 07 Briefing and dashboard | Morning snapshot and responsive three-lens UI | 06 | Schedule, snapshot, UI, accessibility tests | Founder-facing core demo | Yes |
| 08 Conversational intelligence | Workspace-scoped chat with safe read tools | 05, 07 | Tool authorization and answer-grounding tests | Chat demo and graph walkthrough | Yes |
| 09 Corrections and internal actions | Review, correct, snooze, dismiss, restore, complete | 07, 08 | Cross-view consistency and confirmation tests | Trust/correction demo | Yes |
| 10 Retention and release evidence | Ninety-day deletion, audit, observability, E2E evidence | 01–09 | Deletion proof, isolation suite, E2E report | Complete product and failure demo | Partially; deletion migrations need care |

## Dependency rationale

- Establish workspace ownership before storing credentials or email.
- Separate identity/consent before importing data.
- Normalize source data before AI analysis.
- Define confirmed priorities before evaluating priority matching.
- Validate extraction before deterministic ranking.
- Stabilize ranking contracts before building dashboard projections.
- Give chat read tools before allowing it to propose internal mutations.
- Complete retention and end-to-end evidence before considering hosted deployment.

## MVP completion gate

- All unit acceptance criteria pass.
- Gmail remains read-only by code and OAuth scope.
- Tenant isolation tests pass across web, task, search, and chat paths.
- Evaluation meets approved recall/irrelevance thresholds on the agreed fixture set.
- A founder can complete the full journey locally.
- Retention and workspace deletion are demonstrated.
- Known gaps are recorded rather than hidden.

## Deferred roadmap

- Phase 2: Reply Copilot with voice profile, draft evidence, review, and explicit send boundary.
- Phase 3: Delegating Operator with backend-enforced approvals, authorization, expiry, audit, cancellation, and rollback where possible.
- Privacy phase: configurable retention and transient-processing mode.
- Platform phase: additional model/provider adapters and certified on-prem endpoints.
- Hosting phase: execute `context/future-aws-architecture.md` through a separately approved implementation plan.

