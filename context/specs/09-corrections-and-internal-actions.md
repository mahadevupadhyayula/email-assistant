# 09 — Corrections and Internal Actions

## 1. Goal

Make AI output reviewable and allow reversible command-center actions without changing Gmail.

## 2. User-visible outcome

The founder can confirm/edit/reject actions and dates, mark an internal action complete, snooze, dismiss, restore, and report missing or irrelevant items. Changes remain consistent across dashboard and chat.

## 3. Scope and exclusions

Include review queue, correction provenance, reversible states, chat-initiated proposals, confirmation where appropriate, and evaluation feedback export. Exclude Gmail state changes and automatic permanent learning.

## 4. Design and interaction behavior

One-click correction opens a focused form. Low-confidence items start in Needs Review. Snooze requires a return date. Dismiss and completion are reversible. Chat communicates proposed state changes before execution when ambiguity or consequence warrants it.

## 5. Implementation details

- Apply changes through deterministic services shared by web and chat.
- Recompute affected rankings after correction.
- Keep source extraction separate from founder-confirmed overrides.
- Turn validated failures into privacy-safe evaluation examples.
- Do not silently infer a permanent preference from one correction.

## 6. Data, API, and state contracts

`InternalAction` and `Feedback` store type, source, prior/new values, actor, timestamp, confirmation, and reversibility. Effective value resolution prefers valid founder overrides over model inference.

## 7. Error and edge cases

Concurrent edits, expired snooze, correction after source deletion, duplicate command, undo after reranking, and chat/web race conditions.

## 8. Dependencies

Units 07 and 08.

## 9. Security and privacy

Audit internal mutations. Enforce workspace authorization. Feedback exported for evaluation must use synthetic or properly sanitized content.

## 10. Test and verification checklist

- [ ] Correction changes every lens consistently.
- [ ] Founder override wins over inference without rewriting source extraction.
- [ ] Snooze returns at the correct local date/time.
- [ ] Dismiss/restore and complete/reopen work.
- [ ] Duplicate commands are idempotent.
- [ ] Corrections produce evaluation metadata.
- [ ] No action mutates Gmail.

## 11. Code walkthrough points

Effective-value resolution, shared command services, provenance, reversibility, and feedback-to-eval loop.

## 12. Recording assets

Needs Review demo, date correction, cross-tab consistency, chat-initiated snooze, and undo sequence.

