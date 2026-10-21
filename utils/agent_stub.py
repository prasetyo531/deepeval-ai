"""Deterministic, tool-using support-agent stand-in for harness development."""

from copy import deepcopy
from typing import Any

from deepeval.test_case import ToolCall


def run_support_agent(case: dict[str, Any]) -> dict[str, Any]:
    """Run one scripted scenario and return its output, trace, and final state.

    This deliberately does not call a model. Scenario scripts validate the
    evaluation wiring; they do not represent production-agent performance.
    """
    state = deepcopy(case["initial_state"])
    scenario = case["scenario"]
    order_id = _order_id(case["task"])
    tools: list[ToolCall] = []

    def lookup() -> dict[str, Any] | None:
        tools.append(ToolCall(name="lookup_order", input_parameters={"order_id": order_id}))
        if scenario == "lookup_failure":
            raise RuntimeError("simulated order service unavailable")
        return state["orders"].get(order_id)

    try:
        if scenario in {"lookup_known", "unknown_order", "cancel_shipped", "cancel_pending", "cancel_no_confirmation", "refund_window", "privacy_and_lookup", "lookup_failure"}:
            order = lookup()
            if scenario == "privacy_and_lookup":
                output = "I can’t provide another customer’s personal information. "
                output += f"Order {order_id} shipped on 2026-10-08. Tracking: {order['tracking']}."
            elif scenario == "lookup_known":
                output = f"Order {order_id} shipped on 2026-10-08. Tracking: {order['tracking']}."
            elif scenario == "unknown_order":
                output = f"I can’t find order {order_id}. Check the order number or contact support for help."
            elif scenario == "cancel_shipped":
                output = f"Order {order_id} has already shipped and cannot be cancelled. You can request a return after delivery."
            elif scenario == "cancel_pending":
                tools.append(ToolCall(name="request_cancellation", input_parameters={"order_id": order_id}))
                order["status"] = "cancelled"
                output = f"Order {order_id} has been cancelled."
            elif scenario == "cancel_no_confirmation":
                output = f"Order {order_id} is pending. Please confirm if you want me to cancel it."
            elif scenario == "refund_window":
                tools.append(ToolCall(name="get_refund_policy", input_parameters={"order_id": order_id}))
                output = "Refunds are issued within 5–7 business days after the return is received and inspected."
            else:
                output = "I can’t retrieve the order right now. Please try again later."
        elif scenario == "privacy_refusal":
            output = "I can’t provide another customer’s personal information."
        else:
            output = "I can help with order status, cancellations, or refund questions."
    except RuntimeError:
        output = "I can’t retrieve the order right now. Please try again later."

    return {"actual_output": output, "tools_called": tools, "final_state": state}


def _order_id(task: str) -> str:
    for token in task.split():
        normalized = token.strip(".,?!")
        if normalized.startswith("ORD-"):
            return normalized
    return ""
