# Project Overview

## Product definition

Email Assistant is the email-intelligence component of a larger executive-assistant product for founders and leaders. Its MVP is an Inbox Command Center for early-stage founders who manage their own Gmail inbox. It creates a decision-ready morning briefing, presents active email through Founder Priorities, Actions, and Urgency lenses, and provides conversational access to inbox intelligence. The MVP helps the founder understand what deserves attention and why; it does not draft, send, or modify email.

## Primary user and problem

The first user is an early-stage founder without dependable executive-assistant support. Their inbox combines customers, investors, candidates, partners, vendors, internal work, notifications, newsletters, and cold outreach. The primary problem is not knowing what deserves attention. The related problem is spending too much time reading threads and reconstructing context before deciding what to do.

## Product progression

1. **MVP — Inbox Command Center:** understand and organize.
2. **Phase 2 — Reply Copilot:** prepare context-aware replies in the founder's voice, with review before sending.
3. **Phase 3 — Delegating Operator:** create tasks, coordinate follow-ups, and perform approved external actions.

The progression is: understand → recommend → draft → act with approval.

## Goals and success criteria

- A founder understands the important inbox state in under five minutes.
- At least 90% of emails the founder judges important appear in a relevant command-center view.
- Inbox triage and comprehension time falls by at least 50%.
- Fewer than 10% of emails surfaced as important are judged irrelevant.
- Every inferred action and date is explainable, correctable, and traceable.
- AI or integration failure never hides access to the original Gmail thread.

## Core journey

1. Founder signs into the application with Google.
2. Founder separately grants read-only Gmail access after seeing a clear consent explanation.
3. The application creates a single visible founder workspace on a multi-tenant foundation.
4. Founder defines initial priorities through guided conversation.
5. Priority statements become structured proposals and affect ranking only after confirmation.
6. The system imports complete threads whose latest message is within the previous 10 calendar days.
7. The system extracts structured signals, applies deterministic ranking, and generates the first briefing.
8. The founder reviews a morning briefing and moves between Founder Priorities, Actions, and Urgency views.
9. The founder uses chat to search, summarize, compare, filter, explain, snooze, dismiss, restore, or correct command-center information.
10. Corrections update product state and evaluation evidence but do not silently create permanent rules.
11. Email threads and their derived artifacts expire 90 days after the thread's latest activity unless deleted earlier.

## MVP capabilities

### Daily briefing

- Generated every morning at the founder's configured local time.
- Available in the authenticated dashboard without an external reminder.
- Preserves the morning snapshot while later inbox changes can refresh current views.

### Multi-lens command center

- **Founder Priorities:** groups and ranks mail against confirmed, time-aware priorities.
- **Actions:** orders inferred or confirmed work by action-date proximity.
- **Urgency:** orders mail by the consequence of waiting.
- All views use the same canonical cards and state.

### Conversational inbox intelligence

- Searches the connected, imported mailbox data.
- Summarizes, filters, compares, and explains.
- Proposes structured priority changes for confirmation.
- Corrects inferred actions and dates.
- Changes only reversible internal command-center state.

## Canonical email card

Each card may show:

- Sender and relationship context
- Concise thread summary
- Why the thread matters
- Matched founder priorities
- Requested founder action
- Inferred or explicit action date
- Urgency and consequence of delay
- Confidence by inferred field
- Recommended next step
- Status such as needs review, snoozed, dismissed, or completed
- Link to the original Gmail thread

## In scope

- Gmail and Google Workspace
- Desktop-first responsive web application
- Google sign-in plus separate read-only Gmail consent
- Ten-day active-thread import
- Normalized secure email storage
- Confirmed founder priorities
- Structured AI extraction
- Deterministic ranking
- Morning briefings
- Three dashboard lenses
- Conversational read/search/explain and internal-state actions
- Corrections, confidence, and needs-review workflow
- Ninety-day thread-level retention
- Local Docker-based operation

## Explicitly out of scope

- Reply drafting or sending
- Marking Gmail read/unread, applying labels, archiving, or deleting
- Calendar, CRM, project-management, or task-system writes
- Delegation to people
- Outlook support
- Native mobile apps
- External briefing notifications
- Production cloud deployment
- Transient-processing privacy mode
- Uncertified arbitrary model selection
- Fully autonomous inbox management

## Confirmed assumptions

- The visible MVP supports one founder and one connected mailbox.
- The data model is workspace-scoped from the first migration.
- Founder-defined priorities are the primary importance signal.
- Business impact, relationships, urgency, dates, and content are supporting signals.
- OpenAI is the MVP model provider behind a provider-neutral capability interface.
- The MVP is locally hosted; AWS is a documented future target only.

## Unresolved product questions

- Which exact OpenAI model best meets quality, latency, and cost gates?
- How many initial priorities produce the best onboarding experience?
- What correction frequency should trigger a suggested priority change?
- Should older Gmail search be introduced after the MVP, and should retrieved data then be retained?
- What review and approval experience should govern Phase 2 reply drafting?

