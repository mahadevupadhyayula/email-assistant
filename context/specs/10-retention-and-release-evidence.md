# 10 — Retention, Deletion, and MVP Release Evidence

## 1. Goal

Complete privacy lifecycle, observability, audit, and end-to-end evidence required to call the local MVP functional.

## 2. User-visible outcome

The founder can understand retention, delete a thread or workspace data, inspect basic connection/freshness state, and complete the full product journey reliably.

## 3. Scope and exclusions

Include 90-day thread-activity retention, deletion lineage, workspace deletion, audit events, safe metrics/logging, end-to-end tests, evaluation report, and operating runbook. Exclude AWS deployment and transient-processing mode.

## 4. Design and interaction behavior

Settings state the retention policy plainly. Destructive actions identify scope and require confirmation. Deletion progress and completion/failure are visible. No deleted thread remains accessible through briefings or chat.

## 5. Implementation details

- Schedule idempotent retention scans by thread latest activity.
- Delete messages, thread, extraction, ranking, briefing references/entries, citations, and derived retrieval artifacts as one auditable workflow.
- Workspace deletion revokes/disconnects credentials and removes all owned product data.
- Keep only a minimal content-free deletion audit where legally/product appropriate.
- Add operational metrics without email bodies or raw prompts.

## 6. Data, API, and state contracts

Deletion jobs store scope, requested/eligible time, state, counts, error, and content-free audit ID. Foreign keys and cleanup services must make dangling derived data impossible or detectable.

## 7. Error and edge cases

Partial deletion, active sync during deletion, briefing reference to expired thread, restored Gmail thread after expiry, revoked token, worker crash, and repeated deletion request.

## 8. Dependencies

Units 01–09.

## 9. Security and privacy

Deletion is authorization-sensitive and must be backend-enforced. Prevent races by locking/state transitions. Verify secrets, logs, fixtures, and exports contain no unintended email content.

## 10. Test and verification checklist

- [ ] A thread expires 90 days after latest activity, not first message.
- [ ] Source and all derivatives are removed together.
- [ ] Workspace deletion removes all tenant content and credentials.
- [ ] Repeated/failed deletion resumes safely.
- [ ] Tenant-isolation suite passes across all domains.
- [ ] Full local E2E journey passes.
- [ ] AI evaluation report includes recall and irrelevance metrics.
- [ ] Five-minute and 50% time-reduction study plan/results are recorded.
- [ ] No MVP path has Gmail write permission.
- [ ] Known limitations and rollback procedures are documented.

## 11. Code walkthrough points

Deletion lineage, retention calculation, concurrency control, audit/diagnostic split, E2E suite, and release gate.

## 12. Recording assets

Complete founder journey, retention/deletion demonstration, test/evaluation evidence, failure recovery, limitations, and next-phase handoff.

