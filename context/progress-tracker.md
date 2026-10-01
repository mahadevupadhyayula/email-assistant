# Progress Tracker

Update this file after every meaningful implementation change.

## Current phase

Product brainstorming and implementation planning complete; Build Unit 01 implementation started.

## Current goal

Implement and verify `context/specs/01-local-foundation.md` one acceptance criterion at a time.

## Completed

- Defined primary user, problem, product progression, and MVP boundary.
- Defined measurable success criteria.
- Defined dashboard, briefing, chat, priority, confidence, and correction behavior.
- Selected Gmail-only scope and ten-day active-thread import rule.
- Selected 90-day thread-level retention.
- Selected multi-tenant foundation with single-user visible MVP.
- Selected Python/Django/LangGraph/LangChain architecture.
- Selected OpenAI as MVP provider behind a model-agnostic capability interface.
- Selected local hosting and documented future AWS direction.
- Created build plan, feature specs, and recording plan.
- Initialized the Python 3.12/Django 5.2 project scaffold and dependency locks.
- Added repository ignore rules and environment-based Django secret, debug, and host configuration.
- Documented the initial local setup and stable Django check command.

## In progress

- Build Unit 01 local foundation.

## Next up

- Add the workspace and membership domain models with tenant-scoped access patterns and tests.

## Open questions

- Exact OpenAI model after capability evaluation
- Local token-encryption and developer key workflow
- SSE versus WebSockets for streamed chat
- Final branding and visual tokens
- Future AWS region, RPO, and RTO

## Product and architecture decisions

- MVP is an Inbox Command Center for early-stage founders.
- Morning briefing and chat are both primary experiences.
- Founder-defined priorities drive importance.
- Ranking is structured AI extraction plus deterministic rules.
- Gmail access remains read-only throughout MVP.
- Local Docker Compose is the MVP runtime.
- AWS deployment is future work only.

## Risks and blockers

- Gmail OAuth verification and scopes may affect later external distribution.
- Ten days of activity may be insufficient for relationship inference; guided priorities mitigate this.
- LLM extraction quality must be measured with controlled fixtures before relying on rankings.
- Retaining normalized email requires careful deletion lineage and secret handling.
- A model-agnostic interface can become lowest-common-denominator abstraction if capabilities are not explicit.

## Resume notes

Continue Build Unit 01 only. Repository hygiene and environment configuration are in place; the workspace-scoped domain foundation is next.
