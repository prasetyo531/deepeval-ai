# AI Testing Lab

A learning project for evaluating a tool-using customer-support agent. It has two separate paths: an offline deterministic agent harness and an optional live Gemini connectivity smoke test. Neither currently evaluates a company or production agent.

## Current agent harness

```text
agent_dataset.json -> scripted agent -> simulated tools and state
                   -> DeepEval LLMTestCase + local deterministic assertions -> HTML report
```

The ten starter scenarios cover order lookup, cancellation boundaries, refund policy, unknown orders, prompt injection, lack of cancellation confirmation, tool failure, and out-of-scope requests. Tests check expected tool names and arguments, per-case tool allowlists, final state, and fixed response contracts. Passing this suite demonstrates that the harness works; it does not measure a company or production agent.

The runner uses DeepEval's `LLMTestCase` schema and local deterministic checks for exact ordered tool calls, arguments, permissions, simulated state, and response contracts. It does not run DeepEval judge metrics. In the pinned `deepeval==4.2.8`, constructing `ToolCorrectnessMetric` initializes its default OpenAI model, and `ToolPermissionMetric` is unavailable. This compatibility gap is documented in [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md). `TaskCompletionMetric` and `ArgumentCorrectnessMetric` are planned after the real agent trace and judge setup are approved.

## Setup and run

The project is configured for Python 3.13 and uses a project-local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm run test:qa
```

The evaluation command is offline and creates `reports/agent-harness.html`. No API key is needed. The optional Gemini test below is separate and is not an agent-quality test.

### Gemini API smoke test: `tests/test_gemini_api.py`

This opt-in test checks that one request can reach Gemini and return the expected marker. It does not run the scripted agent, call simulated tools, test agent quality, or invoke a judge.

1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`; optionally set `GEMINI_MODEL`. `.env` is ignored by Git and must stay local.
2. Run `npm run test:qa:gemini`.
3. On success, the response text is printed as `Gemini response: ...`; pytest's `-s` option makes it visible. If the API returns an error such as 429, 503, or 504, no generated text exists to print.

The adapter sends a synthetic prompt with `temperature=0`, `max_output_tokens=128`, and thinking level `LOW`. It uses a 30-second HTTP timeout and one request attempt. Free-tier access does not guarantee quota for every model or project. Check the project's Usage / Rate limits in AI Studio before retrying; inspect `quotaMetric`, `quotaId`, and `retryDelay` in a complete 429 error. Do not enable billing unless paid usage is intentional. Use synthetic data only because data handling and eligibility depend on the provider tier. Current failure observations are recorded in [docs/WORKLOG.md](docs/WORKLOG.md).

## Plan to connect a real agent

Before replacing the stub, confirm with the AI team: the staging endpoint, tool inventory and write/destructive tools, trace access, sandbox and test data, data policy for external judges, and SME reviewer. Connect through an adapter only after the staging boundary and tool permissions are clear. Then grow the reviewed dataset toward 20 cases, add judge metrics with explicit thresholds and cost/reproducibility notes, compare scores with human labels, and add smoke-per-merge plus nightly full CI runs.

## Project files

```text
testdata/agent_dataset.json   Agent tasks, expected tool calls, permissions, and state
utils/agent_stub.py           Deterministic scripted agent and simulated tools
tests/test_agent_harness.py   Tool trace, authorization, state, and output contracts
utils/gemini_client.py       Optional Gemini API client
tests/test_gemini_api.py     One-request live connectivity check (opt-in)
docs/TEST_STRATEGY.md         Scope, thresholds, limits, and rollout plan
docs/WORKLOG.md               Decisions, recent results, and Gemini troubleshooting
```

See [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md) for the phased plan and the meaning of each check. Keep deterministic functional/security contracts separate from probabilistic judge scores. Do not add live model calls without documenting the provider, credentials, expected cost, data handling, and reproducibility limits.
