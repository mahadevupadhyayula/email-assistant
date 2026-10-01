# 04 — Founder Priorities

## 1. Goal

Create confirmed, editable, time-aware founder priorities through guided onboarding and structured proposals.

## 2. User-visible outcome

The founder states goals conversationally, reviews a structured proposal, confirms or edits it, and manages active, scheduled, paused, expired, and deleted priorities.

## 3. Scope and exclusions

Include onboarding, proposal parsing, confirmation, scope, importance, duration, history, and manual management. Exclude silent learning and direct ranking implementation.

## 4. Design and interaction behavior

A proposal shows goal, importance, applicable people/companies/topics/projects, start/end, and expected ranking effect. Confirm, Edit, and Cancel are explicit. Active priorities remain visible in the workspace.

## 5. Implementation details

- Define deterministic priority lifecycle/state transitions.
- Use an adapter capability only to propose structured fields from natural language.
- Persist no active priority until confirmation.
- Record source, creator, changes, and expiration.
- Provide a deterministic manual form when model parsing fails.

## 6. Data, API, and state contracts

`PriorityProposal` and `Priority` use product-owned schemas with name, description, importance, scopes, dates, status, and provenance. Priority version/history must be queryable.

## 7. Error and edge cases

Conflicting priorities, overlapping scopes, missing duration, ambiguous company/person, expired proposal, edit during confirmation, and model unavailability.

## 8. Dependencies

Unit 01; model adapter skeleton may be introduced here but full extraction belongs to Unit 05.

## 9. Security and privacy

Priorities are workspace-owned and may themselves contain sensitive business plans. Apply the same access controls and log redaction as email data.

## 10. Test and verification checklist

- [ ] No proposal affects ranking before confirmation.
- [ ] Manual creation works without a model.
- [ ] Time-bound priorities activate/expire correctly.
- [ ] Edit/pause/delete history is visible.
- [ ] Cross-workspace access fails.
- [ ] Ambiguous proposals are recoverable.

## 11. Code walkthrough points

Proposal versus active entity, lifecycle, confirmation invariant, scope model, and fallback form.

## 12. Recording assets

Priority lifecycle diagram and onboarding demo from natural-language statement through confirmed structured priority.

