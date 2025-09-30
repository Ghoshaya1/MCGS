from langgraph.graph import StateGraph, END
from .state import BuildState
from .agents.planner import planner_node
from .agents.architect import architect_node
from .agents.dev import dev_node
from .agents.test_agent import tests_node
from .agents.security import security_node
from .agents.pr_agent import pr_node


def build_graph():
    graph = StateGraph(BuildState)

    graph.add_node("plan", planner_node)
    graph.add_node("design", architect_node)
    graph.add_node("dev", dev_node)
    graph.add_node("tests", tests_node)
    graph.add_node("security", security_node)
    graph.add_node("pr", pr_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "design")
    graph.add_edge("design", "dev")

    def dev_to_tests(state):
        return "tests"

    def tests_next(state):
        # Prevent infinite loops by limiting retries
        dev_attempts = state.get("dev_attempts", 0)
        if dev_attempts >= 3:
            state["logs"].append("Max dev attempts reached, proceeding to security")
            return "security"
        return "security" if (state.get("tests_ok") and state.get("lint_ok")) else "dev"

    def sec_next(state):
        # Prevent infinite loops by limiting retries
        dev_attempts = state.get("dev_attempts", 0)
        if dev_attempts >= 3:
            state["logs"].append("Max dev attempts reached, proceeding to PR")
            return "pr"
        return "pr" if state.get("sec_ok") else "dev"

    graph.add_conditional_edges("dev", dev_to_tests, {"tests": "tests"})
    graph.add_conditional_edges("tests", tests_next, {"dev": "dev", "security": "security"})
    graph.add_conditional_edges("security", sec_next, {"dev": "dev", "pr": "pr"})
    graph.add_edge("pr", END)

    return graph.compile()
