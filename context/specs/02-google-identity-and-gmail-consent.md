# 02 — Google Identity and Gmail Consent

## 1. Goal

Implement Google application sign-in and a separate, explicit read-only Gmail connection lifecycle.

## 2. User-visible outcome

The founder signs in, creates/enters a workspace, reviews Gmail access disclosure, connects a mailbox, sees connection health, and can disconnect it.

## 3. Scope and exclusions

Include OAuth state/PKCE protections as applicable, read-only scope, encrypted token storage, refresh, revocation/disconnect, and connection status. Exclude email sync and all Gmail mutations.

## 4. Design and interaction behavior

Sign-in and Connect Gmail are separate screens/actions. Consent copy explains what is read, stored, retained, and not modified. Disconnect does not imply data deletion; offer a distinct deletion path placeholder.

## 5. Implementation details

- Keep identity credentials separate from Gmail connection credentials.
- Encapsulate Google client behavior behind an integration service.
- Encrypt refresh/access credentials with a local key strategy documented for later replacement.
- Record consent and connection audit events.

## 6. Data, API, and state contracts

`GmailConnection` belongs to a workspace and records provider account identifier, scopes, encrypted credentials, status, timestamps, and sync cursor placeholders.

## 7. Error and edge cases

Denied consent, expired state, account mismatch, revoked token, insufficient scope, refresh failure, duplicate connection, and partial callback failure.

## 8. Dependencies

Unit 01.

## 9. Security and privacy

Use the minimum read-only Gmail permission. Tokens never enter templates, logs, tasks, prompts, or model context. Validate callback state and redirect targets.

## 10. Test and verification checklist

- [ ] Sign-in and Gmail consent are distinct.
- [ ] Only approved read-only scopes are requested.
- [ ] Tokens are encrypted at rest and redacted.
- [ ] Revoked/expired connection states are visible.
- [ ] Cross-workspace connection access fails.
- [ ] Disconnect is reversible and does not silently delete data.

## 11. Code walkthrough points

Two-consent model, scope enforcement, token envelope, connection lifecycle, and authorization checks.

## 12. Recording assets

Consent-flow diagram, scope display, connection/disconnection demo, and safe token-storage explanation.
