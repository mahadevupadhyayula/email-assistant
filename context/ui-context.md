# UI Context

## Direction

Create a calm executive workspace with persistent conversational assistance. It should feel like a decision environment, not another crowded inbox and not a chat interface that hides important information.

## Principles

- Lead with decisions and required attention, not email chronology.
- Make every ranking explainable.
- Keep the original Gmail thread one clear action away.
- Use progressive disclosure: summary first, evidence and thread detail on demand.
- Treat uncertainty as a first-class state.
- Keep chat powerful but prevent it from obscuring persistent dashboard state.
- Favor calm hierarchy over alarm-heavy visuals.

## Information hierarchy

1. Briefing freshness and generation status
2. Current founder priorities
3. View selector: Founder Priorities, Actions, Urgency
4. Ranked canonical email cards
5. Needs Review
6. Persistent assistant access
7. Secondary settings, connection, and retention controls

## Desktop layout

- Top bar: product identity, workspace, sync/briefing freshness, account menu.
- Priority strip: confirmed active priorities with duration and management action.
- Main region: tabbed command center and canonical card list.
- Persistent right panel: conversational assistant, collapsible but easy to restore.
- Detail drawer/modal: evidence, message timeline, corrections, and Gmail link.

## Mobile layout

- Single-column briefing/card feed.
- Sticky switch between Command Center and Assistant.
- Tabs remain horizontally accessible without hiding labels.
- Detail opens as a full-height sheet.
- No desktop-only critical action.

## Canonical card behavior

A card shows sender, summary, reason, matched priority, requested action, date, urgency, confidence, and status as applicable. Expanding it reveals evidence and correction controls. Correcting a card updates every lens because cards are projections of shared state.

## Semantic tokens

Final brand colors remain open. Define semantic tokens rather than hard-coded colors:

- `surface/base`, `surface/raised`, `surface/subtle`
- `text/primary`, `text/secondary`, `text/muted`
- `border/default`, `border/strong`, `focus/ring`
- `status/critical`, `status/high`, `status/normal`, `status/low`
- `confidence/high`, `confidence/medium`, `confidence/low`
- `state/success`, `state/warning`, `state/error`, `state/info`

Every semantic color requires a text label or iconographic distinction.

## Typography and spacing

- Use a highly legible system or approved sans-serif family.
- Use tabular numerals for dates/counts where helpful.
- Maintain a compact but breathable card rhythm.
- Use an 8px-based spacing system with smaller 4px adjustments.
- Use moderate radii and restrained elevation; avoid decorative glass effects.

## Components

- Briefing status header
- Priority chip and priority proposal card
- Lens tabs
- Email decision card
- Confidence badge
- Action-date badge
- Urgency indicator
- Needs-review queue
- Correction form
- Snooze/dismiss/restore controls
- Chat transcript, composer, tool-result card, and confirmation card
- Empty, loading, stale, partial, and error states
- Gmail connection and retention settings

## Interaction rules

- Priority proposals require explicit Confirm, Edit, or Cancel.
- Low-confidence dates cannot visually imitate confirmed deadlines.
- Dismiss and snooze are reversible.
- Destructive deletion uses a clear confirmation and scope statement.
- Streaming chat must not cause layout jumps that disrupt reading.
- Filters and tabs update the URL or restorable state where practical.

## Accessibility

- Meet WCAG 2.2 AA as the implementation target.
- Full keyboard operation and predictable focus management.
- Announce HTMX updates and streamed completion appropriately.
- Provide accessible names for icons and confidence/status controls.
- Respect reduced-motion preferences.
- Use human-readable dates with machine-readable semantics.

## Prohibited inconsistencies

- Different status or action values for the same email across tabs
- Color-only urgency or confidence
- Chat-only access to essential information
- Hidden model uncertainty
- Silent priority changes
- Gmail-looking controls that imply unsupported Gmail mutation
- Fabricated deadlines shown as confirmed facts

## Unresolved visual choices

- Brand name and visual identity
- Exact color palette and typography
- Density preference testing with founders
- Whether chat defaults open on smaller laptops

