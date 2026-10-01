# Build and Product Recording Plan

## Audience

Primary audiences are builders/technical collaborators and potential users/design partners. Each checkpoint pairs implementation reasoning with a founder-visible outcome.

## Opening promise

Show how an early-stage founder can understand what deserves attention in a busy Gmail inbox within five minutes—without letting an agent send or modify email.

## Audience takeaways

### Builders

- How product decisions become explicit system boundaries.
- Why structured extraction and deterministic ranking are separated.
- How tenant isolation, read-only Gmail, confidence, confirmation, and deletion are enforced.
- How LangGraph, LangChain, Django, and Celery have distinct responsibilities.
- How evidence and evaluations gate model/provider changes.

### Design partners

- What the morning briefing and three dashboard lenses do.
- How founder priorities reshape attention.
- How chat answers ad hoc questions without taking unsafe actions.
- How uncertainty, correction, privacy, and retention work.

## Narrative outline

1. Founder inbox problem and five-minute promise.
2. MVP boundary and progression to Reply Copilot and Delegating Operator.
3. Approved user journey and safety model.
4. Architecture and local runtime.
5. Feature-by-feature build checkpoints.
6. Complete product demonstration.
7. Evaluation and test evidence.
8. Failures, limitations, and improvement opportunities.
9. Next-video boundary: Reply Copilot design, not implementation unless separately approved.

## Visual inventory

| Visual | Audience question | Core message | Source | Format | Placement |
|---|---|---|---|---|---|
| Product progression | Where is this going? | Understand → recommend → draft → act | Project overview | Slide | Opening |
| Core journey | How does value appear? | Consent through briefing and correction | Project overview | Flow diagram | Product setup |
| Modular monolith | Why this stack? | One Python system, separate runtime roles | Architecture | Diagram | Technical overview |
| Data/trust boundary | What sees email? | Scoped Gmail, storage, model context, deletion | Architecture | Diagram | Trust section |
| AI workflow | How is ranking produced? | Extraction is generative; ranking is deterministic | Architecture/specs 05–06 | Flow diagram | Intelligence section |
| Three lenses | Why multiple tabs? | Same cards, different decision questions | UI context | Product recording | Dashboard demo |
| Confidence states | What if AI is unsure? | Review rather than false certainty | Specs 05/09 | Product recording | Trust demo |
| Evaluation table | Is it good enough? | Measured recall, irrelevance, and failure cases | Test evidence | Table | Release gate |
| AWS future map | How does local become hosted? | Portable local architecture maps to managed AWS | Future AWS plan | Diagram | Roadmap |

## Recording checkpoints by build unit

1. Foundation: context files, local topology, responsive shell.
2. Identity/consent: separate sign-in and Gmail permission flow.
3. Sync: ten-day latest-activity rule and complete-thread import.
4. Priorities: conversational statement to confirmed structured priority.
5. Extraction: graph, schema, confidence, and sanitized eval case.
6. Ranking: one fixture projected through all three lenses.
7. Dashboard: morning snapshot, live state, mobile behavior.
8. Chat: grounded question, citations, and blocked unsafe request.
9. Corrections: needs-review correction and cross-view update.
10. Release: end-to-end journey, deletion, tests, metrics, and limitations.

## Code walkthrough checklist

- Domain boundaries and workspace scope
- OAuth credential boundary
- Gmail sync idempotency
- Product-owned AI schemas and adapters
- LangGraph states and failure paths
- Deterministic ranking reason codes
- Immutable briefing snapshot
- Chat tool authorization
- Founder override precedence
- Retention/deletion lineage
- Tests and evaluation fixtures

## Demonstration data

Use synthetic founders, organizations, senders, and email threads. Include customer escalation, investor request, CTO candidate, vendor urgency, newsletter noise, ambiguous date, conflicting request, old-but-active thread, prompt-injection email, and irrelevant false-positive scenarios.

## Final demonstration

Start from a connected synthetic mailbox, show the morning briefing, traverse all lenses, ask chat an ad hoc question, propose and confirm a priority, correct a date, snooze an item, inspect evidence, open the source link, and show retention/deletion behavior.

## Failure and improvement discussion

Show one provider failure, one low-confidence extraction, one partial sync, and one relevance error. Explain how the system degrades, what evidence is captured, and which improvement requires a new approved spec.

## Next-video boundary

The next narrative may define Reply Copilot: founder voice, draft evidence, editing, approval, and send authorization. It must not imply that MVP chat can draft or send email.

