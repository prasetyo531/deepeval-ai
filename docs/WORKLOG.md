# Worklog

## 2026-10-21 — Agent harness and Gemini smoke test

### Direction and scope

- Switched the evaluation target from chatbot-level response checks to a tool-using agent.
- Kept the current evaluation offline and deterministic: a local scripted agent stub, simulated tools/state, and synthetic cases. It validates the harness, not a company or production agent.
- The starter dataset has ten scenarios covering order lookup, cancellation boundaries, refund policy, unknown orders, prompt injection, missing authorization, tool failure, and out-of-scope requests.
- Current offline command: `npm run test:qa`. Latest result after harness/config changes: **10 passed**.
- Native DeepEval judge metrics are not enabled. `ToolCorrectnessMetric` initializes its default OpenAI model in the pinned setup, and `ToolPermissionMetric` is unavailable; current trace, allowlist, state, and response checks are deterministic assertions. Judge metrics remain future work after an approved real-agent trace and judge setup.

### Gemini setup and purpose

- Added an optional one-request connectivity smoke test, `npm run test:qa:gemini`. It verifies access to Gemini only; it does not evaluate agent tool use or agent quality.
- The adapter reads `GEMINI_API_KEY` and `GEMINI_MODEL` from the project `.env` or shell. `.env` is ignored by Git; no credentials are recorded here.
- The request uses a synthetic marker prompt, `temperature=0`, `max_output_tokens=128`, and `thinking_level=LOW`. The Python SDK HTTP timeout is 30 seconds and retry attempts are set to one.
- Successful responses are printed as `Gemini response: ...`; the pytest script uses `-s` so stdout is visible. API errors happen before that print, so failed calls have no generated text to log.
- Model default in the adapter is `gemini-3.8-flash`; verify the model selected in `.env` and its current availability/quota in AI Studio.

### Gemini troubleshooting observed

- A request previously returned `402 RESOURCE_EXHAUSTED` with a prepayment-credit message.
- A later request returned `503 UNAVAILABLE` due to high demand; another returned `504 DEADLINE_EXCEEDED`.
- A response arrived with no text when the output limit was 32 tokens. The limit was raised to 128 and thinking was set to `LOW`. `MINIMAL` was rejected by the selected model with `400 INVALID_ARGUMENT`; `LOW` is the supported setting tested successfully.
- With the updated token/thinking configuration, `npm run test:qa:gemini` passed once in **24.78 seconds**.
- After adding response-to-stdout logging, the next integration run returned `503 UNAVAILABLE`, so it printed no response. The latest user-provided error is `429 RESOURCE_EXHAUSTED`: the provider reports quota exhaustion. This is a provider/project/model limit, not a pytest assertion failure. The exact dimension cannot be inferred from the truncated error excerpt.
- Check AI Studio Usage / Rate limits for the project associated with the API key and the selected model. Inspect the full error details for `quotaMetric`, `quotaId`, and `retryDelay`; quota may be rate-, token-, daily-, or model-specific. Do not paste API keys into chat or commit them.

### Next steps

1. In AI Studio, inspect quota and usage for the key's project and selected model; use the full 429 details to identify the exhausted limit.
2. Wait for any stated retry delay or quota reset, or select another model with available quota. Only enable paid billing if that is an intentional choice.
3. Re-run `npm run test:qa:gemini`; on success the text response should appear in the terminal. The deterministic suite remains separate and is run with `npm run test:qa`.
4. Continue the agent plan only after the AI team confirms staging access, tool inventory/permissions, traces, sandbox/test data, judge data policy, and SME reviewer.
