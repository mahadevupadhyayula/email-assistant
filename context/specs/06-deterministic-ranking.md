# 06 — Deterministic Ranking

## 1. Goal

Produce reproducible Founder Priorities, Actions, and Urgency ordering from validated signals and confirmed product state.

## 2. User-visible outcome

Every analyzed thread receives explainable placement in one or more lenses, and the founder can understand which inputs caused that placement.

## 3. Scope and exclusions

Include versioned scoring/rules, lens projections, tie-breaking, low-confidence handling, and human-readable explanations grounded in stored inputs. Exclude dashboard polish and model-selected final ordering.

## 4. Design and interaction behavior

- Priorities view: confirmed priority grouping, relevance, then action date/tie-breakers.
- Actions view: overdue, today, upcoming, no reliable date, and review states.
- Urgency view: consequence-of-delay level with explicit evidence.
- The same canonical thread state appears consistently across lenses.

## 5. Implementation details

- Keep ranking as pure/testable functions where possible.
- Separate importance, action proximity, and urgency rather than collapsing them into one opaque score.
- Store rule inputs, output, version, and reason codes.
- Generate explanation text from reason codes/data; do not ask the model to invent ranking causes.

## 6. Data, API, and state contracts

`Ranking` contains thread/extraction/priority versions, lens-specific values, reason codes, confidence gate, computed timestamp, and rule-set version.

## 7. Error and edge cases

Multiple matching priorities, missing dates, timezone boundaries, expired priorities, conflicting signals, equal scores, stale extraction, and corrected fields.

## 8. Dependencies

Unit 05.

## 9. Security and privacy

Ranking services operate on workspace-scoped IDs and return no cross-workspace aggregate information.

## 10. Test and verification checklist

- [ ] Same inputs and version always produce the same output.
- [ ] Golden fixtures cover each lens and tie-breaker.
- [ ] Low-confidence dates never become confirmed action order.
- [ ] Expired priorities stop influencing new rankings.
- [ ] Explanations exactly match stored reasons.
- [ ] Target relevance/recall metrics can be computed.

## 11. Code walkthrough points

Three-lens separation, pure ranking functions, versioning, reason codes, and golden tests.

## 12. Recording assets

Ranking input/output table, one email moving across lenses after a confirmed priority change, and reproducibility test.

