# Project Guidance

- Keep provider credentials out of source files and committed datasets.
- Keep deterministic functional/security contract checks separate from probabilistic LLM quality metrics.
- Give every metric an explicit threshold and document what its score does and does not mean.
- Prefer reusable pytest fixtures and JSON/JSONL test data over duplicated inline cases.
- Do not add live model calls without documenting the provider, credential setup, expected cost, and reproducibility limits.
- Run the documented evaluation command after changing the harness and report the actual result.
