# Architecture

## Architectural style

Use a Python modular monolith: one repository and domain model, with separate runtime processes for the Django web application, Celery workers, and Celery Beat scheduler. Do not split business domains into networked microservices during the MVP.

## Stack

| Technology | Role | Rationale |
|---|---|---|
| Python | Primary language | One language for product, integrations, and AI workflows |
| Django | Web, auth, authorization, ORM, admin | Mature security and data-model foundation |
| Django templates + HTMX | Interactive server-rendered UI | Avoids a separate React application and API state layer |
| Alpine.js | Small local UI interactions | Used only where HTML/HTMX is insufficient |
| Tailwind CSS | Responsive styling and tokens | Supports a consistent executive workspace |
| PostgreSQL | System of record and initial search | Strong relational ownership, transactions, and full-text search |
| Redis | Celery broker and short-lived coordination | Keeps durable product state out of ephemeral infrastructure |
| Celery | Background jobs | Durable Gmail sync and AI-processing tasks |
| Celery Beat | Per-workspace schedules | Morning briefing generation in founder time zones |
| LangGraph | Stateful AI workflows | Explicit transitions, checkpoints, retries, and review states |
| LangChain | Model/tool adapters and structured output | Provider integration behind product-owned contracts |
| ASGI | Async and streaming boundary | Supports streamed chat and concurrent external calls |
| Google OAuth + Gmail API | Identity and read-only inbox source | MVP provider selected by product scope |
| OpenAI | MVP LLM provider | Initial implementation behind an adapter |
| Docker Compose | Local runtime | Repeatable local web, database, Redis, worker, and scheduler setup |

## Responsibility map

- `accounts`: user identity, workspace membership, session, and account lifecycle.
- `gmail`: OAuth connection, encrypted tokens, incremental sync, provider IDs, and source links.
- `mail`: normalized threads, messages, participants, labels-as-source-metadata, and retention.
- `priorities`: confirmed priorities, proposals, scopes, time windows, and change history.
- `intelligence`: provider-neutral model capabilities, extraction schemas, prompt versions, and evaluation metadata.
- `ranking`: deterministic scores, rule versions, explanations, and lens projections.
- `briefings`: scheduled snapshots, sections, entries, and generation status.
- `assistant`: conversations, read-only tools, internal commands, confirmations, and streamed output.
- `feedback`: corrections, relevance judgments, missing-item reports, and evaluation examples.
- `operations`: task runs, audit events, health checks, retention, and deletion.

## Primary flows

### Connection and initial sync

1. Google identity establishes the application user and workspace.
2. A separate OAuth grant requests only the Gmail permission required by the MVP.
3. Credentials are encrypted and stored outside prompts and logs.
4. Sync queries for threads whose latest message falls within the preceding 10 calendar days.
5. Each matching thread is imported in full, normalized idempotently, and scoped to a workspace.
6. A job dispatches extraction and ranking for changed threads.

### Analysis and ranking

1. Deterministic preprocessing removes unsupported content and prepares relevant thread context.
2. The model adapter returns a product-owned structured extraction schema.
3. Schema validation rejects malformed or unsupported output.
4. Deterministic rules calculate priority relevance, action proximity, and urgency.
5. A separate explanation step describes the ranking using stored evidence.
6. Low-confidence or conflicting results enter `needs_review` rather than becoming confirmed facts.

### Morning briefing

1. Celery Beat dispatches one idempotent briefing job per workspace and local date.
2. The job selects current canonical ranked items.
3. It creates an immutable morning snapshot plus generation metadata.
4. Current command-center projections may update later without rewriting the snapshot.

### Conversational interaction

1. The founder's request enters a LangGraph router.
2. The router selects read tools or a reversible internal-state proposal.
3. Reads are always workspace-scoped.
4. Priority changes become structured proposals and stop for confirmation.
5. Confirmed internal commands write through deterministic application services.
6. The MVP graph has no Gmail mutation or external-action tools.

## Storage model

Core entities include `Workspace`, `User`, `Membership`, `GmailConnection`, `EmailThread`, `EmailMessage`, `Participant`, `Priority`, `PriorityProposal`, `Extraction`, `Ranking`, `Briefing`, `BriefingEntry`, `Conversation`, `ConversationTurn`, `InternalAction`, `Feedback`, `TaskRun`, and `AuditEvent`.

Requirements:

- Every tenant-owned record has a non-null workspace identifier.
- Provider identifiers are unique within their connection/workspace scope.
- Raw/normalized email is distinct from model-derived artifacts.
- Extracted fields store confidence, evidence, model adapter, model version, prompt version, and schema version.
- Rankings store inputs and rule-set version.
- Morning briefings are snapshots, not live queries.
- Email-derived rows retain a deletion lineage to the source thread.

## Authentication, authorization, and ownership

- Google sign-in identifies the application user.
- Gmail authorization is a distinct connection and consent lifecycle.
- Visible MVP creates one founder membership, while roles support future expansion.
- Every read and write is filtered by the authenticated workspace.
- Background jobs carry explicit workspace and connection identifiers, never implicit global context.
- Database access helpers must make unscoped tenant queries difficult.
- OAuth tokens are encrypted, excluded from model context, and redacted from logs.

## Model capability boundary

Application workflows depend on capabilities, not provider SDK types. Initial capabilities:

- `extract_thread_signals`
- `summarize_thread`
- `match_priorities`
- `infer_action_and_date`
- `assess_urgency_evidence`
- `answer_inbox_question`
- `stream_assistant_response`

An adapter advertises structured-output, tool-calling, streaming, context, data-policy, and evaluation status. The OpenAI adapter is first. Future hosted and on-prem adapters must pass conformance and quality gates before selection.

## Search strategy

Use PostgreSQL relational filters and full-text search first. Keep retrieval behind an interface. Add embeddings or a vector index only when evaluation shows that required inbox questions cannot meet relevance targets with PostgreSQL search and deterministic filters.

## Failure handling

- Gmail sync is cursor-based, idempotent, retryable, and records partial progress.
- Invalid model output is rejected and may retry within a bounded policy.
- Low confidence routes to review; it does not fabricate certainty.
- The last successful briefing remains visible when regeneration fails.
- UI states identify stale data and last successful generation time.
- Original Gmail links remain available for every retained thread.
- Poison jobs enter a dead-letter/review state after bounded retries.
- Deletion jobs are idempotent and remove source plus derived data.

## Observability

- Structured logs include correlation ID, workspace-safe pseudonymous ID, job ID, graph run ID, prompt version, adapter, latency, and outcome.
- Never log email bodies, OAuth tokens, secrets, or raw model prompts in production-style logging.
- Track sync freshness, briefing completion, extraction failure, low-confidence rate, queue delay, chat latency, and retention/deletion outcomes.
- Store product audit events separately from diagnostic logs.

## Security and privacy

- Least-privilege, read-only Gmail access during MVP.
- TLS for non-local future transport and encryption at rest for production storage.
- Field/application-level encryption for OAuth credentials.
- Secrets from environment or secret manager, never source control.
- Model calls receive only the context required for a capability.
- Thread and derived artifacts expire 90 days after latest thread activity.
- Workspace deletion removes credentials, source data, derivatives, and conversation references.
- Dependency and container scanning become release gates before cloud deployment.

## Invariants

1. No MVP code path can send or mutate Gmail content or state.
2. No tenant-owned query or background task may execute without an explicit workspace scope.
3. A founder priority affects ranking only after confirmation.
4. Deterministic ranking consumes validated structured signals; raw free-form model text cannot directly set order.
5. Low-confidence dates are never represented as confirmed deadlines.
6. Deleting a thread deletes all email-derived artifacts tied to it.
7. A morning briefing snapshot is immutable after successful publication.
8. Model/provider replacement cannot change product-owned schemas without a versioned migration and evaluation.

## Local topology

Docker Compose should eventually run:

- Django ASGI web process
- Celery worker
- Celery Beat scheduler
- PostgreSQL
- Redis

The local browser connects only to Django. External calls go to Google and the selected model provider. Local setup is the MVP deployment target.

## Future AWS plan

AWS architecture is documented in `context/future-aws-architecture.md`. It is not an MVP implementation requirement and must not add cloud-specific code to early feature units.

## Architecture decisions still open

- Exact OpenAI model and per-capability routing after evaluation
- Final local token-encryption/key-management mechanism
- Whether chat needs WebSockets or server-sent events are sufficient
- Production observability vendor
- AWS region and recovery objectives
- Evidence threshold for introducing semantic/vector retrieval

