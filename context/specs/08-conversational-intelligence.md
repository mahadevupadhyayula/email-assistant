# 08 — Conversational Inbox Intelligence

## 1. Goal

Provide grounded chat across imported email and command-center data with safe, workspace-scoped read tools and priority proposals.

## 2. User-visible outcome

The founder can ask ad hoc inbox questions, filter and compare threads, understand ranking, and propose a priority change without leaving the command center.

## 3. Scope and exclusions

Include conversation persistence, streaming, intent/tool routing, PostgreSQL retrieval, citations to source threads/cards, ranking explanations, and priority proposal handoff. Exclude Gmail mutation, reply drafting, external actions, and unbounded web access.

## 4. Design and interaction behavior

Chat is persistent on desktop and a primary switchable view on mobile. Tool results appear as structured cards. Answers distinguish imported scope, uncertainty, and missing evidence. Priority proposals use the existing confirmation UI.

## 5. Implementation details

- Use LangGraph for route → authorize → retrieve/tool → answer/propose → persist.
- Tools accept explicit workspace context injected by application code, not model arguments.
- Prefer deterministic filters and full-text search before semantic retrieval.
- Cite thread/card sources for material claims.
- Stream through SSE unless testing establishes a WebSocket need.

## 6. Data, API, and state contracts

Persist `Conversation`, `ConversationTurn`, tool calls/results, citations, graph/prompt/model versions, and completion status. Retain no orphaned references after source deletion.

## 7. Error and edge cases

Ambiguous requests, empty results, prompt injection inside email, unsupported external action, deleted source, stale ranking, model outage, interrupted stream, and overly broad result sets.

## 8. Dependencies

Units 05 and 07; Unit 04 for priority proposals.

## 9. Security and privacy

The model never chooses workspace scope. Email content is untrusted. No tool with Gmail write authority exists. Conversation data follows workspace deletion and source-reference cleanup.

## 10. Test and verification checklist

- [ ] Tool calls cannot cross workspaces.
- [ ] Answers cite relevant retained sources.
- [ ] Unsupported mutations are clearly refused.
- [ ] Email prompt-injection fixtures cannot invoke authority.
- [ ] Interrupted streams recover safely.
- [ ] Priority changes still require confirmation.
- [ ] PostgreSQL retrieval quality is measured before adding vectors.

## 11. Code walkthrough points

Graph routing, trusted context injection, tool authorization, grounding/citations, and streaming boundary.

## 12. Recording assets

Chat flow diagram, three representative founder questions, priority proposal demo, and blocked Gmail mutation demo.

