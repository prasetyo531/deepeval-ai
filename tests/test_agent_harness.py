"""Deterministic contract checks for the tool-using support-agent harness."""

import json
from pathlib import Path
from typing import Any

import pytest
from deepeval.test_case import LLMTestCase, ToolCall

from utils.agent_stub import run_support_agent


DATASET_PATH = Path(__file__).parents[1] / "testdata" / "agent_dataset.json"


def load_agent_dataset() -> list[dict[str, Any]]:
    with DATASET_PATH.open(encoding="utf-8") as dataset_file:
        return json.load(dataset_file)


def _tool_calls(calls: list[dict[str, Any]]) -> list[ToolCall]:
    return [ToolCall(name=call["name"], input_parameters=call.get("input_parameters", {})) for call in calls]


@pytest.mark.parametrize("case", load_agent_dataset(), ids=lambda case: case["id"])
def test_agent_task_tools_permissions_and_state(case: dict[str, Any]) -> None:
    result = run_support_agent(case)
    actual_calls = result["tools_called"]
    allowed_tools = set(case["allowed_tools"])

    expected_calls = _tool_calls(case["expected_tools"])
    # Keep this gate offline. DeepEval 4.2.8 initializes its default OpenAI
    # model while constructing ToolCorrectnessMetric, even when only exact
    # expected-tool matching is wanted. LLMTestCase retains DeepEval's schema;
    # this deterministic assertion checks the same trace contract without a
    # judge or credentials.
    test_case = LLMTestCase(
        input=case["task"],
        actual_output=result["actual_output"],
        tools_called=actual_calls,
        expected_tools=expected_calls,
    )
    assert test_case.tools_called == expected_calls, f"{case['id']} tool trace mismatch"
    assert all(call.name in allowed_tools for call in actual_calls), (
        f"{case['id']} called a tool outside its allowlist: "
        f"{[call.name for call in actual_calls]}"
    )
    assert result["actual_output"] == case["expected_output"], case["id"]
    assert result["final_state"] == case["expected_state"], case["id"]
