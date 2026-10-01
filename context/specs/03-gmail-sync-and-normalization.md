# 03 — Gmail Sync and Normalization

## 1. Goal

Import and incrementally synchronize complete Gmail threads whose latest message is within the previous 10 calendar days.

## 2. User-visible outcome

The connected founder sees sync progress, freshness, imported thread count, and source-linked normalized threads.

## 3. Scope and exclusions

Include initial active-thread selection, full matching-thread fetch, MIME-safe normalization, participants, source labels as metadata, incremental change detection, idempotency, and source links. Exclude older-mail search and Gmail mutations.

## 4. Design and interaction behavior

Show not-started, syncing, partial, current, stale, and failed states. Never claim the mailbox is fully represented beyond the stated ten-day active window.

## 5. Implementation details

- Calculate the cutoff in the workspace time zone, then query/fetch through Gmail.
- Include a thread only when its latest message timestamp satisfies the cutoff.
- Once included, import the complete thread even when its first messages are older.
- Normalize text/HTML safely, preserve minimal source metadata, and avoid executing remote content.
- Use stable Gmail IDs and upserts for idempotency.
- Dispatch changed thread IDs for later analysis.

## 6. Data, API, and state contracts

Persist `EmailThread`, `EmailMessage`, participants, source identifiers, timestamps, normalized bodies, snippet, source-link information, and sync/run records. Source records belong to workspace and connection.

## 7. Error and edge cases

Large threads, malformed MIME, missing bodies, attachments, deleted messages, moved labels, API pagination, rate limits, token revocation, duplicate delivery, and partial sync.

## 8. Dependencies

Unit 02.

## 9. Security and privacy

Sanitize HTML, do not fetch remote images, do not send content to a model in this unit, and avoid logging source content.

## 10. Test and verification checklist

- [ ] Cutoff is based on latest message, not first message.
- [ ] Active old threads import completely.
- [ ] Inactive unread/starred threads do not bypass cutoff.
- [ ] Repeated sync is idempotent.
- [ ] Incremental updates modify only relevant threads.
- [ ] Partial failure and resume are demonstrated.
- [ ] Tenant isolation holds in tasks and queries.

## 11. Code walkthrough points

Cutoff semantics, Gmail pagination, normalization, idempotency, sync state, and security treatment of HTML.

## 12. Recording assets

Sync sequence diagram, fixture mailbox before/after, progress UI, and failure/resume demonstration.

