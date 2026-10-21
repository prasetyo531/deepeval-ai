# Learning Roadmap

This roadmap tracks the repository's agent evaluation work, not personal learning progress.

| Stage | Focus | Status |
| --- | --- | --- |
| 0 | Discover the real agent: endpoint, tools and write permissions, traces, sandbox, external-judge data policy, SME | Pending team input |
| 1 | Build a small dataset of agent tasks, expected tool calls, permissions, and state | In progress: ten synthetic starter scenarios are checked into `testdata/agent_dataset.json`; expand toward 20 and review with an SME |
| 2 | Deterministic runner and contracts | Implemented with a scripted agent, DeepEval `LLMTestCase` schema, offline exact trace checks, allowlist assertion, state comparison, and response contract |
| 3 | Baseline and thresholds | Pending a real agent; run repeated trials and compare judge scores with human-reviewed examples before setting quality thresholds |
| 4 | CI gates | Planned: deterministic smoke tests per merge request and full evaluation nightly |
| 5 | Red teaming and corpus operations | Planned: expand injection, privacy leakage, unauthorized action, tool failure, and reviewed production-trace regressions |

## Metric boundaries

The local suite uses no LLM judge. Its exact contracts validate the harness and scripted scenarios only. The pinned DeepEval version currently prevents offline use of its native tool metrics; see `docs/TEST_STRATEGY.md`. Future `TaskCompletionMetric` and `ArgumentCorrectnessMetric` results will be probabilistic judge scores; document their thresholds and limitations, compare them with SME labels, and keep them separate from deterministic security/state assertions.

Any live-model integration must document provider, model/version, credential setup, data handling, expected cost, and reproducibility limits before making calls.
