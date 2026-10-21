# Agent Test Strategy

## Current scope

The active evaluation target is a tool-using customer-support agent. The repository currently contains a deterministic scripted stand-in and synthetic data. It validates dataset loading, DeepEval case construction, tool selection and argument checks, tool allowlists, state assertions, and reporting. It does **not** measure a company agent or production quality.

The current starter dataset has ten agent tasks: known and unknown order lookup, shipped and pending cancellation, refund lookup, tool failure, out-of-scope request, and privacy-injection cases. Grow this to roughly 20 representative cases after validating the first set with the AI team and SME.

## Test layers and thresholds

| Layer | Current check | Threshold | What the result means / does not mean |
| --- | --- | ---: | --- |
| Tool trace contract | Deterministic equality check over DeepEval `LLMTestCase.tools_called` and `expected_tools`, including input parameters and order | 100% exact match | Every scripted tool call and argument matches the case. This does not establish task success by itself. |
| Tool authorization | Ordinary Python allowlist assertion | 100% of calls authorized | No recorded call is outside the case allowlist. This is a local deterministic check; it is not DeepEval's `ToolPermissionMetric`. |
| State contract | Exact comparison of final simulated state with expected state | Exact equality | The simulated run preserved or changed specified state as expected. It does not validate a real backend transaction. |
| Final response contract | Exact comparison with the expected response for these scripted cases | Exact equality | The stub returned the fixed contract string. This does not measure semantic quality of an LLM answer. |
| Task completion / argument quality | Not implemented | Calibrate after human review | Add DeepEval `TaskCompletionMetric` and `ArgumentCorrectnessMetric` after connecting an approved agent trace and judge. These are judge-based and probabilistic. |

The installed `deepeval==4.2.8` initializes its default OpenAI model when constructing `ToolCorrectnessMetric`, even when `available_tools` is omitted. To keep the current harness offline, it uses DeepEval's `LLMTestCase` structure and compares the expected and actual tool traces directly. The same pinned version does not expose `ToolPermissionMetric`; the allowlist assertion provides the deterministic permission gate without silently changing the dependency. Revisit both native metrics after a version review and verify they work without judge credentials before adopting them as CI gates.

## Dataset and runner

Agent cases live in `testdata/agent_dataset.json`. Each case provides a task, scenario key, expected output, expected tool names and arguments, allowed tools, initial state, and expected final state. `utils/agent_stub.py` executes scripted local scenarios and returns the output, ordered tool calls, and final state. `tests/test_agent_harness.py` runs every case through the adapter and checks each contract.

The stub scripts and the expected dataset are separate, so a broken tool trace or state transition can fail the checks. Keep provider credentials out of source and datasets. Use synthetic data in all local scenarios.

## Next stages

1. **Discover the real agent:** confirm staging endpoint, tool inventory and write permissions, trace access, sandbox/data set, external-judge data policy, and SME contact.
2. **Grow and review the dataset:** expand the ten starter cases toward 20; have an SME label expected outcomes and risky side effects.
3. **Connect an adapter:** replace the scripted runner with a staging adapter only after sandboxing and trace access are confirmed. Do not enable destructive tools against production.
4. **Add judge metrics:** add task completion and argument correctness, document provider/model, credentials, expected cost, data handling, thresholds, and reproducibility limits. Run repeated trials and compare judge results with human review before setting quality gates.
5. **Add CI:** run a small deterministic smoke subset on each merge request and the full dataset nightly. Store agent/model, judge/model, dataset revision, code commit, and run results. Keep probabilistic scores separate from deterministic security and state contracts.
6. **Operate the corpus:** add reviewed failures from staging or production traces, and schedule red-team cases for injection, leakage, unauthorized actions, and tool failures.

## Current command

Run the offline harness and generate its report with:

```bash
npm run test:qa
```

The command does not call an external model or API. An optional `npm run test:qa:gemini` command sends one short request to Google's Gemini Developer API using `GEMINI_API_KEY` and `GEMINI_MODEL` from `.env` or the shell. It is a connectivity smoke test only; it does not test tool use or task completion. The prompt is synthetic, output is capped at 128 tokens, and a successful response is printed in the terminal. Requests eligible for the Gemini Free tier have no token charge, but quota/model eligibility can vary and paid-tier usage is billed. Google's pricing documentation says free-tier content may be used to improve its products. Do not send customer or confidential data. A model alias may change over time, so record the selected model and run date when comparing results. See [WORKLOG.md](WORKLOG.md) for recent quota and API failure observations.
