# 05 — Provider-Neutral AI Extraction

## 1. Goal

Turn normalized threads into validated, evidence-backed structured signals using an OpenAI MVP adapter behind model-agnostic capability contracts.

## 2. User-visible outcome

Threads gain concise summaries, requested actions, inferred dates, urgency evidence, priority matches, and confidence values without yet relying on final ranking UI.

## 3. Scope and exclusions

Include capability registry, OpenAI adapter, LangGraph extraction flow, Pydantic schemas, prompt/schema versions, bounded retries, evidence references, and evaluation fixtures. Exclude final deterministic ranking and arbitrary customer-selected models.

## 4. Design and interaction behavior

High/medium/low confidence is field-specific. Missing or conflicting evidence remains visible. Low confidence routes to review rather than appearing confirmed.

## 5. Implementation details

- Define provider-neutral request/result models.
- Use a graph with preprocessing, capability call, validation, confidence/evidence checks, and persistence.
- Pin the selected model snapshot after evaluation.
- Minimize sent context and avoid model-side product-state mutation.
- Make adapter configuration replaceable without changing domain schemas.

## 6. Data, API, and state contracts

Extraction includes summary, requested action, action owner, date/time and source type, urgency evidence, priority candidates, confidence per field, supporting message IDs/snippets, adapter/model/prompt/schema versions, and run status.

## 7. Error and edge cases

Prompt injection in email, quoted/forwarded content, conflicting dates, timezone ambiguity, model refusal, truncation, invalid schema, rate limit, timeout, and provider outage.

## 8. Dependencies

Units 03 and 04.

## 9. Security and privacy

Treat email as untrusted data, never instructions. Pass only required content. Do not include tokens or unrelated threads. Record metadata without raw prompts in ordinary logs.

## 10. Test and verification checklist

- [ ] Fake-adapter unit tests cover every capability outcome.
- [ ] OpenAI adapter conforms to product contracts.
- [ ] Structured output and refusal/error handling pass.
- [ ] Prompt-injection fixtures do not alter workflow authority.
- [ ] Confidence/evidence rules are deterministic.
- [ ] Evaluation report covers representative founder scenarios.
- [ ] Model/prompt/schema version is stored for every result.

## 11. Code walkthrough points

Capability abstraction, LangGraph state, structured output, email-as-untrusted-data defense, and evaluation harness.

## 12. Recording assets

Graph diagram, schema example, sanitized evaluation table, failure trace, and adapter replacement explanation.

