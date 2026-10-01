# 07 — Morning Briefing and Command Center

## 1. Goal

Deliver an immutable daily briefing and responsive three-lens command center using canonical thread state.

## 2. User-visible outcome

At the configured morning time, the founder can open the app and understand what matters, what requires action, and what is urgent in under five minutes.

## 3. Scope and exclusions

Include schedule configuration, idempotent snapshot generation, freshness, lens tabs, cards, detail/evidence view, source links, needs-review section, responsive layout, and accessibility. Exclude external reminders and Gmail mutations.

## 4. Design and interaction behavior

Desktop uses main dashboard plus persistent assistant panel placeholder/current chat integration point. Mobile uses single-column views. Cards share status across tabs. The morning snapshot is distinguishable from the live/current projection.

## 5. Implementation details

- Schedule by founder time zone and local date.
- Enforce one successful snapshot per workspace/date/version unless an explicit regeneration record is created.
- Render server-side and update fragments through HTMX.
- Preserve focus and announce meaningful updates.
- Link each card to the original Gmail thread.

## 6. Data, API, and state contracts

`Briefing` stores workspace, local date, generated time, source freshness, status, rule/model versions, and immutable entries. Live lens queries use current canonical rankings.

## 7. Error and edge cases

DST/timezone changes, scheduler duplication, late sync, partial extraction, no important email, stale briefing, failed regeneration, and deleted source after snapshot.

## 8. Dependencies

Unit 06.

## 9. Security and privacy

Never cache one workspace's HTML for another. Avoid email content in URLs. Preserve authorization on HTMX endpoints and Gmail links.

## 10. Test and verification checklist

- [ ] Morning generation is time-zone correct and idempotent.
- [ ] Snapshot stays immutable while live views update.
- [ ] The same card state is consistent across tabs.
- [ ] Empty, partial, stale, failure, and review states render.
- [ ] Keyboard, screen-reader, contrast, and mobile checks pass.
- [ ] Five-minute comprehension study procedure is documented.

## 11. Code walkthrough points

Snapshot/live distinction, scheduling, canonical projections, HTMX state, and accessibility.

## 12. Recording assets

Morning-opening product demo, responsive captures, three-lens comparison, and stale/partial failure demo.

