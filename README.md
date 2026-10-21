# AI Testing Lab

A learning project for evaluating a tool-using customer-support agent. The current harness uses a deterministic local stand-in to validate agent-level test wiring without a model call, API credentials, or live side effects.

## Current agent harness

```text
agent_dataset.json -> scripted agent -> simulated tools and state
                   -> DeepEval tool trace check + deterministic assertions -> HTML report
```

The ten starter scenarios cover order lookup, cancellation boundaries, refund policy, unknown orders, prompt injection, lack of cancellation confirmation, tool failure, and out-of-scope requests. Tests check expected tool names and arguments, per-case tool allowlists, final state, and fixed response contracts. Passing this suite demonstrates that the harness works; it does not measure a company or production agent.

The runner uses DeepEval's `LLMTestCase` schema and deterministic checks for exact ordered tool calls, arguments, permissions, state, and response contracts. In the pinned `deepeval==4.2.8`, constructing `ToolCorrectnessMetric` initializes its default OpenAI model, and `ToolPermissionMetric` is unavailable. The harness therefore does not call either metric while it must remain offline; this compatibility gap is documented in [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md). `TaskCompletionMetric` and `ArgumentCorrectnessMetric` are planned after the real agent trace and judge setup are approved.

## Setup and run

The project is configured for Python 3.13 and uses a project-local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm run test:qa
```

The evaluation command is offline and creates `reports/agent-harness.html`. No API key is needed. An optional one-request Gemini connectivity check is separate from the suite and is not an agent-quality test.

To configure Gemini, copy `.env.example` to `.env` and set `GEMINI_API_KEY`. The key stays local and `.env` is ignored by Git. Install dependencies with `python -m pip install -r requirements.txt`, then run `npm run test:qa:gemini` explicitly. That command sends one short synthetic prompt, caps output at 128 tokens, and prints a successful text response in the terminal. The request uses low thinking, a 30-second HTTP timeout, and one attempt. Gemini free-tier eligibility and quotas depend on the project/model; check AI Studio before using it. Google's free-tier terms say submitted content may be used to improve products, so use synthetic data only. This smoke test verifies API connectivity only; the tool-using agent still runs as a local stub.

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
```

See [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md) for the phased plan and the meaning of each check. Keep deterministic functional/security contracts separate from probabilistic judge scores. Do not add live model calls without documenting the provider, credentials, expected cost, data handling, and reproducibility limits.
