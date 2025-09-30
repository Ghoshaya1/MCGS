from typing import List, TypedDict, Optional


class BuildState(TypedDict):
    request: str
    repo_path: str
    # artifacts
    prd: str
    rfc: str
    tasks: List[dict]
    # control flags
    branch: str
    lint_ok: bool
    tests_ok: bool
    sec_ok: bool
    pr_url: str
    dev_attempts: int
    # trace
    logs: List[str]
