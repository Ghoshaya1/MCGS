from ..tools.runners import run_pip_audit


def security_node(state):
    code, out = run_pip_audit(state["repo_path"])
    state["sec_ok"] = (code == 0)
    state["logs"].append(f"pip-audit: exit={code}\n" + out[:1000])
    return state
