from ..tools.code_runner import run_project_tests, run_project_linting
from ..tools.file_operations import analyze_project_structure


def tests_node(state):
    # Analyze project to determine language and structure
    project_analysis = analyze_project_structure(state["repo_path"])
    language = project_analysis.get("primary_language", "unknown")
    
    # Run language-appropriate linter
    code, out = run_project_linting(state["repo_path"], project_analysis)
    state["lint_ok"] = (code == 0)
    state["logs"].append(f"Linter ({language}): exit={code}\n" + out[:1000])

    # Run language-appropriate tests
    code, out = run_project_tests(state["repo_path"], project_analysis)
    state["tests_ok"] = (code == 0)
    state["logs"].append(f"Tests ({language}): exit={code}\n" + out[:1000])
    
    return state
