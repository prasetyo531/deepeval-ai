# AI Testing Lab Handoff

## Project goal

Build a practical QA framework for a tool-using customer-support agent. The QA contribution is to define expected behavior, build a repeatable runner, and establish quality gates. The active scope is agent tasks, tool traces, permissions, and state changes—not chatbot text quality alone.

## Current repository state

- Python, pytest, and DeepEval are used for the local harness.
- `testdata/agent_dataset.json` contains ten synthetic scenarios.
- `utils/agent_stub.py` simulates a deterministic agent and local tool calls.
- `tests/test_agent_harness.py` checks ordered tool calls, arguments, allowlists, final state, and fixed response contracts.
- `npm run test:qa` runs the offline suite and creates `reports/agent-harness.html`.
- No staging agent, external judge, or CI workflow is connected. An opt-in Gemini API connectivity smoke test exists; it is not an agent eval.

The pinned DeepEval version initializes an OpenAI model when creating `ToolCorrectnessMetric`, and does not provide `ToolPermissionMetric`. Current tool and permission gates therefore use direct deterministic assertions over DeepEval `LLMTestCase` records. See [docs/TEST_STRATEGY.md](docs/TEST_STRATEGY.md).

## Next steps

1. Ask the AI team for the staging endpoint, tools and write permissions, trace access, sandbox/test data, and data policy for external judges.
2. Identify an SME to validate expected outcomes and ambiguous scenarios.
3. Grow the reviewed dataset toward 20 tasks, including multi-step flows, failures, out-of-scope requests, and adversarial inputs.
4. Connect an adapter to a safe staging agent, then consider judge metrics and CI gates after calibrating against human labels.

Keep provider credentials out of source and datasets. Before any live model call, document provider, credential setup, expected cost, data handling, and reproducibility limits.
